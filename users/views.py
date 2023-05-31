from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Profile
from testapp.models import Projects
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, UpdateProfileForm, SkillForm, MessageForm
from .utils import search_profiles, paginate_profiles


# Create your views here.
def profiles(request):
    profiles, search_query = search_profiles(request)
    profiles, custom_range = paginate_profiles(request=request, profiles=profiles, results_per_page=4)

    ctx = {"profiles": profiles, "search_query": search_query, "custom_range": custom_range}
    return render(request, template_name="users/profiles.html", context=ctx)
    

def profile_view(request, pk):
    profile = Profile.objects.get(id=pk)
    projects = Projects.objects.filter(owner=profile)
    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description="")
    ctx = {"profile": profile, "projects": projects, "top_skills": top_skills, "other_skills": other_skills}
    return render(request, template_name="users/profile.html", context=ctx)


def user_login_view(request):
    page = "login"
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, message="User doesn't exists!")

        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, message="Logged in successfully!")
            return redirect(to=request.GET.get("next") if "next" in request.GET else "account")
        else:
            messages.error(request, message="Invalid username/password. Retry!")

    return render(request, template_name="users/login-register.html")


@login_required(login_url="login")
def user_logout_view(request):
    logout(request)
    messages.success(request, message="Logged out successfully!")
    return redirect(to="login")


def user_registration_view(request):
    page = "register"
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, message="Registered successfully!")
            login(request, user)
            return redirect(to="account")
        else:
            messages.error(request, message="Something went wrong!")

    ctx = {"form": form, "page": page}
    return render(request, template_name="users/login-register.html", context=ctx)


@login_required(login_url="login")
def user_account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    ctx = {"profile": profile, "skills": skills}
    return render(request, template_name="users/user-account.html", context=ctx)


@login_required(login_url="login")
def user_account_update(request):
    profile = request.user.profile
    form = UpdateProfileForm(instance=profile)

    if request.method == "POST":
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, message="Profile updated successfully!")
            return redirect(to="account")
            
    ctx = {"form": form}
    return render(request, template_name="users/edit-account-form.html", context=ctx)


@login_required(login_url="login")
def create_skill_view(request):
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():    
            skill = form.save(commit=False)
            skill.owner = request.user.profile
            skill.save()
            messages.success(request, message="Successfully added new skill!")
            return redirect(to="account")

    ctx = {"form": form}
    return render(request, template_name="users/skill-form.html", context=ctx)


@login_required(login_url="login")
def update_skill_view(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():    
            form.save()
            messages.success(request, message="Skill updated successfully!")
            return redirect(to="account")

    ctx = {"form": form}
    return render(request, template_name="users/skill-form.html", context=ctx)


@login_required(login_url="login")
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        messages.success(request, message=f"Skill({skill}) deleted!")
        return redirect(to="account")

    ctx = {"object": skill}
    return render(request, template_name="confirm-delete.html", context=ctx)


@login_required(login_url="login")
def inbox_view(request):
    profile = request.user.profile
    message_request = profile.messages.all()
    unread_message_count = message_request.filter(is_read=False).count()
    ctx = {"profile": profile, "message_request": message_request, "unread_message_count": unread_message_count}
    return render(request, template_name="users/inbox.html", context=ctx)


@login_required(login_url="login")
def message_detail_view(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    profile.profile_img_url
    if not message.is_read:
        message.is_read = True
        message.save()

    ctx = {"profile": profile, "message": message}
    return render(request, template_name="users/message.html", context=ctx)


def create_message_view(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = None
            message.recipient = recipient
            if request.user.is_authenticated:
                sender = request.user.profile
                message.sender = sender
                message.sender_name = sender.name
                message.sender_email = sender.email
            message.save()
            messages.success(request, message=f"Message sent to: {recipient.name}")
            return redirect("profile", recipient.id)

    ctx = {"form": form, "recipient": recipient}
    return render(request, template_name="users/send_message.html", context=ctx)
