from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView, UpdateView, ListView, CreateView, RedirectView
from django.template.defaultfilters import slugify
from django.db.models import Q

from .models import Follow, Profile, Education, Experience, Post, Comment, Group, GroupPost, GroupInvite, PostImage, \
    PrivateMessage, GroupInviteRequest, Job
from .forms import RegisterForm, ModifyProfileForm, ModifyUserForm, ModifyBioForm, ModifySkillsForm, \
    ModifyAchievementForm, ModifyExperienceForm, ModifyEducationForm, PostCreateForm, CommentCreateForm, ModifyPostForm, \
    GroupCreateForm, ModifyGroupForm, GroupPostCreateForm, ModifyGroupPostForm, GroupCommentCreateForm, \
    GroupInviteCreateForm, ImageForm, ImageFormSet, PrivateMessageCreateForm, GroupInviteRequestCreateForm, RequestOrganization, ModifyJobsForm


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
            job_form = ModifyJobsForm(request.GET or None)
            achievements_form = ModifyAchievementForm(instance=request.user.profile)
        elif 'submit_skill' in request.POST:
            skill_form = ModifySkillsForm(request.POST, instance=request.user.profile)
            if skill_form.is_valid():
                skill_form.save()
            bio_form = ModifyBioForm(instance=request.user.profile)
            education_form = ModifyEducationForm(request.GET or None)
            experience_form = ModifyExperienceForm(request.GET or None)
            job_form = ModifyJobsForm(request.GET or None)
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
            job_form = ModifyJobsForm(request.GET or None)
            achievements_form = ModifyAchievementForm(instance=request.user.profile)
        elif 'submit_jobs' in request.POST:
            job_form = ModifyJobsForm(request.POST)
            if job_form.is_valid():
                job_type = job_form.cleaned_data.get('job_type')
                compan = job_form.cleaned_data.get('compan')
                location = job_form.cleaned_data.get('location')
                until = job_form.cleaned_data.get('until')
                jobs = Job(job_type=job_type, compan=compan, location=location, until=until)
                jobs.save()
                request.user.profile.job.add(jobs)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            bio_form = ModifyBioForm(instance=request.user.profile)
            skill_form = ModifySkillsForm(instance=request.user.profile)
            experience_form = ModifyExperienceForm(request.GET or None)
            education_form = ModifyEducationForm(request.GET or None)
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
            job_form = ModifyJobsForm(request.GET or None)
            achievements_form = ModifyAchievementForm(instance=request.user.profile)
        elif 'submit_achievements' in request.POST:
            achievements_form = ModifyAchievementForm(request.POST, instance=request.user.profile)
            if achievements_form.is_valid():
                achievements_form.save()
            bio_form = ModifyBioForm(instance=request.user.profile)
            skill_form = ModifySkillsForm(instance=request.user.profile)
            education_form = ModifyEducationForm(request.GET or None)
            job_form = ModifyJobsForm(request.GET or None)
            experience_form = ModifyExperienceForm(request.GET or None)
    else:
        bio_form = ModifyBioForm(instance=request.user.profile)
        skill_form = ModifySkillsForm(instance=request.user.profile)
        job_form = ModifyJobsForm(request.GET or None)
        education_form = ModifyEducationForm(request.GET or None)
        experience_form = ModifyExperienceForm(request.GET or None)
        achievements_form = ModifyAchievementForm(instance=request.user.profile)
    context = {'bio_form': bio_form, 'skill_form': skill_form, 'education_form': education_form,
               'experience_form': experience_form, 'achievements_form': achievements_form, 'job_form': job_form}
    return render(request, "user/profile.html", context)


def request_organization(request):
    if request.method == 'POST':
        organization_form = RequestOrganization(request.POST, instance=request.user.profile)
        if organization_form.is_valid():
            organization_form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        organization_form = RequestOrganization(instance=request.user.profile)
    return render(request, "registration/request.html", {'organization_form': organization_form})


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
def register_group(request):
    if request.method == 'POST':
        form = GroupCreateForm(request.POST)
        if form.is_valid():
            group = Group.objects.create(
                name=form.cleaned_data['name'],
                location=form.cleaned_data['location'],
                description=form.cleaned_data['description'],
                image=form.cleaned_data['image']
            )
            group.members.add(request.user)
            return HttpResponseRedirect(reverse("index"))
    else:
        form = GroupCreateForm()
    return render(request, 'registration/register-group.html', {'form': form})


