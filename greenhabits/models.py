import datetime
from urllib.parse import urlparse

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.forms import ValidationError
from django.shortcuts import render
from django.views.generic import ListView
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import MultiFieldPanel, RichTextFieldPanel, FieldPanel, StreamFieldPanel
from wagtail.api import APIField
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index


# See how long it takes before that becomes too lax..
# @receiver(post_save, sender=User)
# def set_user_as_contributor(sender, instance, created, **kwargs):
#     if created:
#         # This group should exist from last db backup.
#         # TODO: check backup strategy
#         instance.groups.add(Group.objects.get(name='Editors'))
#         instance.save()


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

    # this route needs to be protected
    @route(r'^week/(\d+)/$', name='week')
    def render_page_by_week(self, request, week):
        week_offset = int(week) * 7
        GreenHabitPages = GreenHabitPage.objects.order_by('-id').all()[week_offset:week_offset + 7]
        return render(request, 'greenhabits/green_habit_index_page.html', {
            'greenhabitspages': GreenHabitPages,
        })

    @route(r'^lastweek/$', name='lastweek')
    def render_page_by_last_week(self, request):
        GreenHabitPages = GreenHabitPage.objects.order_by('-id')[:7]
        return render(request, 'greenhabits/green_habit_index_page.html', {
            'greenhabitspages': GreenHabitPages,
        })

    @route(r'^(\d+)/$', name='id')
    def render_page_by_id(self, request, id):
        page = GreenHabitPage.objects.get(id=int(id))
        return render(request, 'greenhabits/green_habit_page.html', {
            'page': page,
        })


class PetitionPage(Page, models.Model):
    petition = StreamField([
        ('link', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('url', blocks.URLBlock()),
            ('expiry_date', blocks.DateBlock(default=datetime.datetime.now() + datetime.timedelta(days=30),
                                             help_text='Important: petitions have a short lifespan and can expire within days!')),
            ('summary', blocks.CharBlock(required=False)),
        ]))])

    content_panels = Page.content_panels + [
        StreamFieldPanel('petition'),
    ]

    def __str__(self):
        return self.petition

    api_fields = [
        APIField('petition'),
    ]


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


class GreenHabitIdeas(Page):
    idea = models.CharField(blank=True, max_length=1000, help_text='The idea summary')
    content_panels = Page.content_panels + [
        FieldPanel('idea', classname="full"),
    ]


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


class Link(models.Model):
    name = models.URLField()
    choices = (
        ('headline', 'headline'),
        ('study', 'Study'),
        ('source', 'Source'),
    )
    typeOf = models.CharField(max_length=15, choices=choices)


def validate_url(value):
    if not value:
        return  # Required error is done the field
    obj = urlparse(value)
    if obj.scheme != 'https':
        raise ValidationError(f'Only secure links can be used: https://...')


