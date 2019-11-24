from django.db import models
from django.shortcuts import render
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


class GreenHabitTagPage(TaggedItemBase):
    content_object = ParentalKey(
        'GreenHabitPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


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
    header = models.CharField(max_length=250, blank=True)
    TYPES = (
        ('law', 'Law'), ('essential', 'Essential'), ('habit', 'Habit')
    )
    importance = models.CharField(choices=TYPES, max_length=20, default='habit')
    summary = models.CharField(max_length=180, help_text='Mobile quote! Keep this short and effective')
    tags = ClusterTaggableManager(through=GreenHabitTagPage,
                                  help_text='Tags to mark the content. ie: energy, diet, household...')
    body = RichTextField(blank=True, help_text='The body is additional content for larger devices')
    links = RichTextField(blank=True, help_text='Call to actions or details regarding suggestion')
    source = models.CharField(max_length=120, default='',
                              help_text='Original author or source. If website or article. Use link field but only the domain name here! Seek approval of the owner before publishing')
    reference = models.CharField(blank=True, max_length=250, help_text='If source is not link (like paper or archives)')
    notes = models.TextField(blank=True,
                             help_text='Notes about the quote. Useful for drafts and moderators. Not published.')

    search_fields = Page.search_fields + [
        index.SearchField('header'),
        index.SearchField('summary'),
        index.SearchField('tags'),
        index.SearchField('importance'),
        # index.SearchField('body'),
    ]

    # Export fields over the API
    api_fields = [
        # APIField('published_date'),
        APIField('summary'),
        APIField('header'),
        APIField('body'),
        APIField('importance'),
        APIField('links'),
        APIField('notes'),
        APIField('source'),
        # APIField('reference'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            # FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="Sustainable habit details"),
        # FieldPanel('header'),
        FieldPanel('source'),
        FieldPanel('summary'),
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
