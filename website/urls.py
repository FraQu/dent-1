from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views
from .decorators import login_required
from .views import (
    RegisterView, LoginView,SchedulerView
)

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('contact/', views.contact, name='contact'),
    path('appointment/', views.appointment, name='appointment'),
    path('user_profile/', views.customer_update_view, name='user_profile'),
    path('staff_profile/', views.employee_update_view, name='staff_profile'),
    path('our_team/', views.our_team_view, name='our_team'),
    path('dashboard', views.dashboard, name='dashboard'),

    path('password_change/done/',
         login_required(auth_views.PasswordChangeDoneView.as_view(
             template_name='registration/password_change_complete.html')), name='password_change_complete'),
    path('password_change/',
         login_required(auth_views.PasswordChangeView.as_view(
             success_url=reverse_lazy('password_change_complete'),
             template_name='registration/password_change.html')),
         name='password_change'),
    path('add_customer/', views.addcustomer, name='add_customer'),
    path('calendar/', SchedulerView.as_view(), name='calendar'),
    path('appointment/new/$', views.schedule_appointment, name='appointment_new'),
	path('event/edit/(?P<appointment_id>\d+)/$', views.schedule_appointment, name='event_edit'),
    path('services', views.services, name='services'),
    path('services_dashboard', views.services_dashboard, name='services_dashboard'),


]
