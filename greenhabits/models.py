from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.api import APIField




class GreenHabitIndexPage(Page):
    parent_page_types = []
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        GreenHabitpages = self.get_children().live().order_by('-first_published_at')
        context['greenhabitspages'] = GreenHabitpages
        context['all']=self.get_children()
        return context


class GreenHabitPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'GreenHabitPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class GreenHabitTagIndexPage(Page):
    parent_page_types = []
    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        GreenHabitpages = GreenHabitPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['GreenHabitpages'] = GreenHabitpages
        return context


class GreenHabitPage(Page):
    # date = models.DateField("Post date", auto_now_add=True, blank=True)
    header = models.CharField(max_length=250, blank=True)
    TYPES = (
        ('law', 'Law'), ('essential', 'Essential'), ('habit', 'Habit')
    )
    importance = models.CharField(choices=TYPES, max_length=20)
    summary = models.CharField(max_length=250, blank=True)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=GreenHabitPageTag, blank=True)
    link = models.URLField(blank=True)
    reference = models.CharField(blank=True, max_length=250)
    notes = models.TextField(blank=True)

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
        APIField('header'),
        APIField('summary'),
        APIField('body'),
        APIField('importance'),
        APIField('link'),
        APIField('notes'),
        APIField('reference'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            # FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="Sustainable habit details"),
        # FieldPanel('header'),
        FieldPanel('summary'),
        FieldPanel('importance'),
        FieldPanel('body', classname="full"),
        FieldPanel('link'),
        FieldPanel('reference'),
        FieldPanel('notes'),
    ]

    # Various rating assessing the impact of the habit
    # class GreenHabitRating(Page)

    # class GreenHabitPageGalleryImage(Orderable):
    #     page = ParentalKey(GreenHabitPage, on_delete=models.CASCADE, related_name='gallery_images')
    #     image = models.ForeignKey(
    #         'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    #     )
    #     caption = models.CharField(blank=True, max_length=250)
    #
    #     panels = [
    #         ImageChooserPanel('image'),
    #         FieldPanel('caption'),
    #     ]


