from django import forms
from django.forms import ModelForm, widgets
from .models import Projects, Reviews
from django.contrib.auth.models import User


class UserProfileForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        cleaned_email = cleaned_data.get("email")
        cleaned_username = cleaned_data.get("username")

        if User.objects.filter(email=cleaned_email).exists():
            raise forms.ValidationError("Email already exists. Enter a different email")

        if User.objects.filter(username=cleaned_username).exists():
            raise forms.ValidationError("Username already taken. Try different username")

        return cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class PhotoUploadForm(forms.Form):
    image = forms.ImageField()


class ProjectsForm(ModelForm):
    class Meta:
        model = Projects
        fields = ["title", "description", "featured_image", "demo_link", "source_link"]

        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class ReviewForm(ModelForm):
    class Meta:
        model = Reviews
        fields = ["value", "body"]

        labels = {
            "value": "Place  your vote",
            "body": "Please add you comment",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
