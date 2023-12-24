from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Post
from account.models import User


paginator_interval = 4

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'page'

    # load first set of posts on initial load of page
    def get(self, request, *args, **kwargs):
        page_num = request.GET.get('page', 1)

        posts = Post.objects.all().order_by('-date_posted')

        paginator = Paginator(posts, per_page=paginator_interval)
        page = paginator.get_page(page_num)

        # passing required information to html context
        return render(
            request=request,
            template_name=self.template_name,
            context={'page': page}
        )


@login_required()
def load_more_blog_posts(request):
    # receives the current page number and returns next set of posts
    if request.htmx:
        page_num = request.GET.get('page', 1)

        posts = Post.objects.all().order_by('-date_posted')

        page = Paginator(object_list=posts, per_page=paginator_interval).get_page(page_num)

        # does not return home.html but blog_pagination.html do handle pagination of homepage
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
    # receives the current page number and returns next set of posts
    if request.htmx:
        page_num = request.GET.get('page', 1)

        passed_user = User.objects.get(pk=user_id)
        posts = Post.objects.filter(author=passed_user).order_by('-date_posted')

        page = Paginator(object_list=posts, per_page=paginator_interval).get_page(page_num)

        # does not return profile.html but profile_pagination.html do handle pagination of user profiles
        return render(
            request=request,
            template_name='profile_pagination.html',
            context={
                'page': page,
                'user_object': passed_user,
            }
        )

    return render(request, 'profile_pagination.html')


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

    # checks if current user is the author of the post, if true delete is allowed
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required()
def about (request):
    return render(request, 'about.html')
