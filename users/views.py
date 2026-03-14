from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserLoginForm, UserRegistrationForm, \
    ProfileForm
from main.models import Zayvka 
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,
                                     password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:new_list'))
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        print("=== ДЕБАГ РЕГИСТРАЦИИ ===")
        print("Данные формы:", request.POST)
        print("Форма валидна:", form.is_valid())
        
        if not form.is_valid():
            print("Ошибки формы:")
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
        
        if form.is_valid():
            user = form.save()
            print(f"Создан пользователь: {user.username}")
            print(f"Email пользователя: {user.email}")

            auth.login(request, user)
            
            messages.success(
                request, 
                f'{user.username}, регистрация прошла успешно!'
            )
            return HttpResponseRedirect(reverse('main:popular_list'))
        else:
            messages.error(request, 'Пожалуйста, проверьте введенные данные. \nУбедитесь, что: имя пользователя уникально, email корректен и не зарегистрирован ранее, \nпароль состоит минимум из 8 символов, не слишком простой и пароли совпадают.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/registration.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        print("=== ДЕБАГ ПРОФИЛЯ ===")
        print("POST данные:", request.POST)
        print("FILES данные:", request.FILES)
        form = ProfileForm(data=request.POST, instance=request.user,
                           files=request.FILES)
        if form.is_valid():
            user = form.save()
            print(f"Сохранен пользователь: {user.username}")
            print(f"Имя: {user.first_name}")
            print(f"Фамилия: {user.last_name}")
            print(f"Email: {user.email}")
            messages.success(request, 'Profile was changed')
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = ProfileForm(instance=request.user)
    
    zayvki = Zayvka.objects.filter(email=request.user.email).order_by('-id')
    return render(request, 'users/profile.html',
                  {'form': form,
                   'zayvki': zayvki}) 
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:popular_list'))
