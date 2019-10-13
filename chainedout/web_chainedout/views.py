from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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