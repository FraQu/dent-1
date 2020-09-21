from django.urls import path

from website.views import RegisterView, LoginView, CustomerView, OurTeamView, EmployeeView
from . import views

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

]
