from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, UpdateView

from .forms import RegisterForm, LoginForm, UserProfileForm

email_contact = ['contact@dent.com']


def index(request):
    return render(request, 'website/index.html')


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = '/login'
    template_name = 'website/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().get(request, *args, **kwargs)


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'website/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request or None
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user,)
            return redirect('home')
        else:
            messages.info(request, 'email OR password is incorrect')
        return super(LoginView, self).form_invalid(form)


def logout_user(request):
    logout(request)
    return redirect('home')


def contact(request):

    if request.method == 'POST':
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']

        # Send Email
        send_mail(
            message_name,  # subject
            message,  # message
            message_email,  # from email
            email_contact,  # to email
        )

        return render(request, 'website/contact.html', {'message_name': message_name,
                                                        'message_email': message_email,
                                                        'message': message})
    else:
        return render(request, 'website/contact.html')


def appointment(request):

    if request.method == 'POST':
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message_phone = request.POST['message-phone']
        message_address = request.POST['message-address']
        message_date = request.POST['message-date']
        message_time = request.POST['message-time']
        message = request.POST['message']

        # Send Email
        appointment_topic = 'Name: ' + message_name + ' Phone: ' + message_phone + ' Email: ' + message_email + \
                            ' Address:' + message_address + ' Schedule: ' + message_date + ' ' + message_time + \
                            ' Message: ' + message

        send_mail(
            'Appointment request',  # subject
            appointment_topic,  # message
            message_email,  # from email
            email_contact  # to email
        )
        return render(request, 'website/appointment.html',
                      {'message_name': message_name,
                       'message_phone': message_phone,
                       'message_email': message_email,
                       'message_address': message_address,
                       'message_date': message_date,
                       'message_time': message_time,
                       'message': message,
                       })
    else:
        return render(request, 'website/appointment.html')


class UserProfileView(UpdateView):
    form_class = UserProfileForm
    template_name = 'website/user_profile.html'
    success_url = '/user_profile'

    def get_object(self, queryset=None):
        return self.request.user.profile
