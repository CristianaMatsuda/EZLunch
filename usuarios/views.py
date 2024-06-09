from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import LoginForm, RegisterForm
from .singleton import UserAuthSingleton
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_auth = UserAuthSingleton()
            if user_auth.login_user(request, username, password):
                return redirect('pedidos:index')
            else:
                messages.error(request, "Usuário ou senha inválidos")
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'usuarios/logout.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('usuarios:login')
    else:
        form = RegisterForm()
    return render(request, 'usuarios/register.html', {'form': form})
