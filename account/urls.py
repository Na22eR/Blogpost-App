from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='account-profile'),
    path('register/', views.register, name='account-register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='account-login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='account-logout'),

]