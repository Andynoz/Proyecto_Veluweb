from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm

def home(request):
    clientes = Cliente.objects.all()
    context = {'clientes': clientes}
    return render(request, 'todo/home.html', context)

def agregar(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClienteForm()
    context = {'form': form}
    return render(request, 'todo/agregar.html', context)

def eliminar(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    cliente.delete()
    return redirect('home')

def editar(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClienteForm(instance=cliente)
    context = {'form': form}
    return render(request, 'todo/editar.html', context)

def clientes(request):
    return render(request, 'todo/clientes.html')
