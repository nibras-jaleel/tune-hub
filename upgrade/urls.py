from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .models import Vehicle, Upgrade, SimulationResult, Profile


urlpatterns = [
    path('', views.home, name='home'),

    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),

    # App
    path('vehicles/', views.vehicles, name='vehicles'),
    path('tune/', views.tune, name='tune'),
    path('tune/results/<int:result_id>/', views.tune_results, name='tune_results'),
    path("user_dashboard/", views.user_dashboard, name="user_dashboard"),
    path("add-vehicle/", views.add_vehicle_view, name="add_vehicle"),
    path('accounts/profile/', views.profile, name='profile'),  

    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),

    
]
