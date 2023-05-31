from django.contrib import admin
from .models import PhotoModel, Article, Projects, Reviews, Tags
# Register your models here.

admin.site.register(PhotoModel)
# admin.site.register(UserProfile)
admin.site.register(Article)
admin.site.register(Projects)
admin.site.register(Reviews)
admin.site.register(Tags)
