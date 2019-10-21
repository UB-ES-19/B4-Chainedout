from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Education, Experience


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
        fields = ['phone', 'website', 'location', ]
        labels = ['Telephone Number', 'Website', 'Location', ]


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
