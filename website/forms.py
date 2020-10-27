from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from .models import Customer, User, Employee, Appointment

UserModel = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """Custom Admin creation form."""

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."), }

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        """Check passwords fields function."""

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        """Save email and password as User Admin function."""

        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_customer = True
        user.is_employee = False
        if commit:
            user.save()
            Customer.objects.create(email=user)
        return user


class LoginForm(forms.Form):
    """Login form based on email and password."""

    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    """Register Form based on email and password."""
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."), }

    email = forms.EmailField(label='Email')

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        """Check passwords fields function."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(self.error_messages['password_mismatch'])
        return password2

    def clean_email(self):
        """Check email field function."""
        email = self.cleaned_data.get('email')
        email_ex = User.objects.filter(email=email)
        if not email:
            raise forms.ValidationError(_("Fill email field."))
        if email_ex.exists():
            raise forms.ValidationError(_(f"{email} - this email is already taken."))
        return email

    @transaction.atomic
    def save(self, commit=True):
        """Save email and password as User function."""
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.active = True
        user.is_customer = True
        user.is_employee = False
        if commit:
            user.save()
            Customer.objects.create(email=user)
        return user


gender_choice = (('M', 'Male'), ('F', 'Female'))


class CustomerForm(forms.ModelForm):
    """Customer form."""

    class Meta:
        model = Customer
        fields = ()
        exclude = ['user']


class UserForm(forms.ModelForm):
    """Custom User model based on Django User model."""
    full_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.TypedChoiceField(required=False, choices=gender_choice,
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    profile_pic = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('full_name', 'birth_date', 'phone', 'gender', 'profile_pic',)
        exclude = ['user']


class EmployeeForm(forms.ModelForm):
    """Employee form."""

    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Employee
        fields = ('bio',)
        exclude = ['user']


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ('title', 'description', 'start_time', 'end_time', 'customer', 'doctor')
