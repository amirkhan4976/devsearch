from django.urls import path

from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("login/", views.user_login_view, name="login"),
    path("logout/", views.user_logout_view, name="logout"),
    path("register/", views.user_registration_view, name="register"),
    
    path("", views.profiles, name="profiles"),
    path("profile/<str:pk>/", views.profile_view, name="profile"),
    path("user-account/", views.user_account, name="account"),
    path("update-account/", views.user_account_update, name="update-account"),

    path("create-skill/", views.create_skill_view, name="create-skill"),
    path("update-skill/<str:pk>/", views.update_skill_view, name="update-skill"),    
    path("delete-skill/<str:pk>/", views.delete_skill, name="delete-skill"),
    path("inbox/", views.inbox_view, name="inbox"),
    path("message-view/<str:pk>/", views.message_detail_view, name="message-view"),
    path("create-message/<str:pk>/", views.create_message_view, name="send-message"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
