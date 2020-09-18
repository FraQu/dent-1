from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom user model manager without username and with unique email as identifier
    based on Django UserManager."""

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """Create and save User with email and password"""
        if not email:
            raise ValueError('Email is required.')
        if not password:
            raise ValueError("Password is required.")
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_email(self):
        return self.email


class Customer(models.Model):
    """User profile model."""
    username = None
    email = models.OneToOneField(User, related_name='customer', null=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    gender_choice = (('-', '---',), ('M', 'Male'), ('F', 'Female'))
    gender = models.CharField(max_length=1, choices=gender_choice, default='-', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=9, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)
    updated_date = models.DateField(auto_now_add=True, null=True, blank=True)
    objects = UserManager()

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = 'customer'
        verbose_name_plural = 'customers'


class Employee(models.Model):
    """Staff info model."""
    username = None
    email = models.OneToOneField(User, related_name='employee', null=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)
    updated_date = models.DateField(auto_now_add=True, null=True, blank=True)

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = 'employee'
        verbose_name_plural = 'employees'