class GreenHabitPage(Page, models.Model):
    CARBON_FOOTPRINT_IMPACT_TYPES = (
        ('high', 'High co2e reduction'),
        ('medium', 'Medium co2e reduction'),
        ('low', 'Low co2e reduction')
    )
    AUDIENCE = (
        ('global', 'Global'),
        ('UK', 'UK'),
        ('US', 'US')
    )

    class Meta:
        verbose_name = "Nudge"

    # def colored_first_name(self):
    #     return format_html(
    #         '<span style="color: #{};">{}</span>',
    #         self.description,
    #         self.title,
    #     )
    # colored_first_name.admin_order_field = 'first_name'

    ordering = ['-pub_date', 'author']

    description = models.CharField(blank=False,
                                   max_length=100,
                                   help_text='Title of the nudge as it appears on history and favourites. This is '
                                             'what the user will save and search.')
    carbon_footprint_impact = models.CharField(choices=CARBON_FOOTPRINT_IMPACT_TYPES, max_length=20, default='low')
    delivered = models.BooleanField(default=False, help_text='Set to false once delivered with scheduler')
    tags = ClusterTaggableManager(through=GreenHabitTagPage,
                                  blank=True,
                                  help_text='Tags to mark the content. ie: energy, diet, household...')
    body = RichTextField(blank=True,
                         max_length=1000,
                         help_text='This should be a short paragraph where the carbon reduction habits '
                                   'should be highlighted. Avoid lists. Keep the message focused. '
                                   'One day. One change.')
    hero_image = models.ImageField(blank=False,
                                   upload_to="nudge_post_heros")
    quiz = models.JSONField(blank=True, default={})
    headline_link = RichTextField(blank=True, help_text='headline link: source content')

    study_link = RichTextField(help_text="study link: study/paper supporting content (can be pdf, diagram...) ",
                               blank=True)
    other_link = RichTextField(help_text="other link: any links related to content", blank=True)
    footnote = RichTextField(blank=True,
                             max_length=500,
                             help_text='Inspirational quote or funny facts to leave the user on high note and'
                                       ' strongly encourage sharing/saving ')
    notes = models.TextField(blank=True,
                             help_text='Notes about the quote. '
                                       'Useful for drafts and/or moderators comment. '
                                       'Not published.')
    audience = models.CharField(choices=AUDIENCE,
                                max_length=20,
                                default='global',
                                help_text="Content can be global or country specific. Our main audience is UK for now but global is preferred for reusability and we're not restricting add distribution. Be mindful of links used (metrics used, GDPR like restrictions); Some might not be accessible in every country")

    # obsolete since we usually link back
    source = models.CharField(max_length=120,
                              blank=True,
                              help_text='Original author or source. '
                                        'If website or article. '
                                        'Use link field but only the domain name here! ')

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('description'),
        index.SearchField('carbon_footprint_impact'),
        index.SearchField('body'),
        index.SearchField('quiz'),
    ]

    # Export fields over the API
    api_fields = [
        # APIField('published_date'),
        APIField('body'),
        APIField('hero_image'),
        APIField('carbon_footprint_impact'),
        APIField('description'),
        APIField('headline_link'),
        APIField('study_link'),
        APIField('footnote'),
        APIField('other_link'),
        APIField('notes'),
        APIField('source'),
        APIField('quiz'),
        # APIField('links'),
        # APIField('reference'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('audience'),
        MultiFieldPanel([
            # FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="Sustainable habit details"),
        FieldPanel('carbon_footprint_impact'),
        FieldPanel('delivered'),
        RichTextFieldPanel('body', classname="full"),
        FieldPanel('hero_image', classname="full"),
        FieldPanel('headline_link'),
        FieldPanel('study_link'),
        FieldPanel('other_link'),
        FieldPanel('footnote'),
        # FieldPanel('source'),
        # FieldPanel('reference'),
        FieldPanel('notes'),
        FieldPanel('quiz'),
    ]


class PetitionPageAdmin(ModelAdmin):
    model = PetitionPage
    menu_label = 'Petitions'
    menu_icon = 'warning'
    menu_order = 2
    # list_display = ('petition__link',)
    # list_display = ('petition',)
    # list_display = ('link',)
    list_display = ('__str__',)


class GreenHabitPageAdmin(ModelAdmin):
    model = GreenHabitPage
    menu_label = 'Nudges'
    menu_icon = 'snippet'
    menu_order = 1

    def has_quiz(self, obj):
        if obj.quiz:
            return True
        else:
            return False

    has_quiz.short_description = 'has quiz'
    list_display = ('title', 'description', 'carbon_footprint_impact', 'quiz')
    list_export = ('title', 'description', 'carbon_footprint_impact', 'quiz')


modeladmin_register(GreenHabitPageAdmin)
modeladmin_register(PetitionPageAdmin)


class StaticPage(Page):
    # parent_page_types = []  # make the page private
    body = RichTextField()
    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
