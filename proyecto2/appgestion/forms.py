from django import forms
from .models import Vehiculo, VehiculoVendido


# Formulario para registrar una venta basado en el modelo VehiculoVendido en models.py
class VehiculoVendidoForm(forms.ModelForm):
    class Meta:
        model = VehiculoVendido
        fields = ['vehiculo', 'fecha_venta', 'precio_venta', 'comprador']
        # Aplica clases de Bootstrap (form-select, form-control) y tipos de entrada a los campos de la página HTML
        # 'required' significa que no pueden quedar en blanco
        widgets = {
            'vehiculo': forms.Select(attrs={
                'class': 'form-select',
                'required': True
                }),
            'fecha_venta': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'required': True
                }),
            'precio_venta': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': True
                }),
            'comprador': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True
                }),
        }

# Formulario para capturar los datos del cliente
# forms.Form para que Django no bloquee los RUT ya existentes
class ClienteForm(forms.Form):
    rut = forms.CharField(
        max_length=12, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ej: 12345678-9', 
            'required': True
        })
    )
    nombre = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'required': True
        })
    )
    apellidos = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'required': True
        })
    )

# Formulario para registrar solo los datos del vehículo basado en el modelo Vehiculo en models.py
class VehiculoBasicoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['marca', 'modelo', 'anio']
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'anio': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
        }