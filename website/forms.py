from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction

from .models import Customer, User


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 is None:
            raise forms.ValidationError("Fill first password field.")
        if password2 is None:
            raise forms.ValidationError("Fill second password field.")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    """Register Form based on email and password."""
    email = forms.EmailField(label='Email')

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        """Check passwords fields."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 == '':
            raise forms.ValidationError("Fill first password field.")
        if password2 is None:
            raise forms.ValidationError("Fill second password field.")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def clean_email(self):
        """Check email field."""
        email = self.cleaned_data.get('email')
        email_ex = User.objects.filter(email=email)
        if email is None:
            raise forms.ValidationError("Fill email field.")
        if email_ex.exists():
            raise forms.ValidationError(f"{email} - this email is already taken.")
        if not email:
            raise forms.ValidationError("Fill email field.")
        return email

    @transaction.atomic
    def save(self, commit=True):
        """Save email and password as User."""
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.active = True
        user.is_customer = True
        if commit:
            user.save()
            Customer.objects.create(email=user)
        return user


class CustomerForm(forms.ModelForm):
    full_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.TypedChoiceField(choices=Customer.gender_choice,
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    birth_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=9, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = ('full_name', 'gender', 'birth_date', 'phone', 'profile_pic',)
        exclude = ['user']


class EmployeeForm(forms.ModelForm):
    full_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = ('full_name', 'bio', 'profile_pic',)
        exclude = ['user']


User = get_user_model()