@login_required
def group_profile(request, pk):
    group = get_object_or_404(Group, pk=pk)

    if request.method == 'POST':
        group_post_form = GroupPostCreateForm(request.POST, request.FILES)
        if group_post_form.is_valid():
            group_post = GroupPost.objects.create(
                author=request.user,
                group=group,
                body=group_post_form.cleaned_data['body'],
                image=group_post_form.cleaned_data['image']
            )
    else:
        group_post_form = GroupPostCreateForm()

    objects = GroupPost.objects.filter(group=group)
    paginator = Paginator(objects, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'groups/group_profile.html', {'user': request.user, 'group': group, 'posts': posts,
                                                         'group_post_form': group_post_form})


@login_required
def groups(request):
    groups = Group.objects.all()
    return render(request, 'groups/groups.html', {'groups': groups})


@login_required
def quit_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    group.members.remove(request.user)
    return redirect('groups')


@login_required
def user_list(request):
    if 'q' in request.GET:
        if request.GET.get('q') == '':
            return HttpResponseRedirect(reverse("index"))
        print("test")
        # ToDo: add attribute to profile that merges both first & last names
        query = request.GET.get('q')
        profiles_result = Profile.objects.filter((Q(user__first_name__contains=query) & Q(organization=False)) |
                                                 (Q(user__last_name__contains=query) & Q(organization=False)) |
                                                 Q(name_organization__contains=query) & Q(organization=True))
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
def group_user_list(request, group):
    group = get_object_or_404(Group, pk=group)
    users = group.members.all()
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


class UpdateJobs(UpdateView):
    model = Job
    form_class = ModifyJobsForm
    template_name = 'user/update_jobs.html'
    success_url = '/profile'

    def get_context_data(self, **kwargs):
        context = super(UpdateJobs, self).get_context_data(**kwargs)
        context['form'] = ModifyJobsForm(
            instance=Job.objects.filter(profile=self.request.user.profile, pk=self.kwargs['pk']).first())
        return context

    def get_object(self):
        return Job.objects.filter(profile=self.request.user.profile, pk=self.kwargs['pk']).first()


class DeleteJobs(SuccessMessageMixin, DeleteView):
    model = Job
    success_url = '/profile'
    success_message = "Removed Job"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        job_type = self.object.job_type
        request.session['job_type'] = job_type
        message = request.session['job_type'] + ' deleted successfully'
        messages.success(self.request, message)
        return super(DeleteJobs, self).delete(request, *args, **kwargs)

def group_post_info(request, group_pk, post_pk):
    group = get_object_or_404(Group, pk=group_pk)
    group_post = get_object_or_404(GroupPost, group=group, author=request.user, pk=post_pk)
    if request.method == 'POST' :
        form = GroupCommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = group_post
            comment.author = request.user
            comment.save()
    else:
        form = GroupCommentCreateForm()
    comments = get_object_or_404(GroupPost, pk=post_pk).comments.all()
    return render(request, 'groups/group_post_info.html', {'group': group, 'group_post': group_post,
                                                           'comments': comments, 'form': form})


def inbox(request):
    invites = request.user.invites_received.all()
    invite_requests = request.user.invite_requests_received.all()
    messages = request.user.messages_received.all()
    return render(request, 'user/inbox.html', {'invites': invites,
                                               'invite_requests': invite_requests, 'messages': messages})


def accept_invite(request, group_pk, invite_pk):
    group = get_object_or_404(Group, pk=group_pk)
    group.members.add(request.user)
    GroupInvite.objects.get(pk=invite_pk).delete()
    return redirect('inbox')


def decline_invite(request, group_pk, invite_pk):
    GroupInvite.objects.get(pk=invite_pk).delete()
    return redirect('inbox')


def accept_invite_request(request, group_pk, invite_pk):
    group = get_object_or_404(Group, pk=group_pk)
    invite = get_object_or_404(GroupInviteRequest, pk=invite_pk)
    group.members.add(invite.sender)
    GroupInviteRequest.objects.get(pk=invite_pk).delete()
    return redirect('inbox')


def decline_invite_request(request, group_pk, invite_pk):
    GroupInviteRequest.objects.get(pk=invite_pk).delete()
    return redirect('inbox')


