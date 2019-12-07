from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView, UpdateView, ListView, CreateView, RedirectView
from django.template.defaultfilters import slugify
from django.db.models import Q

from .models import Follow, Profile, Education, Experience, Post, Comment
from .forms import RegisterForm, ModifyProfileForm, ModifyUserForm, ModifyBioForm, ModifySkillsForm, \
    ModifyAchievementForm, ModifyExperienceForm, ModifyEducationForm, PostCreateForm, CommentCreateForm, ModifyPostForm,\
    RequestOrganization



def index(request):
    return render(request, "index.html")


@login_required
def save_profile(request):
    if request.method == 'POST':
        if 'submit_bio' in request.POST:
            bio_form = ModifyBioForm(request.POST, instance=request.user.profile)
            if bio_form.is_valid():
                bio_form.save()
            skill_form = ModifySkillsForm(instance=request.user.profile)
            education_form = ModifyEducationForm(request.GET or None)
            experience_form = ModifyExperienceForm(request.GET or None)
            achievements_form = ModifyAchievementForm(instance=request.user.profile)
        elif 'submit_skill' in request.POST:
            skill_form = ModifySkillsForm(request.POST, instance=request.user.profile)
            if skill_form.is_valid():
                skill_form.save()
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
            bio_form = ModifyBioForm(instance=request.user.profile)
            skill_form = ModifySkillsForm(instance=request.user.profile)
            education_form = ModifyEducationForm(request.GET or None)
            achievements_form = ModifyAchievementForm(instance=request.user.profile)
        elif 'submit_achievements' in request.POST:
            achievements_form = ModifyAchievementForm(request.POST, instance=request.user.profile)
            if achievements_form.is_valid():
                achievements_form.save()
            bio_form = ModifyBioForm(instance=request.user.profile)
            skill_form = ModifySkillsForm(instance=request.user.profile)
            education_form = ModifyEducationForm(request.GET or None)
            experience_form = ModifyExperienceForm(request.GET or None)
    else:
        bio_form = ModifyBioForm(instance=request.user.profile)
        skill_form = ModifySkillsForm(instance=request.user.profile)
        education_form = ModifyEducationForm(request.GET or None)
        experience_form = ModifyExperienceForm(request.GET or None)
        achievements_form = ModifyAchievementForm(instance=request.user.profile)
    context = {'bio_form': bio_form, 'skill_form': skill_form, 'education_form': education_form,
               'experience_form': experience_form, 'achievements_form': achievements_form}
    return render(request, "user/profile.html", context)


def request_organization(request):
    if request.method == 'POST':
        organization_form = RequestOrganization(request.POST, instance=request.user.profile)
        if organization_form.is_valid():
            organization_form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        organization_form = RequestOrganization(instance=request.user.profile)
    return render(request, "registration/request.html", {'organization_form' : organization_form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse("organization_info"))
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def user_list(request):
    if 'q' in request.GET:
        if request.GET.get('q') == '':
            return HttpResponseRedirect(reverse("index"))
        print("test")
        # ToDo: add attribute to profile that merges both first & last names
        query = request.GET.get('q')
        profiles_result = Profile.objects.filter(user__first_name__contains=query) | Profile\
            .objects.filter(user__last_name__contains=query)
        usernames_result = [profile.user.username for profile in profiles_result]
        context = {
            'search': query,
            'users': User.objects.filter(username__in=usernames_result)
        }
        return render(request, 'user/list.html', context)
    else:
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


def post_info(request, year, month, day, slug, pk):
    post = get_object_or_404(Post, slug=slug, published__year=year, published__month=month, published__day=day, pk=pk)
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
    else:
        form = CommentCreateForm()
    comments = get_object_or_404(Post, pk=pk).comments.all()
    return render(request, 'posts/post_info.html', {'post': post, 'comments': comments, 'form': form})


class UpdateEducation(UpdateView):
    model = Education
    form_class = ModifyEducationForm
    template_name = 'user/update_education.html'
    success_url = '/profile'

    def get_context_data(self, **kwargs):
        context = super(UpdateEducation, self).get_context_data(**kwargs)
        context['form'] = ModifyEducationForm(
            instance=Education.objects.filter(profile=self.request.user.profile, pk=self.kwargs['pk']).first())
        return context

    def get_object(self):
        return Education.objects.filter(profile=self.request.user.profile, pk=self.kwargs['pk']).first()


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

    def get_context_data(self, **kwargs):
        context = super(UpdateExperience, self).get_context_data(**kwargs)
        context['form'] = ModifyExperienceForm(
            instance=Experience.objects.filter(profile=self.request.user.profile, pk=self.kwargs['pk']).first())
        return context

    def get_object(self):
        return Experience.objects.filter(profile=self.request.user.profile, pk=self.kwargs['pk']).first()


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
        return super(DeleteExperience, self).delete(request, *args, **kwargs)


class UpdateProfile(UpdateView):
    model = Profile
    form_class = ModifyUserForm
    second_form_class = ModifyProfileForm
    template_name = 'user/update_profile.html'
    success_url = '/profile'

    def get_context_data(self, **kwargs):
        context = super(UpdateProfile, self).get_context_data(**kwargs)
        context['form'] = ModifyUserForm(instance=self.request.user)
        context['form2'] = ModifyProfileForm(instance=Profile.objects.get(user=self.request.user))
        return context

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ModifyUserForm(request.POST, instance=self.object.user)
        form2 = ModifyProfileForm(request.POST, request.FILES, instance=Profile.objects.get(user=self.object.user))
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data())


class PostCreateView(CreateView):
    template_name = 'posts/post_list.html'
    model = Post
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super(PostCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        following = self.request.user.following.all()
        objects = Post.objects.all().filter(Q(status='posted', author__in=following) | Q(author=self.request.user))
        paginator = Paginator(objects, 5)
        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['page'] = page
        context['posts'] = posts
        return context

class DeletePost(SuccessMessageMixin, DeleteView):
    model = Post
    success_url = '/posts'
    success_message = "Removed Post"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        title = self.object.title
        request.session['title'] = title
        message = request.session['title'] + ' deleted successfully'
        messages.success(self.request, message)
        return super(DeletePost, self).delete(request, *args, **kwargs)


class UpdatePost(UpdateView):
    model = Post
    form_class = ModifyPostForm
    template_name = 'posts/update_post.html'
    success_url = '/posts'

    def get_context_data(self, **kwargs):
        context = super(UpdatePost, self).get_context_data(**kwargs)
        context['form'] = ModifyPostForm(
            instance=Post.objects.filter(author=self.request.user, pk=self.kwargs['pk']).first())
        return context

    def get_object(self):
        return Post.objects.filter(author=self.request.user, pk=self.kwargs['pk']).first()


class PostLike(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, slug=self.kwargs.get("slug"), pk=self.kwargs.get("pk"))
        user = self.request.user
        if user.is_authenticated and user != post.author:
            if user in post.likes.all():
                post.likes.remove(user)
            else:
                post.likes.add(user)
        return '/posts'