from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import ProfileView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<int:user_id>', ProfileView.as_view(), name='account-profile'),
    path('account/', views.account, name='account-account'),

    path('register/', views.register, name='account-register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='account-login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='account-logout'),

    path('reset/', PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('reset/done', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/complete', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

]
