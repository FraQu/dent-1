from django.urls import path

from website.views import RegisterView, LoginView, UserProfileView, OurTeamView, StaffProfileView
from . import views
from .decorators import login_required

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('contact/', views.contact, name='contact'),
    path('appointment/', views.appointment, name='appointment'),
    path('user_profile/', login_required(UserProfileView.as_view()), name='user_profile'),
    path('staff_profile/', login_required(StaffProfileView.as_view()), name='staff_profile'),
    path('our_team/', OurTeamView.as_view(), name='our_team'),

]
