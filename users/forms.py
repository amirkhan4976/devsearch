from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message


class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class UpdateProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]

    def __init__(self, *args, **kwrgs):
        super().__init__(*args, **kwrgs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class SkillForm(forms.ModelForm):
    
    class Meta:
        model = Skill
        fields = "__all__"
        exclude = ["owner"]

    def __init__(self, *args, **kwrgs):
        super().__init__(*args, **kwrgs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ["sender_name", "sender_email", "subject", "body"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
