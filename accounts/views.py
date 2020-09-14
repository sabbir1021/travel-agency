from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import  UserRegistrationForm , UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib.auth.decorators import login_required




def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
        # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
            user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request,
            'authenticate/register.html',
            {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
    'authenticate/register.html',
    {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
        data=request.POST)
        profile_form = ProfileEditForm(
        instance=request.user.profile,
        data=request.POST,
        files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
    'authenticate/edit.html',
    {'user_form': user_form,
    'profile_form': profile_form})

def profile(request):
    return render(request , "authenticate/profile.html")