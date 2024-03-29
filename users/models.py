from django.db import models
from django.contrib.auth.models import User
import uuid
# from django.db.models.signals import post_save, post_delete


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    email = models.CharField(max_length=256, null=True, blank=True)
    short_intro = models.CharField(max_length=256, null=True, blank=True)
    location = models.CharField(max_length=256, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile_pictures", default="profile_pictures/user-default.png", null=True, blank=True)
    social_github = models.CharField(max_length=256, null=True, blank=True)
    social_youtube = models.CharField(max_length=256, null=True, blank=True)
    social_twitter = models.CharField(max_length=256, null=True, blank=True)
    social_linkedin = models.CharField(max_length=256, null=True, blank=True)
    social_website = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    def __str__(self):
        return str(self.user.username)

    @property
    def profile_img_url(self):
        if self.profile_image:
            pass
        else:
            self.profile_image = "profile_pictures/user-default.png"
            self.save()
        
        return self.profile_image


    class Meta:
        ordering = ["created_at"]


class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    
    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    subject = models.CharField(max_length=256, null=True, blank=True)
    sender_name = models.CharField(max_length=256, null=True, blank=True)
    sender_email = models.EmailField(null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = [
            'is_read',
            '-created_at',
        ]
