from django import forms
from django.contrib.auth import get_user_model

from .models import UserProfile, User


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
            UserProfile.objects.create(email=user)
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    """Register Form based on email and password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        """Check passwords fields."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if not password1:
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
        if not email:
            raise forms.ValidationError("Fill email field.")
        if email_ex.exists():
            raise forms.ValidationError(f"{email} - this email is already taken.")
        if not email:
            raise forms.ValidationError("Fill email field.")
        return email

    def save(self, commit=True):
        """Save email and password as User."""
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.active = True
        if commit:
            user.save()
            UserProfile.objects.create(email=user)
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user']


User = get_user_model()
