from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Cliente
from .forms import ClienteForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import PasswordResetToken
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
import uuid

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
        return redirect('login')
    
    return render(request, 'todo/nueva_contrasena.html')