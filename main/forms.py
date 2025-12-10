from django import forms
from django.core.validators import RegexValidator, ValidationError
from datetime import date, datetime, timedelta
import re
from django.utils import timezone
from .models import Zayvka
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

class ZayvkaForm(forms.ModelForm):
    class Meta:
        model = Zayvka
        fields = '__all__'
        exclude = ['status', 'created_at']
        
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'initiative_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'initiative_time': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': '12:00 - 13:00'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов Иван Иванович'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.ru'}),
            'vk_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'https://vk.com/id12345'}),
            'workplace': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ИТ-центр "БАЗА"'}),
            'initiative_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш ответ'}),
            'initiative_goal': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ваш ответ'}),
            'initiative_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '3-5 предложений о том, в чем суть Вашей идеи'}),
            'other_format_details': forms.Textarea(attrs={'class': 'form-control'}),
            'technical_equipment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Укажите, какое техническое оснащение Вам необходимо для проведения инициативы'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Если есть дополнительные уточнения или пожелания к инициативной заявке - просьба указать информацию здесь :)'}),
            'initiative_format': forms.Select(attrs={'class': 'form-control'}),
            'expected_participants': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'personal_data_agreement': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        # Удаляем все нецифровые символы кроме плюса в начале
        cleaned_phone = re.sub(r'[^\d+]', '', phone)
        
        # Проверяем длину (12 символов для формата +79999999999)
        if len(cleaned_phone) != 12:
            raise ValidationError('Номер телефона должен содержать 11 цифр после +7 (всего 12 символов)')
        
        return phone
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        
        if not birth_date:
            return birth_date
        
        today = date.today()
        
        # Рассчитываем возраст точно
        age = today.year - birth_date.year
        
        # Если день рождения еще не наступил в этом году, уменьшаем возраст на 1
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        
        # Проверяем возраст от 14 до 35 лет
        if age < 14:
            raise ValidationError('Возраст должен быть не менее 14 лет')
        
        if age > 35:
            raise ValidationError('Возраст должен быть не более 35 лет')
        
        return birth_date
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if email:
            # Простая проверка формата email (дополнительно к встроенной проверке Django)
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                raise ValidationError('Введите корректный email адрес')
        
        return email
    
    def clean_initiative_date(self):
        initiative_date = self.cleaned_data.get('initiative_date')
        
        if not initiative_date:
            return initiative_date
        
        today = date.today()
        
        # Проверяем, что дата инициативы не в прошлом
        if initiative_date < today:
            raise ValidationError('Дата проведения инициативы не может быть в прошлом')
        
        return initiative_date
    
    def clean_personal_data_agreement(self):
        agreement = self.cleaned_data.get('personal_data_agreement')
        
        # Проверяем, что чекбокс отмечен
        if not agreement:
            raise ValidationError('Необходимо дать согласие на обработку персональных данных')
        
        return agreement