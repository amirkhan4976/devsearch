from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.db import IntegrityError
from .forms import UserProfileForm, UserLoginForm, PhotoUploadForm, ProjectsForm, ReviewForm
# from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from . import models
from django.views import generic
from .owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .utils import search_projects, paginate_profiles


# Create your views here.
class HomePageView(View):
    def get(self, request):
        form = UserProfileForm()
        ctx = {"form": form}
        return render(request, template_name="testapp/home.html", context=ctx)

    def post(self, request):
        form = UserProfileForm(request.POST)
        if form.is_valid():
            pass1 = form.cleaned_data.get("password")
            pass2 = form.cleaned_data.get("confirm_password")
            if pass1 != pass2:
                ctx = {"form": form}
                return render(request, template_name="testapp/home.html", context=ctx)
            else:
                user = User.objects.create_user(
                    first_name=form.cleaned_data.get("first_name"),
                    last_name=form.cleaned_data.get("last_name"),
                    email=form.cleaned_data.get("email"),
                    username=form.cleaned_data.get("username"),
                    password=form.cleaned_data.get("password")
                )

                user_profile = models.UserProfile()
                user_profile.user = user
                user_profile.save()
                login(request, user)
                return redirect("upload-photo")

        ctx = {"form": form}
        return render(request, template_name="testapp/home.html", context=ctx)


class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        ctx = {"form": form}
        return render(request, template_name="registration/login.html", context=ctx)

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                ctx = {"user": user}
                if request.POST.get("next"):
                    return redirect(to=request.POST.get("next"))
                else:
                    return render(request, template_name="testapp/home.html", context=ctx)
            else:
                ctx = {"form": form}
                return render(request, template_name="registration/login.html", context=ctx)

        ctx = {"form": form}
        return render(request, template_name="registration/login.html", context=ctx)


class LoadPageLoggedInUserView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_name="testapp/loggedinneeded.html")


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect(to="login")


class PhotoUploadView(LoginRequiredMixin, View):

    def get(self, request):
        photos = models.PhotoModel.objects.filter(user__username=request.user)
        images = []
        for photo in photos:
            images.append(photo.title)

        ctx = {"images": images, "user": request.user, "img_folder": "testapp/img/"}
        return render(request, template_name="testapp/upload-photo.html", context=ctx)

    def post(self, request):
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = models.PhotoModel()
            photo.image = form.cleaned_data.get("image")
            photo.user = request.user
            photo.save()

            return redirect(to="upload-photo")

        ctx = {"form": form}
        return render(request, template_name="testapp/upload-photo.html", context=ctx)


class DeletePhotoView(LoginRequiredMixin, View):
    
    def post(self, request):
        return redirect(to="home")
        # models.PhotoModel.delete()


class PhotoListView(generic.ListView):
    model = models.PhotoModel
    template_name = "testapp/photo_view.html"


class ArticleListView(OwnerListView):
    model = models.Article
    template_name = "testapp/article_list.html"


class ArticleCreateView(OwnerCreateView):
    model = models.Article
    fields = ["title", "text"]
    template_name = "testapp/article_form.html"
    success_url = reverse_lazy("all")


class ArticleUpdateView(OwnerUpdateView):
    model = models.Article
    fields = ["title", "text"]
    template_name = "testapp/article_form.html"
    success_url = reverse_lazy("all")


class ArticleDeleteView(OwnerDeleteView):
    model = models.Article
    success_url = reverse_lazy("all")


class ArticleDetailView(OwnerDetailView):
    model = models.Article


class ProjectsListView(View):
    
    def get(self, request):
        projects, search_query = search_projects(request)

        projects, custom_range = paginate_profiles(request, projects, results_per_page=3)

        ctx = {"projects": projects, "search_query": search_query, "custom_range": custom_range}
        return render(request=request, template_name="testapp/projects-views.html", context=ctx)


class ProjectDetailView(View):

    def get(self, request, pk):
        project_obj = models.Projects.objects.get(id=pk)
        form = ReviewForm()
        ctx = {"project": project_obj, "form": form}
        return render(request, template_name="testapp/project-detail-view.html", context=ctx)

    def post(self, request, pk):
        project_obj = models.Projects.objects.get(id=pk)
        form = ReviewForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                review = form.save(commit=False)
                review.owner = request.user.profile
                review.project = project_obj
                try:
                    review.save()
                    project_obj.get_vote_count
                    messages.success(request, message="Review added successfully!")
                except IntegrityError:
                    messages.error(request, message="You have already reviewed this project.")
                    # return redirect()
                finally:
                    return redirect(to="project-detail", pk=project_obj.id)

            else:
                messages.error(request, message="Please login to add a comment")
                return redirect(to="login")


class ProjectCreateView(LoginRequiredMixin, View):

    def get(self, request):
        form = ProjectsForm()
        ctx = {"form": form}
        return render(request, template_name="testapp/project_form.html", context=ctx)

    def post(self, request):
        form = ProjectsForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            profile = models.Profile.objects.get(user=request.user)
            form.instance.owner = profile
            project = form.save()
            messages.success(request, message=f"Project({project}) added successfully!")
            return redirect(to="account")

        ctx = {"form": form}
        return render(request, template_name="testapp/project_form.html", context=ctx)


class ProjectUpdateView(LoginRequiredMixin, View):

    def get(self, request, pk):
        profile = request.user.profile
        project = profile.projects_set.get(id=pk)
        form = ProjectsForm(instance=project)
        ctx = {"form": form, "project": project}
        return render(request, template_name="testapp/project_form.html", context=ctx)

    def post(self, request, pk):
        project = models.Projects.objects.get(id=pk)
        form = ProjectsForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            tags = request.POST.get("new_tags").replace(",", " ").split()
            for tag in tags:
                tag, created = models.Tags.objects.get_or_create(name=tag)
                project.tags.add(tag)

            messages.success(request, message=f"Project({project}) updated successfully!")
            return redirect(to="account")

        ctx = {"form": form, "project": project}
        return render(request, template_name="testapp/project_form.html", context=ctx)


class ProjectDeleteView(LoginRequiredMixin, View):

    def get(self, request, pk):
        profile = request.user.profile
        project = profile.projects_set.get(id=pk)
        ctx = {"project": project}
        return render(request, template_name="confirm-delete.html", context=ctx)

    def post(self, request, pk):
        project = models.Projects.objects.get(id=pk)
        project.delete()
        messages.success(request, message=f"Project({project}) deleted successfully!")
        return redirect(to="account")
