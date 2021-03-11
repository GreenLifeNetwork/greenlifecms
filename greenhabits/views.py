import json

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render

from wagtail.core.models import Page
from wagtail.search.models import Query
from .models import GreenHabitPage
from django.http import HttpResponse
from django.db.models import Q

NUDGE_FIELDS = ('id', 'body', 'hero_image', 'headline_link', 'study_link', 'other_link', 'last_published_at', 'title')


# NUDGE_FIELDS = ('id', 'body', 'last_published_at', 'importance', 'image', 'headline')


# TODO nudge model refactor: headline
# TODO nudge model refactor: body to stream!
# TODO: check valid header token in request


def json_week(request, id):
    # Grabs a QuerySet of dicts
    week_offset = id * 7
    week_limit = week_offset + 7
    qs = GreenHabitPage.objects.live().order_by('-id').all()[week_offset:week_limit].values(*NUDGE_FIELDS)

    # Convert the QuerySet to a List
    list_of_dicts = list(qs)

    # Convert List of Dicts to JSON
    data = json.dumps(list_of_dicts, cls=DjangoJSONEncoder)
    return HttpResponse(data, content_type="application/json")


def json_ids(request, ids):
    # Grabs all the ids
    q_query_str = [f"Q(id={id})|" for id in ids.split(',')]
    q_query_str = ''.join(q_query_str).rstrip('|')
    q_query = eval(q_query_str)
    qs = GreenHabitPage.objects.live().filter(q_query).values(*NUDGE_FIELDS)

    # Convert the QuerySet to a List
    list_of_dicts = list(qs)

    # Convert List of Dicts to JSON
    data = json.dumps(list_of_dicts, cls=DjangoJSONEncoder)
    return HttpResponse(data, content_type="application/json")


def json_last_week(request):
    # Grabs a QuerySet of dicts
    qs = GreenHabitPage.objects.live().order_by('-id')[:7].values(*NUDGE_FIELDS)

    # Convert the QuerySet to a List
    list_of_dicts = list(qs)

    # Convert List of Dicts to JSON
    data = json.dumps(list_of_dicts, cls=DjangoJSONEncoder)
    return HttpResponse(data, content_type="application/json")


# def greenhabit_light(request):
#     greenhabit_entries = greenhabitPage.objects.all()
#     # page = request.GET.get('page', 1)
#
#     # Pagination
#     # paginator = Paginator(greenhabit_entries, 10)
#     # try:
#     #     search_results = paginator.page(page)
#     # except PageNotAnInteger:
#     #     search_results = paginator.page(1)
#     # except EmptyPage:
#     #     search_results = paginator.page(paginator.num_pages)
#     #
#     # print('habit entries', greenhabit_entries)
#     return render(request, 'greenhabit/greenhabit_index_page_public.html', {
#         'habit_entries': greenhabit_entries,
#     })
#
#
def search(request):
    search_query = request.GET.get('query', None)
    page = request.GET.get('page', 1)

    # Search
    if search_query:
        search_results = Page.objects.live().search(search_query)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
        })
