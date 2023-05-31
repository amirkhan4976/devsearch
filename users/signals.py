from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings


def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            name=f"{user.first_name} {user.last_name}",
            email=user.email,   
        )
        send_mail(
            subject="Welcome to DevSearch",
            message="Happy that you are here",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[
                profile.email,
            ],
            fail_silently=False

        )


# def update_profile(sender, instance, created, **kwargs):
#     if not created:
#         user = instance
#         profile = Profile.objects.get(user=user)
#         profile.name = f"{user.first_name} {user.last_name}"
#         profile.email = user.email
#         profile.save()


def user_update(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        user.first_name = instance.name
        user.email = instance.email
        user.save()


def profile_delete(sender, instance, **kwargs):
    try:
        user_to_delete = User.objects.get(id=user.id)
        user_to_delete.delete()
    except Exception as e:
        print(e)
    

post_save.connect(create_profile, User)
# post_save.connect(update_profile, User)
post_save.connect(user_update, Profile)
post_delete.connect(profile_delete, Profile)
