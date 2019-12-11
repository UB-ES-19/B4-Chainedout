from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404
from django_summernote.widgets import SummernoteWidget

from .models import Profile, Education, Experience, Post, Comment, Group, GroupPost, GroupComment, GroupInvite, \
    PostImage, PrivateMessage


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class ModifyProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'website', 'location', 'image', ]
        labels = ['Telephone Number', 'Website', 'Location', 'Image', ]


class ModifyUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', ]
        labels = ['First Name', 'Last Name', 'E-mail', ]


class ModifyBioForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', ]
        labels = ['Bio', ]


class ModifySkillsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['skills', ]
        labels = ['Skills', ]


class ModifyAchievementForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['achievements', ]
        labels = ['Achievements', ]


class ModifyEducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['entity', 'title', 'edu_started', 'edu_finished']
        labels = ['Entity', 'Title', 'Started', 'Finished']


class ModifyExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['work_experience', 'company', 'exp_started', 'exp_finished', 'job']
        labels = ['Work_experience', 'Company', 'Started', 'Finished', 'Job']


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'status']
        labels = ['Title', 'Body', 'Status']
        widgets = {
            'body': SummernoteWidget(attrs={'summernote': {'height': '200px', 'width': '100%'}}),
        }


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = PostImage
        fields = ['image']


ImageFormSet = modelformset_factory(PostImage, form=ImageForm, extra=3)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['texto',]
        labels = ['Texto',]
        widgets = {
            'texto': SummernoteWidget(attrs={'summernote': {'height': '200px', 'width': '100%'}}),
        }


class ModifyPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'status']
        labels = ['Title', 'Body', 'Status']
        widgets = {
            'body': SummernoteWidget(attrs={'summernote': {'height': '200px', 'width': '100%'}}),
        }


class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'location', 'description', 'image']
        labels = ['Name', 'Location', 'Description', 'Image']
        widgets = {
            'body': SummernoteWidget(attrs={'summernote': {'height': '200px', 'width': '100%'}}),
        }


class ModifyGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'location', 'description', 'image']
        labels = ['Name', 'Location', 'Description', 'Image']
        widgets = {
            'body': SummernoteWidget(attrs={'summernote': {'height': '200px', 'width': '100%'}}),
        }


class GroupPostCreateForm(forms.ModelForm):
    class Meta:
        model = GroupPost
        fields = ['body', 'image']
        labels = {
            "body": "Create a new post",
            "image": "Attach an image"
        }
        widgets = {
            'body': SummernoteWidget(attrs={'summernote': {'height': '200px', 'width': '100%'}}),
        }


class ModifyGroupPostForm(forms.ModelForm):
    class Meta:
        model = GroupPost
        fields = ['body', 'image']
        labels = ['Body', 'Image']
        widgets = {
            'body': SummernoteWidget(attrs={'summernote': {'height': '200px', 'width': '100%'}}),
        }


class GroupCommentCreateForm(forms.ModelForm):
    class Meta:
        model = GroupComment
        fields = ['body']
        widgets = {
            'body': SummernoteWidget(attrs={'summernote': {'height': '200px', 'width': '100%'}}),
        }


class GroupInviteCreateForm(forms.ModelForm):
    class Meta:
        model = GroupInvite
        fields = ['text', 'receiver']
        labels = {
            "text": "Message",
        }

    receiver = forms.ModelChoiceField(queryset=User.objects.all(), initial=0)

    def __init__(self, *args, **kwargs):
        sender = kwargs.pop('user', None)
        group_pk = kwargs.pop('group_pk', None)
        group = get_object_or_404(Group, pk=group_pk)
        super(GroupInviteCreateForm, self).__init__(*args, **kwargs)

        if sender:
            self.fields['receiver'].queryset = sender.following.filter(~Q(user_groups__in=[group]))
            self.fields['receiver'].initial = 0
            self.fields['receiver'].label = 'User'


class PrivateMessageCreateForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['text', 'image']
        labels = {
            "text": "Message",
            "image": "Image"
        }

