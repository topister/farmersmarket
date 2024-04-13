from django.http import HttpResponse
from django.shortcuts import redirect, render
# from userauths.forms import SignUpForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.contrib.auth import logout
from userauths.models import User, Profile
from django.contrib.auth import get_user_model
# User = get_user_model()

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse, reverse_lazy

from userauths.forms import *
from core.permission import user_is_farmer 


def profile_edit(request, id):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile) 
        if form.is_valid():
            profile_save = form.save(commit=False)
            profile_save.user = request.user
            profile_save.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('core:dashboard')
    else:
        form = ProfileForm(instance=profile)
    context = {
         'form':form,
         'profile':profile,
     }
    return render(request, 'userauths/profile_edit.html', context)


def get_success_url(request):

    """
    Handle Success Url After LogIN

    """
    if 'next' in request.GET and request.GET['next'] != '':
        return request.GET['next']
    else:
        return reverse('core:index')



def farmer_registration(request):

    """
    Handle Farmer Registration

    """
    form = FarmerRegistrationForm(request.POST or None)
    if form.is_valid():
        form = form.save()
        return redirect('userauths:login')
    context={
        
            'form':form
        }
    return render(request,'account/farmer-registration.html',context)


def buyer_registration(request):

    """
    Handle Buyer Registration 

    """
    form = BuyerRegistrationForm(request.POST or None)
    if form.is_valid():
        form = form.save()
        return redirect('userauths:login')
    context={
        
            'form':form
        }

    return render(request,'account/buyer-registration.html',context)


@login_required(login_url=reverse_lazy('userauths:login'))
@user_is_farmer
def farmer_edit_profile(request, id=id):

    """
    Handle Farmer Profile Update Functionality

    """

    user = get_object_or_404(User, id=id)
    form = FarmerProfileEditForm(request.POST or None, instance=user)
    if form.is_valid():
        form = form.save()
        messages.success(request, 'Your Profile Was Successfully Updated!')
        return redirect(reverse("account:edit-profile", kwargs={
                                    'id': form.id
                                    }))
    context={
        
            'form':form
        }

    return render(request,'account/farmer-edit-profile.html',context)



def user_logIn(request):

    """
    Provides users to logIn

    """

    form = UserLoginForm(request.POST or None)
    

    if request.user.is_authenticated:
        return redirect('/')
    
    else:
        if request.method == 'POST':
            if form.is_valid():
                auth.login(request, form.get_user())
                return HttpResponseRedirect(get_success_url(request))
    context = {
        'form': form,
    }

    return render(request,'account/login.html',context)


def user_logOut(request):
    """
    Provide the ability to logout
    """
    auth.logout(request)
    messages.success(request, 'You are Successfully logged out')
    return redirect('userauths:login')