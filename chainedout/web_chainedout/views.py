from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView, UpdateView

from .models import Follow, Profile, Education, Experience
from .forms import RegisterForm, ModifyProfileForm, ModifyUserForm, ModifyBioForm, ModifySkillsForm, \
    ModifyAchievementForm, ModifyExperienceForm, ModifyEducationForm


def index(request):
    return render(request, "index.html")


@login_required
def save_profile(request):
    if request.method == 'POST':
        if 'submit_user' in request.POST:
            user_form = ModifyUserForm(request.POST, instance=request.user)
            profile_form = ModifyProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
            bio_form = ModifyBioForm(instance=request.user.profile)
            skill_form = ModifySkillsForm(instance=request.user.profile)
            education_form = ModifyEducationForm(request.GET or None)
            experience_form = ModifyExperienceForm(request.GET or None)
            achievements_form = ModifyAchievementForm(instance=request.user.profile)
        elif 'submit_bio' in request.POST:
            bio_form = ModifyBioForm(request.POST, instance=request.user.profile)
            if bio_form.is_valid():
                bio_form.save()
            user_form = ModifyUserForm(instance=request.user)
            profile_form = ModifyProfileForm(instance=request.user.profile)
            skill_form = ModifySkillsForm(instance=request.user.profile)
            education_form = ModifyEducationForm(request.GET or None)
            experience_form = ModifyExperienceForm(request.GET or None)
            achievements_form = ModifyAchievementForm(instance=request.user.profile)
        elif 'submit_skill' in request.POST:
            skill_form = ModifySkillsForm(request.POST, instance=request.user.profile)
            if skill_form.is_valid():
                skill_form.save()
            user_form = ModifyUserForm(instance=request.user)
            profile_form = ModifyProfileForm(instance=request.user.profile)
            bio_form = ModifyBioForm(instance=request.user.profile)
            education_form = ModifyEducationForm(request.GET or None)
            experience_form = ModifyExperienceForm(request.GET or None)
            achievements_form = ModifyAchievementForm(instance=request.user.profile)
        elif 'submit_education' in request.POST:
            education_form = ModifyEducationForm(request.POST)
            if education_form.is_valid():
                entity = education_form.cleaned_data.get('entity')
                title = education_form.cleaned_data.get('title')
                edu_started = education_form.cleaned_data.get('edu_started')
                edu_finished = education_form.cleaned_data.get('edu_finished')
                education = Education(entity=entity, title=title, edu_started=edu_started, edu_finished=edu_finished)
                education.save()
                request.user.profile.educations.add(education)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            user_form = ModifyUserForm(instance=request.user)
            profile_form = ModifyProfileForm(instance=request.user.profile)
            bio_form = ModifyBioForm(instance=request.user.profile)
            skill_form = ModifySkillsForm(instance=request.user.profile)
            experience_form = ModifyExperienceForm(request.GET or None)
            achievements_form = ModifyAchievementForm(instance=request.user.profile)
        elif 'submit_experience' in request.POST:
            experience_form = ModifyExperienceForm(request.POST)
            if experience_form.is_valid():
                work_experience = experience_form.cleaned_data.get('work_experience')
                company = experience_form.cleaned_data.get('company')
                job = experience_form.cleaned_data.get('job')
                exp_started = experience_form.cleaned_data.get('exp_started')
                exp_finished = experience_form.cleaned_data.get('exp_finished')
                experience = Experience(work_experience=work_experience, company=company, job=job,
                                        exp_started=exp_started, exp_finished=exp_finished)
                experience.save()
                request.user.profile.experiences.add(experience)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            user_form = ModifyUserForm(instance=request.user)
            profile_form = ModifyProfileForm(instance=request.user.profile)
            bio_form = ModifyBioForm(instance=request.user.profile)
            skill_form = ModifySkillsForm(instance=request.user.profile)
            education_form = ModifyEducationForm(request.GET or None)
            achievements_form = ModifyAchievementForm(instance=request.user.profile)
        elif 'submit_achievements' in request.POST:
            achievements_form = ModifyAchievementForm(request.POST, instance=request.user.profile)
            if achievements_form.is_valid():
                achievements_form.save()
            user_form = ModifyUserForm(instance=request.user)
            profile_form = ModifyProfileForm(instance=request.user.profile)
            bio_form = ModifyBioForm(instance=request.user.profile)
            skill_form = ModifySkillsForm(instance=request.user.profile)
            education_form = ModifyEducationForm(request.GET or None)
            experience_form = ModifyExperienceForm(request.GET or None)
    else:
        user_form = ModifyUserForm(instance=request.user)
        profile_form = ModifyProfileForm(instance=request.user.profile)
        bio_form = ModifyBioForm(instance=request.user.profile)
        skill_form = ModifySkillsForm(instance=request.user.profile)
        education_form = ModifyEducationForm(request.GET or None)
        experience_form = ModifyExperienceForm(request.GET or None)
        achievements_form = ModifyAchievementForm(instance=request.user.profile)
    context = {'user_form': user_form, 'profile_form': profile_form, 'bio_form': bio_form, 'skill_form': skill_form,
               'education_form': education_form, 'experience_form': experience_form, 'achievements_form': achievements_form}
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
    if request.user == user:
        return redirect('saveprofile')
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


class UpdateEducation(UpdateView):
    model = Education
    form_class = ModifyEducationForm
    template_name = 'user/update_education.html'
    success_url = '/profile'


class DeleteEducation(SuccessMessageMixin, DeleteView):
    model = Education
    success_url = '/profile'
    success_message = "Removed Education"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        entity = self.object.entity
        request.session['entity'] = entity
        message = request.session['entity'] + ' deleted successfully'
        messages.success(self.request, message)
        return super(DeleteEducation, self).delete(request, *args, **kwargs)


class UpdateExperience(UpdateView):
    model = Experience
    form_class = ModifyExperienceForm
    template_name = 'user/update_experience.html'
    success_url = '/profile'


class DeleteExperience(SuccessMessageMixin, DeleteView):
    model = Experience
    success_url = '/profile'
    success_message = "Removed Experience"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        job = self.object.job
        request.session['job'] = job
        message = request.session['job'] + ' deleted successfully'
        messages.success(self.request, message)
        return super(DeleteEducation, self).delete(request, *args, **kwargs)
