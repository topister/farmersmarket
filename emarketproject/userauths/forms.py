from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile
from django.contrib.auth import get_user_model
User = get_user_model()

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Type your username..."}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email Address"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):

    fullname = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"FullName"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Bio"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Phone"}))


    class Meta:
        model =  Profile
        fields = ['fullname', 'image', 'bio', 'phone']