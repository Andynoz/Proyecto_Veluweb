from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Cliente
from .forms import ClienteForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    clientes = Cliente.objects.all()
    return render(request, 'todo/home.html', {'clientes': clientes})

def agregar(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClienteForm()
    
    return render(request, 'todo/agregar.html', {'form': form})

def editar(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'todo/editar.html', {'form': form})

def eliminar(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('home')

def index(request):
    return render(request, 'todo/index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        correo = request.POST['correo']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.email == correo:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credenciales incorrectas')
    return render(request, 'todo/login.html')

def registro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        correo = request.POST['correo']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
        else:
            user = User.objects.create_user(username=username, email=correo, password=password)
            user.save()
            return redirect('login')
    return render(request, 'todo/registro.html')