from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    """Custom user model manager without username and with unique email as identifier
    based on Django UserManager."""

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """Create and save User with email and password"""
        if not email:
            raise ValueError('Email is required.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save SuperUser with email and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    def create_staff_user(self, email, password, **extra_fields):
        """Create and save Staff User with email and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff user must have is_staff=True.')
        if extra_fields.get('is_superuser') is not False:
            raise ValueError('Staff user must have is_superuser=False.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model based on Django User model."""
    username = None
    email = models.EmailField(max_length=255, unique=True)
    is_customer = models.BooleanField(default=False, null=True, blank=True)
    is_employee = models.BooleanField(default=False, null=True, blank=True)
    is_nurse = models.BooleanField(default=False, null=True, blank=True)
    is_doctor = models.BooleanField(default=False, null=True, blank=True)
    full_name = models.CharField(_('Full name'), max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender_choice = (('-', '-',), ('M', 'Male'), ('F', 'Female'))
    gender = models.CharField(max_length=1, choices=gender_choice, default='-', blank=True)
    phone = models.CharField(max_length=9, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_email(self):
        return self.email


class Customer(models.Model):
    """Customer profile model - OneToOne User."""
    email = models.OneToOneField(User, related_name='customer', null=True, on_delete=models.CASCADE)
    updated_date = models.DateField(auto_now_add=True, null=True, blank=True)

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')


class Employee(models.Model):
    """Employee info model - OneToOne User."""
    email = models.OneToOneField(User, related_name='employee', null=True, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    updated_date = models.DateField(auto_now_add=True, null=True, blank=True)

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('employees')


class Appointment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    customer = models.ForeignKey(Customer, verbose_name='Customer', on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_doctor' : True})

    class Meta:
        verbose_name = _('Appointment')
        verbose_name_plural = _('Appointments')

    def check_override(self, fixed_start, fixed_end, new_start, new_end, fixed_doctor,
                      new_doctor, fixed_customer, new_customer):
        override = False
        if (new_start == fixed_end or new_end == fixed_start) \
                and (new_doctor != fixed_doctor) \
                and (new_customer != fixed_customer):
            override = False
        elif ((new_start >= fixed_start and new_start <= fixed_end)
              or (new_end >= fixed_start and new_end <= fixed_end)) \
                and (new_doctor == fixed_doctor) \
                and (new_customer == fixed_customer):
            override = True
        elif new_start <= fixed_start and new_end >= fixed_end \
                and (new_doctor == fixed_doctor) \
                and (new_customer == fixed_customer):
            override = True

        return override

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        if self.doctor.full_name is not None:
            doctor = self.doctor.full_name
        else:
            doctor = self.doctor

        return f'<a href="{url}"> Doc: {doctor} <br> Pat: {self.customer} {self.start_time.hour}:{self.start_time.minute} - ' \
            f'{self.end_time.hour}:{self.end_time.minute}</a>'


    def clean(self):
        if self.end_time <= self.start_time:
            raise ValueError('Ending time must be after start time')

        appointments = Appointment.objects.all()
        if appointments.exists():
            for appointment in appointments:
                if self.check_override(appointment.start_time, appointment.end_time,
                                      self.start_time,self.end_time, appointment.doctor,
                                      self.doctor, appointment.customer, self.customer):
                    raise ValidationError(
                        f'This appointment time or doctor is already in use. Choose another date schedule'
                        f' {str(appointment.start_time.hour)} {str(appointment.start_time.minute)} - '
                        f'{str(appointment.doctor)}')
