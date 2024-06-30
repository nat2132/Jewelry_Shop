from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_signup, name="signup"),
    path('admins/home/', views.admin_home, name="ahome"),
    path('users/home/', views.user_home, name="home"),
    path('signup/user/', views.user_signup, name='user_signup'),
    path('signup/admin/', views.admin_signup, name='admin_signup'),
    path('signin/user/', views.user_signin, name='user_signin'),
    path('signin/admin/', views.admin_signin, name='admin_signin'),
    path('signout/user/', views.user_signout, name='user_signout'),
    path('signout/admin/', views.admin_signout, name='admin_signout'),
    path('admins/activate/<uidb64>/<token>', views.admin_activate, name="admin_activate"),
    path('users/activate/<uidb64>/<token>', views.user_activate, name="user_activate"),
    path('users/password-reset/', views.user_password_reset, name='password_reset'),
    path('users/password-reset/<uidb64>/<token>/', views.user_password_recovery, name='password_recovery'),
    path('users/password-recovery/<str:uidb64>/<str:token>/', views.user_password_recovery, name='password_reset'),
    path('users/save_profile/', views.user_save_profile, name='user_save_profile'),
    path('admins/password-reset/', views.admin_password_reset, name='password_reset'),
    path('admins/password-reset/<uidb64>/<token>/', views.admin_password_recovery, name='password_recovery'),
    path('admins/password-recovery/<str:uidb64>/<str:token>/', views.admin_password_recovery, name='password_reset'),
    path('admins/save_profile/', views.admin_save_profile, name='admin_save_profile'),
]
