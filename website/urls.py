from django.urls import path
from website.views import RegisterView, LoginView
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('contact/', views.contact, name='contact'),
    path('appointment/', views.appointment, name='appointment'),
    path('user_profile/', views.user_profile, name='user_profile'),
]
