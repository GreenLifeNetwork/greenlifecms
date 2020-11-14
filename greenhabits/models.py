from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.shortcuts import render
from django.views.generic import ListView
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.core import blocks
from wagtail.core.models import Page, Orderable, Group
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.search import index
from wagtail.api import APIField

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


# See how long it takes before that becomes too lax..
@receiver(post_save, sender=User)
def set_user_as_contributor(sender, instance, created, **kwargs):
    if created:
        # This group should exist from last db backup.
        # TODO: check backup strategy
        instance.groups.add(Group.objects.get(name='Editors'))
        instance.save()


class GreenHabitIndexPage(RoutablePageMixin, Page):
    # parent_page_types = []
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        GreenHabitPages = self.get_children().live().order_by('-first_published_at')
        context['greenhabitspages'] = GreenHabitPages
        context['all'] = self.get_children()
        return context

    @route(r'^(\d+)/$', name='id')
    def render_page_by_id(self, request, id):
        page = GreenHabitPage.objects.get(id=int(id))
        return render(request, 'greenhabits/green_habit_page.html', {
            'page': page,
        })


class BlogTagPage(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class GreenHabitTagPage(TaggedItemBase):
    content_object = ParentalKey(
        'GreenHabitPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogPageIndex(RoutablePageMixin, Page):
    intro = RichTextField(blank=True, default='Green Life articles')

    # def get_blog_items(self):
    #     # This returns a Django paginator of blog items in this section
    #     return Paginator(self.get_children().live().type(BlogPage), 1)

    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        pages_tagged = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['pages_tagged'] = pages_tagged
        posts = self.get_children().live().reverse()
        page = request.GET.get('page', 1)
        paginator = Paginator(posts, 1)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        return context


class BlogPage(Page):
    body = RichTextField(blank=False)
    summary = models.CharField(max_length=180, help_text='The article summary')
    tags = ClusterTaggableManager(blank=True, through=BlogTagPage,
                                  help_text='Tags to mark the content. ie: energy, diet, household...')
    links = RichTextField(blank=True, help_text='Possible links to follow up or support discussions')
    reference = models.CharField(blank=True, max_length=250, help_text='If source is not link (like paper or archives)')
    notes = models.TextField(blank=True,
                             help_text='Notes about the quote. Useful for drafts and moderators. Not published.')
    search_fields = Page.search_fields + [
        index.SearchField('summary'),
        index.SearchField('tags'),
        index.SearchField('body'),
    ]

    # Export fields over the API
    api_fields = [
        APIField('body'),
        APIField('tags'),
        APIField('links'),
        APIField('reference'),
        APIField('notes'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('tags'),
        ], heading="Blog pages"),
        FieldPanel('body', classname="full"),
        FieldPanel('summary'),
        FieldPanel('links'),
        FieldPanel('reference'),
        FieldPanel('notes'),
    ]


class BlogList(ListView):
    model = BlogPage
    paginate_by = 1


class GreenHabitTagIndexPage(Page):
    # parent_page_types = []

    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        pages_tagged = GreenHabitPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['pages_tagged'] = pages_tagged
        return context


class GreenHabitPage(Page):
    TYPES = (
        ('law', 'Law'), ('essential', 'Essential'), ('habit', 'Habit')
    )
    source = models.CharField(max_length=120, blank=True,
                              help_text='Original author or source. If website or article. Use link field but only the domain name here! Seek approval of the owner before publishing')
    importance = models.CharField(choices=TYPES, max_length=20, default='habit', blank=True)
    tags = ClusterTaggableManager(through=GreenHabitTagPage, blank=True,
                                  help_text='Tags to mark the content. ie: energy, diet, household...')
    body = RichTextField(blank=True, help_text='The body is additional content for larger devices')
    links = RichTextField(blank=True, help_text='Call to actions or details regarding suggestion')
    reference = models.CharField(blank=True, max_length=250, help_text='If source is not link (like paper or archives)')
    notes = models.TextField(blank=True,
                             help_text='Notes about the quote. Useful for drafts and/or moderators comment. Not published.')

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        # index.SearchField('tags'),
        # index.SearchField('importance'),
        index.SearchField('body'),
    ]

    # Export fields over the API
    api_fields = [
        # APIField('published_date'),
        APIField('body'),
        APIField('importance'),
        APIField('links'),
        APIField('notes'),
        APIField('source'),
        # APIField('reference'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('source'),
        MultiFieldPanel([
            # FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="Sustainable habit details"),
        FieldPanel('importance'),
        FieldPanel('body', classname="full"),
        FieldPanel('links'),
        FieldPanel('reference'),
        FieldPanel('notes'),
    ]


class StaticPage(Page):
    # parent_page_types = []  # make the page private
    body = RichTextField()
    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