class UpdateEducation(UpdateView):
    model = Education
    form_class = ModifyEducationForm
    template_name = 'user/update_education.html'
    success_url = '/profile'

    def get_context_data(self, **kwargs):
        context = super(UpdateEducation, self).get_context_data(**kwargs)
        context['form'] = ModifyEducationForm(
            instance=get_object_or_404(Education, profile=self.request.user.profile, pk=self.kwargs.get("pk")))
        return context

    def get_object(self):
        return get_object_or_404(Education, profile=self.request.user.profile, pk=self.kwargs.get("pk"))


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
            instance=get_object_or_404(Experience, profile=self.request.user.profile, pk=self.kwargs.get("pk")))
        return context

    def get_object(self):
        return get_object_or_404(Experience, profile=self.request.user.profile, pk=self.kwargs.get("pk"))


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

    def post(self, request, *args, **kwargs):
        formset = ImageFormSet(request.POST, request.FILES, queryset=PostImage.objects.none())
        post_form = PostCreateForm(request.POST)
        if post_form.is_valid() and formset.is_valid():
            post_form = post_form.save(commit=False)
            post_form.author = self.request.user
            post_form.slug = slugify(post_form.title)
            post_form.save()
            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    post_image = PostImage(post=post_form, image=image)
                    post_image.save()
        return redirect('post_list')

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
        context['formset'] = ImageFormSet(queryset=PostImage.objects.none())
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
            instance=get_object_or_404(Post, author=self.request.user, pk=self.kwargs.get("pk")))
        return context

    def get_object(self):
        return get_object_or_404(Post, author=self.request.user, pk=self.kwargs.get("pk"))


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


class UpdateGroup(UpdateView):
    model = Group
    form_class = ModifyGroupForm
    template_name = 'groups/update_group.html'
    success_url = '/groups'

    def get_context_data(self, **kwargs):
        context = super(UpdateGroup, self).get_context_data(**kwargs)
        context['form'] = ModifyGroupForm(instance=get_object_or_404(Group, pk=self.kwargs.get("pk")))
        return context

    def get_object(self):
        return get_object_or_404(Group, pk=self.kwargs.get("pk"))


class DeleteGroupPost(SuccessMessageMixin, DeleteView):
    model = GroupPost
    success_message = "Removed Group Post"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(DeleteGroupPost, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('group-profile', kwargs={'pk': self.kwargs.get("group_pk")})


class UpdateGroupPost(UpdateView):
    model = GroupPost
    form_class = ModifyGroupPostForm
    template_name = 'groups/update_group_post.html'

    def get_context_data(self, **kwargs):
        group = get_object_or_404(Group, pk=self.kwargs.get("group_pk"))
        context = super(UpdateGroupPost, self).get_context_data(**kwargs)
        context['form'] = ModifyGroupPostForm(
            instance=get_object_or_404(GroupPost, group=group,
                                       author=self.request.user, pk=self.kwargs.get("post_pk")))
        return context

    def get_object(self):
        group = get_object_or_404(Group, pk=self.kwargs.get("group_pk"))
        return get_object_or_404(GroupPost, group=group,
                                 author=self.request.user, pk=self.kwargs.get("post_pk"))

    def get_success_url(self):
        return reverse('group-profile', kwargs={'pk': self.kwargs.get("group_pk")})


class GroupPostLike(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        group = get_object_or_404(Group, pk=self.kwargs.get("group_pk"))
        group_post = get_object_or_404(GroupPost, group=group, pk=self.kwargs.get("post_pk"))
        user = self.request.user
        if user.is_authenticated:
            if user in group_post.likes.all():
                group_post.likes.remove(user)
            else:
                group_post.likes.add(user)
        return reverse('group-profile', kwargs={'pk': self.kwargs.get("group_pk")})


class GroupInviteCreateView(CreateView):
    template_name = 'groups/group_invite.html'
    model = GroupInvite
    form_class = GroupInviteCreateForm

    def form_valid(self, form):
        print('invite')
        form.instance.sender = self.request.user
        form.instance.group = get_object_or_404(Group, pk=self.kwargs.get("group_pk"))
        return super(GroupInviteCreateView, self).form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(GroupInviteCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["user"] = self.request.user
        form_kwargs["group_pk"] = self.kwargs.get("group_pk")
        return form_kwargs


class GroupInviteRequestCreateView(CreateView):
    template_name = 'groups/group_invite_request.html'
    model = GroupInviteRequest
    form_class = GroupInviteRequestCreateForm

    def form_valid(self, form):
        print('invite_request')
        form.instance.sender = self.request.user
        form.instance.group = get_object_or_404(Group, pk=self.kwargs.get("group_pk"))
        return super(GroupInviteRequestCreateView, self).form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(GroupInviteRequestCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["user"] = self.request.user
        form_kwargs["group_pk"] = self.kwargs.get("group_pk")
        return form_kwargs


class PrivateMessageCreateView(CreateView):
    template_name = 'user/message.html'
    model = PrivateMessage
    form_class = PrivateMessageCreateForm

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.receiver = get_object_or_404(User, pk=self.kwargs.get("pk"))
        if 'image' in self.request.FILES:
            form.instance.image = self.request.FILES['image']
        return super(PrivateMessageCreateView, self).form_valid(form)

    def get_success_url(self):
        user = get_object_or_404(User, pk=self.kwargs.get("pk"))
        return reverse_lazy('user_info', args=[user.username])
