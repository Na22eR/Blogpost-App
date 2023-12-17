from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView

from blog.views import paginator_interval
from .models import User
from blog.models import Post

from account.templates.forms import RegisterUserForm, UserUpdateForm, ProfileUpdateForm


def home(request):
    if request.user.is_authenticated:
        return redirect('blog-home')
    else:
        return redirect('account-login')


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


@login_required()
def account(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile information changed!")
            return redirect('account-account')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'account.html', context)


class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'profile.html'

    def get(self, request, user_id, *args, **kwargs):
        page_num = request.GET.get('page', 1)
        passed_user = User.objects.get(pk=user_id)

        posts = Post.objects.filter(author=passed_user).order_by('-date_posted')

        paginator = Paginator(posts, per_page=paginator_interval)
        page = paginator.get_page(page_num)

        return render(
            request=request,
            template_name=self.template_name,
            context={
                'page': page,
                'user_object': passed_user,
                'user_total': Post.objects.filter(author=passed_user).count(),
                'user_last_post': Post.objects.filter(author=passed_user).order_by('-date_posted').first(),
                     }
        )


@login_required()
def profile(request, user_id):

    passed_user = User.objects.get(pk=user_id)

    context = {
        'user_object': passed_user,
        'user_posts': Post.objects.filter(author=passed_user).order_by('-date_posted')
    }

    return render(request, 'profile.html', context)
