from django import forms
from .models import Cliente
import re

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'correo', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'required': True, 'maxlength': 100, 'class': 'form-control'
            }),
            'apellido': forms.TextInput(attrs={
                'required': True, 'maxlength': 100, 'class': 'form-control'
            }),
            'correo': forms.EmailInput(attrs={
                'required': True, 'class': 'form-control'
            }),
            'telefono': forms.TextInput(attrs={
                'required': True, 'maxlength': 20, 'class': 'form-control'
            }),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if not re.match(r'^\d{10}$', telefono):
            raise forms.ValidationError("El teléfono debe tener exactamente 10 dígitos.")
        return telefono

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if Cliente.objects.filter(correo=correo).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return correo
