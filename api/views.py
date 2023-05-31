from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectsSerializer
from testapp.models import Projects, Reviews, Tags


@api_view(["GET"])
def get_routes(request):
    routes = [
        {"GET": "/api/projects"},
        {"GET": "api/projects/id"},
        {"POST": "api/projects/id/vote"},

        {"POST": "api/users/token"},
        {"POST": "api/users/token/refresh"},
    ]
    return Response(routes)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_projects(request):
    projects = Projects.objects.all()
    serialized = ProjectsSerializer(instance=projects, many=True)
    return Response(serialized.data)


@api_view(["GET"])
def get_project(request, pk):
    project = Projects.objects.get(id=pk)
    serialized = ProjectsSerializer(instance=project, many=False)
    return Response(serialized.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def project_vote(request, pk):
    project = Projects.objects.get(id=pk)
    user_profile = request.user.profile
    review, created = Reviews.objects.get_or_create(
        owner=user_profile,
        project=project
    )
    review.value = request.data["value"]
    review.body = request.data["body"]
    review.save()

    project.get_vote_count

    serialized = ProjectsSerializer(instance=project, many=False)
    return Response(serialized.data)


@api_view(["DELETE"])
def remove_tags_view(request):
    tag_id = request.data.get("tag")
    project_id = request.data.get("project")

    project = Projects.objects.get(id=project_id)
    tag = Tags.objects.get(id=tag_id)

    project.tags.remove(tag)

    return Response('Tag was deleted')