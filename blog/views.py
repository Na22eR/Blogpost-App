from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .models import Post
from account.models import User

paginator_interval = 4

@login_required()
def home(request ):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'home.html', context)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'page'

    def get(self, request, *args, **kwargs):
        page_num = request.GET.get('page', 1)

        posts = Post.objects.all().order_by('-date_posted')

        paginator = Paginator(posts, per_page=paginator_interval)
        page = paginator.get_page(page_num)

        return render(
            request=request,
            template_name=self.template_name,
            context={'page': page}
        )


@login_required()
def load_more_blog_posts(request):
    if request.htmx:
        page_num = request.GET.get('page', 1)

        posts = Post.objects.all().order_by('-date_posted')

        page = Paginator(object_list=posts, per_page=paginator_interval).get_page(page_num)

        return render(
            request=request,
            template_name='blog_pagination.html',
            context={
                'page': page
            }
        )

    return render(request, 'blog_pagination.html')


@login_required()
def load_more_profile_posts(request, user_id):
    if request.htmx:
        page_num = request.GET.get('page', 1)

        passed_user = User.objects.get(pk=user_id)
        posts = Post.objects.filter(author=passed_user).order_by('-date_posted')

        page = Paginator(object_list=posts, per_page=paginator_interval).get_page(page_num)

        return render(
            request=request,
            template_name='blog_pagination.html',
            context={
                'page': page,
                'user_object': passed_user,
            }
        )

    return render(request, 'blog_pagination.html')


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'post_form.html'

    # fill in the current user as author before creating the post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # add is_create boolean to context to determine if it is an update or a post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = True
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'post_update.html'

    # fill in the current user as author before creating the post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # checks if current user is the author of the post, if true update is allowed
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/blog'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required()
def about (request):
    return render(request, 'about.html')
