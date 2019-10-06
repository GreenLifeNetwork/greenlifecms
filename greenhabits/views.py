from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from wagtail.core.models import Page
from wagtail.search.models import Query
from .models import greenhabitIndexPage, greenhabitPage


def greenhabit_light(request):
    greenhabit_entries = greenhabitPage.objects.all()
    # page = request.GET.get('page', 1)

    # Pagination
    # paginator = Paginator(greenhabit_entries, 10)
    # try:
    #     search_results = paginator.page(page)
    # except PageNotAnInteger:
    #     search_results = paginator.page(1)
    # except EmptyPage:
    #     search_results = paginator.page(paginator.num_pages)
    #
    # print('habit entries', greenhabit_entries)
    return render(request, 'greenhabit/greenhabit_index_page_public.html', {
        'habit_entries': greenhabit_entries,
    })
