from django import forms
from django.contrib.auth.forms import AuthenticationForm, \
    UserCreationForm, UserChangeForm
from .models import User
from django.core.exceptions import ValidationError


class UserLoginForm(AuthenticationForm):
    # AuthenticationForm уже имеет нужные поля
    pass

class UserRegistrationForm(UserCreationForm):
    # Добавляем email как обязательное поле
    email = forms.EmailField(
        required=True,
        label='Email'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfileForm(UserChangeForm):
    password = None  # Скрыть поле пароля
    

    class Meta:
        model = User
        fields = (
            'image',
            'first_name',
            'last_name',
            'middle_name',
            'birthday', 
            'phone',
            'link_vk',
            'link_tg'
        )
        widgets = {
            'birthday': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control form-styleprofile'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control form-styleprofile',
                'placeholder': 'Ваше имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control form-styleprofile', 
                'placeholder': 'Ваша фамилия'
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control form-styleprofile',
                'placeholder': 'Ваше отчество'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control form-styleprofile',
                'placeholder': '+7(999) 999 99-99'
            }),
            'link_vk': forms.TextInput(attrs={
                'class': 'form-control form-styleprofile',
                'placeholder': 'https://vk.com/...'
            }),
            'link_tg': forms.TextInput(attrs={
                'class': 'form-control form-styleprofile',
                'placeholder': 't.me/....'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control form-styleimg mt-2'
            })
        }