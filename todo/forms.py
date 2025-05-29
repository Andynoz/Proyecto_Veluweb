from django import forms
from .models import Cliente
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class ClienteForm(forms.ModelForm):
    telefono = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[
            RegexValidator(
                regex='^\d{10}$',
                message='El número de teléfono debe tener exactamente 10 dígitos.'
            )
        ],
        error_messages={
            'required': 'Este campo es obligatorio.',
            'min_length': 'Debe tener al menos 10 dígitos.',
            'max_length': 'Debe tener como máximo 10 dígitos.',
        },
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'correo', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'nombre': {'required': 'Este campo es obligatorio.'},
            'apellido': {'required': 'Este campo es obligatorio.'},
            'correo': {
                'required': 'Este campo es obligatorio.',
                'invalid': 'Ingrese un correo válido.',
            },
        }

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if Cliente.objects.filter(correo=correo).exists():
            raise ValidationError('Este correo ya está registrado.')
        return correo
