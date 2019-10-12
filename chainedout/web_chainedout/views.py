from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.forms.models import inlineformset_factory
from django.views.decorators.http import require_POST
from .models import Follow, ProfileForm

from .forms import RegisterForm

def index(request):
    return render(request, "index.html")

def testprofile(request):
    return render(request, "user/profile.html")

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
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})

@login_required
def edit_profile(request, pk):
    user = User.objects.get(pk=pk)
    user_form = ProfileForm(instance=User)
    ProfileInLineFormset = inlineformset_factory(User, ProfileForm, fields=('bio','location','birth_date','jobsIds','phone'))
    formset = ProfileInLineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = ProfileForm(request.POST, request.FILES, instance=user)
            formset = ProfileInLineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit = False)
                formset = ProfileInLineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('profile')

        return render(request, 'profile'), {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset
        }
    else:
        raise PermissionDenied
