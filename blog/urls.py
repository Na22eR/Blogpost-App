from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from django.urls import path
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('load/', views.load_more_blog_posts, name='blog-load-more-bp'),
    path('load2/<int:user_id>', views.load_more_profile_posts, name='blog-load-more-pp'),
    path('about/', views.about, name='blog-about'),

    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/new', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]
