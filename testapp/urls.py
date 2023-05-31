from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# app_name = "testapp"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("restricted-page/", views.LoadPageLoggedInUserView.as_view(), name="restricted-page"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("upload-photo/", views.PhotoUploadView.as_view(), name="upload-photo"),
    path("delete-photo/", views.DeletePhotoView.as_view(), name="delete-photo"),
    path("photo-list-view/", views.PhotoListView.as_view(), name="photo-list-view"),
    path("list-all-article/", views.ArticleListView.as_view(), name="all"),
    path("create-article/", views.ArticleCreateView.as_view(), name="create-article"),
    path("update-article/<int:pk>", views.ArticleUpdateView.as_view(), name="update-article"),
    path("delete-article/<int:pk>", views.ArticleDeleteView.as_view(), name="delete-article"),
    path("detail-article/<int:pk>", views.ArticleDetailView.as_view(), name="detail-article"),
    path("projects/", views.ProjectsListView.as_view(), name="projects"),
    path("project-detail/<str:pk>/", views.ProjectDetailView.as_view(), name="project-detail"),
    path("project-form/", views.ProjectCreateView.as_view(), name="project-form"),
    path("project-update/<str:pk>/", views.ProjectUpdateView.as_view(), name="project-update"),
    path("delete-confirm/<str:pk>/", views.ProjectDeleteView.as_view(), name="delete-confirm"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
