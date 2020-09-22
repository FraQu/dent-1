from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import (
    RegisterView, LoginView, CustomerView, OurTeamView, EmployeeView
)

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('contact/', views.contact, name='contact'),
    path('appointment/', views.appointment, name='appointment'),
    path('user_profile/', CustomerView.as_view(), name='user_profile'),
    path('staff_profile/', EmployeeView.as_view(), name='staff_profile'),
    path('our_team/', OurTeamView.as_view(), name='our_team'),

    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_complete.html'),
         name='password_change_complete'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(success_url='done',
                                               template_name='registration/password_change.html'),
         name='password_change'),
]
