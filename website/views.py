from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, UpdateView, ListView

from .decorators import active_required, login_required, customer_required, employee_required
from .forms import RegisterForm, LoginForm, CustomerForm, EmployeeForm
from .models import Employee

email_contact = ['contact@dent.com']


def index(request):
    """Index page function."""

    return render(request, 'website/index.html')


class RegisterView(CreateView):
    """RegisterView."""

    form_class = RegisterForm
    success_url = '/login'
    template_name = 'registration/register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().get(request, *args, **kwargs)


class LoginView(FormView):
    """LoginView."""

    form_class = LoginForm
    success_url = '/'
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request or None
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        if user and password is not None:
            login(request, user, )
            return redirect('home')
        else:
            messages.info(request, 'email OR password is incorrect')
        return super(LoginView, self).form_invalid(form)


def logout_user(request):
    """Logout user function."""

    logout(request)
    return redirect('home')


def contact(request):
    """Contact sender function."""

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
    """Appointment sender function."""

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


@method_decorator([active_required, login_required, customer_required], name='dispatch')
class CustomerView(UpdateView):
    """CustomerView update."""
    form_class = CustomerForm
    template_name = 'website/user_profile.html'
    success_url = '/user_profile'

    def get_object(self, queryset=None):
        return self.request.user.customer


@method_decorator([active_required, login_required, employee_required], name='dispatch')
class EmployeeView(UpdateView):
    """EmployeeView update."""

    form_class = EmployeeForm
    template_name = 'website/staff_profile.html'
    success_url = '/staff_profile'

    def get_object(self, queryset=None):
        return self.request.user.employee


class OurTeamView(ListView):
    """OurTeamView List."""

    model = Employee
    template_name = 'website/our_team.html'
