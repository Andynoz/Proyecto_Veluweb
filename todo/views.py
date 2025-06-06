from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from .models import Cliente
from .forms import ClienteForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import PasswordResetToken
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
from django.db import IntegrityError
from django.contrib.auth.backends import ModelBackend



def home(request):
    return render(request, 'todo/home.html')  

def tabla(request):
    clientes = Cliente.objects.all()
    return render(request, 'todo/tabla.html', {'clientes': clientes})

def agregar(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tabla')
    else:
        form = ClienteForm()
    
    return render(request, 'todo/agregar.html', {'form': form})

def editar(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('tabla')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'todo/editar.html', {'form': form})

def eliminar(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('tabla')

def index(request):
    return render(request, 'todo/index.html')



def registro(request):  # Vista para registrar un nuevo usuario
    if request.method == 'GET':
        return render(request, 'todo/registro.html', {
            'form': UserCreationForm()
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                email = request.POST['email']
                user = User.objects.create_user(
                    username=email,
                    email=email,                    
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('signIn')
            except IntegrityError:
                return render(request, 'todo/registro.html', {
                    'form': UserCreationForm(),
                    'error': 'El usuario ya existe'
                })
        return render(request, 'todo/registro.html', {
                    'form': UserCreationForm(),
                    'error': 'Las contraseñas no coinciden'
        })

def signout(request): # Vista para cerrar sesión
    logout(request)
    return redirect('home')
    
    
def signIn(request): #Vista para iniciar sesión
    if request.method == 'GET':
        return render(request, 'todo/signIn.html', {
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(
            request, username=request.POST['email'],
            password=request.POST['password'])
        
        if user is None:
            return render(request, 'todo/signIn.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('index')
        
        
def enviar_codigo_reset(user):
    token = PasswordResetToken.objects.create(
        user=user,
        expires_at=timezone.now() + timedelta(minutes=10)
    )
    
    asunto = 'Código de recuperación de contraseña'
    mensaje = f'Hola {user.username}, tu código para restablecer tu contraseña es:\n\n{token.token}'
    remitente = 'andynox27v@gmail.com'
    destinatario = [user.email]
    
    send_mail(asunto, mensaje, remitente, destinatario)

def recuperacion(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        try:
            user = User.objects.get(email=correo)
            enviar_codigo_reset(user)
            messages.success(request, 'Se ha enviado un código de recuperación a tu correo.')
            return redirect('verificar_codigo')
        except User.DoesNotExist:
            messages.error(request, 'No se encontró una cuenta con ese correo.')
    return render(request, 'todo/recuperacion.html')

def recuperar_contrasena(request):
    return render(request, 'todo/recuperar_contrasena.html')

def correo_enviado(request):
    return render(request, 'todo/correo_enviado.html')

def confirmar_contrasena(request):
    return render(request, 'todo/confirmar_contrasena.html')

def contrasena_cambiada(request):
    return render(request, 'todo/contrasena_cambiada.html')

def verificar_codigo(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        try:
            token_obj = PasswordResetToken.objects.get(token=token)
            if token_obj.is_valid():
                request.session['reset_user_id'] = token_obj.user.id
                return redirect('nueva_contrasena')
            else:
                messages.error(request, 'El código ha expirado.')
        except PasswordResetToken.DoesNotExist:
            messages.error(request, 'Código inválido.')
    return render(request, 'todo/verificar_codigo.html')

def nueva_contrasena(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('recuperacion')

    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        nueva = request.POST.get('password')
        user.set_password(nueva)
        user.save()
        del request.session['reset_user_id']
        messages.success(request, 'Contraseña actualizada correctamente.')
        return redirect('signIn')
    
    return render(request, 'todo/nueva_contrasena.html')


def bienvenida(request):
    return render(request, 'bienvenida.html')