from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users
from .forms import CreateUserForm

# Create your views here.
from .models import *


email_contact = ['contact@dent.com']


@unauthenticated_user
def register_page(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name=user.username,
                email=user.email,
            )
            messages.success(request, "Account was created for " + username)
            return redirect('login')
        else:
            messages.info(request, "Invalid data in field.")

    context = {'form': form}
    return render(request, 'website/register.html', context)


@unauthenticated_user
def login_page(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'website/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def index(request):
    return render(request, 'website/index.html')


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
