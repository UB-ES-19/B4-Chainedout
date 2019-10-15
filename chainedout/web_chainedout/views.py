from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from .models import Follow, Profile
from .forms import RegisterForm, ModifyProfileForm, ModifyUserForm


def index(request):
    """
    user = request.user
    user.profile.profession = 'Profession Test'
    user.profile.bio = 'Bio Test'
    user.profile.location = 'Location Test'
    user.profile.education = 'Education Test'
    user.profile.skills = 'Skills Test'
    user.profile.achievements = 'Achievements Test'
    user.profile.experience = 'Experience Test'
    user.save()"""
    return render(request, "index.html")

@login_required
def testprofile(request):
    if request.method == 'POST':
        user_form = ModifyUserForm(request.POST, instance=request.user)
        profile_form = ModifyProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = ModifyUserForm()
        profile_form = ModifyProfileForm()
    return render(request, "user/profile.html", {'user_form': user_form, 'profile_form': profile_form})


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




