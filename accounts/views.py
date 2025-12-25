# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}! Теперь войдите.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form, 'title': 'Регистрация'})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверный логин или пароль')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form, 'title': 'Вход'})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из аккаунта!')
    return redirect('login')