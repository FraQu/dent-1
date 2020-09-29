from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


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


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base user suitable for use in Oscar projects.
    This is basically a copy of the core AbstractUser model but without a
    username field
    """
    email = models.EmailField(_('Email'), unique=True)
    full_name = models.CharField(_('Full name'), max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(_('Staff status'), default=False)
    is_active = models.BooleanField(_('Active'))
    date_joined = models.DateTimeField(_('Date Joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        abstract = True
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.full_name


class User(AbstractUser):
    """Custom User model based on Django User model."""
    email = models.EmailField(max_length=255, unique=True)
    is_customer = models.BooleanField(default=False, null=True, blank=True)
    is_employee = models.BooleanField(default=False, null=True, blank=True)
    is_nurse = models.BooleanField(default=False, null=True, blank=True)
    is_doctor = models.BooleanField(default=False, null=True, blank=True)
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
