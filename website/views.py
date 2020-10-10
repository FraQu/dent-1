from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView

from .decorators import active_required, login_required, customer_required, employee_required
from .forms import RegisterForm, LoginForm, CustomerForm, EmployeeForm, UserForm
from .models import Employee, User

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
            return redirect('dashboard')
        else:
            messages.info(request, 'email OR password is incorrect')
        return super(LoginView, self).form_invalid(form)


@login_required
@active_required
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


@login_required
@active_required
def dashboard(request):
    return render(request, 'website/dashboard.html',
                  {'section': 'dashboard'})


@login_required
@active_required
@employee_required
def employee_update_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        employee_form = EmployeeForm(request.POST, instance=request.user.employee)
        if user_form.is_valid() and employee_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            employee = employee_form.save(commit=False)
            employee.save()
            messages.success(request, f'Your account has been updated!')
            return redirect(reverse_lazy('staff_profile'))
    else:
        user_form = UserForm(instance=request.user)
        employee_form = EmployeeForm(instance=request.user.employee)

    context = {
        'user_form': user_form,
        'employee_form': employee_form
    }
    return render(request, 'website/staff_profile.html', context=context)


@login_required
@active_required
@customer_required
def customer_update_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        customer_form = CustomerForm(request.POST, instance=request.user.customer)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            employee = customer_form.save(commit=False)
            employee.save()
            messages.success(request, f'Your account has been updated!')
            return redirect(reverse_lazy('user_profile'))
    else:
        user_form = UserForm(instance=request.user)
        customer_form = CustomerForm(instance=request.user.customer)

    context = {
        'user_form': user_form,
        'customer_form': customer_form
    }
    return render(request, 'website/user_profile.html', context=context)


def our_team_view(request):
    users = User.objects.all().filter(is_staff=True)
    employee = Employee.objects.all()

    context = {
        "object_list": users,
        "employee": employee,
    }
    return render(request, 'website/our_team.html', context)
