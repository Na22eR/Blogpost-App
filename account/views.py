from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from account.templates.forms import RegisterUserForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            '''username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)  
            login(request, user)'''
            messages.success(request, "Registered successfully")
            return redirect('account-login')
    else:
        form = RegisterUserForm()

    return render(request, 'register.html', {'form': form})


def home(request):
    if request.user.is_authenticated:
        return redirect('blog-home')
    else:
        return redirect('account-login')


@login_required()
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile information changed!")
            return redirect('account-profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)
