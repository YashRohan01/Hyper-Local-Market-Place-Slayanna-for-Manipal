# users/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User

class LoginForm(AuthenticationForm):
    name_or_email = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Name / Email'
        })
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number'
        })

        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })

        # Reorder the fields
        ordered_fields = ['name_or_email', 'username', 'password']
        self.fields = {key: self.fields[key] for key in ordered_fields}



class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name' ,'phone_number','student_id', 'student_id_picture' ,'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})