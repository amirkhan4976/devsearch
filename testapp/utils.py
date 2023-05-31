from django.db.models import Q
from .models import Projects, Tags
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def search_projects(request):
    search_query = ""
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    tags = Tags.objects.filter(
        name__icontains=search_query
    )

    projects = Projects.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(tags__in=tags)
    )

    return projects, search_query


def paginate_profiles(request, projects, results_per_page):

    page_number = request.GET.get("page")
    results_per_page = results_per_page

    # projects = sorted(projects, key=lambda x: x.title)
    paginator = Paginator(object_list=projects, per_page=results_per_page)
    try:
        projects = paginator.page(number=page_number)
    except PageNotAnInteger:
        page_number = 1
        projects = paginator.page(number=page_number)
    except EmptyPage:
        page_number = 1
        projects = paginator.page(number=page_number)

    left_index = int(page_number) - 4
    if left_index < 1:
        left_index = 1

    right_index = int(page_number) + 5
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return projects, custom_range
    