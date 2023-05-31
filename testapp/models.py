from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
import uuid
from users.models import Profile

# Create your models here.
# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

#     def __str__(self):
#         return f"{self.user.first_name} {self.user.last_name}"


class PhotoModel(models.Model):
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to="testapp/static/testapp/img/")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.image.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(
        max_length=256,
        validators=[MinLengthValidator(5, "Title should be greater than 5 characters")]
    )
    text = models.TextField()
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.title


class Projects(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=256, null=True, blank=True)
    source_link = models.CharField(max_length=256, null=True, blank=True)
    tags = models.ManyToManyField("Tags", blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-vote_ratio", "-vote_total", "title"]

    @property
    def featured_image_url(self):
        if self.featured_image:
            pass
        else:
            print("No featured image")
            self.featured_image = "default.jpg"
            self.save()
        
        return self.featured_image

    @property
    def get_vote_count(self):
        reviews = self.reviews_set.all()
        total_up_votes = reviews.filter(value="up").count()
        total_votes = reviews.count()
        self.vote_ratio = (total_up_votes / total_votes) * 100
        self.vote_total = total_votes
        self.save()

    @property
    def reviewers(self):
        query_set = self.reviews_set.all().values_list("owner__id", flat=True)
        return query_set


class Reviews(models.Model):
    VOTE_TYPE = (
        ("up", "Up vote"),
        ("down", "Down vote")
    )
    owner = models.ForeignKey(to=Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    body = models.TextField()
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.value

    class Meta:
        ordering = [
            "-created_at",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["owner", "project"],
                name="unique_review"
            )
        ]


class Tags(models.Model):
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.name
