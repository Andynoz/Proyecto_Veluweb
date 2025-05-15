from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Cliente
from .forms import ClienteForm

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