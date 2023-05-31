from django.db.models import Q
from .models import Profile, Skill
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def search_profiles(request):
    search_query = ""
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    skills = Skill.objects.filter(
        name__icontains=search_query
    )

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
    )

    return profiles, search_query


def paginate_profiles(request, profiles, results_per_page):

    page_number = request.GET.get("page")
    results_per_page = results_per_page

    paginator = Paginator(object_list=profiles, per_page=results_per_page)
    try:
        profiles = paginator.page(number=page_number)
    except PageNotAnInteger:
        page_number = 1
        profiles = paginator.page(number=page_number)
    except EmptyPage:
        page_number = 1
        profiles = paginator.page(number=page_number)

    left_index = int(page_number) - 4
    if left_index < 1:
        left_index = 1

    right_index = int(page_number) + 5
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return profiles, custom_range
    