from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from .models import Follow, Profile
from .forms import RegisterForm, ModifyProfileForm, ModifyUserForm, ModifyBioForm, ModifySkillsForm, \
    ModifyAchievementForm, ModifyExperienceForm, ModifyEducationForm


def index(request):
    return render(request, "index.html")


@login_required
def save_profile(request):
    if request.method == 'POST':
        user_form = ModifyUserForm(request.POST, instance=request.user)
        profile_form = ModifyProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = ModifyUserForm()
        profile_form = ModifyProfileForm()
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, "user/profile.html", context)


@login_required()
def save_bio(request):
    if request.method == 'POST':
        bio_form = ModifyBioForm(request.POST, instance=request.user.profile)
        if bio_form.is_valid():
            bio_form.save()
    else:
        bio_form = ModifyBioForm()
    context = {'bio_form': bio_form}
    return render(request, "user/profile.html", context)


@login_required()
def save_skills(request):
    if request.method == 'POST':
        skill_form = ModifySkillsForm(request.POST, instance=request.user.profile)
        if skill_form.is_valid():
            skill_form.save()
    else:
        skill_form = ModifySkillsForm()
    context = {'skill_form': skill_form}
    return render(request, "user/profile.html", context)

@login_required()
def save_education(request):
    if request.method == 'POST':
        education_form = ModifyEducationForm(request.POST, instance=request.user.profile.education)
        if education_form.is_valid():
            education_form.save()
    else:
        education_form = ModifyEducationForm()
    context = {'education_form': education_form}
    return render(request, "user/profile.html", context)

@login_required()
def save_experience(request):
    if request.method == 'POST':
        experience_form = ModifyExperienceForm(request.POST, instance=request.user.profile.experience)
        if experience_form.is_valid():
            experience_form.save()
    else:
        experience_form = ModifyExperienceForm()
    context = {'experience_form': experience_form}
    return render(request, "user/profile.html", context)

@login_required()
def save_achievements(request):
    if request.method == 'POST':
        achievements_form = ModifyAchievementForm(request.POST, instance=request.user.profile)
        if achievements_form.is_valid():
            achievements_form.save()
    else:
        achievements_form = ModifyAchievementForm()
    context = {'achievements_form': achievements_form}
    return render(request, "user/profile.html", context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'user/list.html', {'section': 'people', 'users': users})


@login_required
def user_info(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'user/profile.html', {'section': 'people', 'user': user})


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Follow.objects.get_or_create(user_following=request.user, user_followed=user)
            else:
                Follow.objects.filter(user_following=request.user, user_followed=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})
