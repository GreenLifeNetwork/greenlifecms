from django.db import models

from wagtail.core.models import Page


class HomePage(Page):
    parent_page_types = []
    pass
