from django import forms
from .models import PerfilUsuario, Objetivo, Progreso
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



# Formulario de perfil de usuario
class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['edad', 'peso', 'altura']
        widgets = {
            'edad': forms.NumberInput(attrs={'min': 0}),
            'peso': forms.NumberInput(attrs={'step': '0.1'}),
            'altura': forms.NumberInput(attrs={'step': '0.01'}),
        }

# Formulario para configurar el objetivo
class ObjetivoForm(forms.ModelForm):
    class Meta:
        model = Objetivo
        fields = ['tipo', 'peso_deseado', 'dias_entrenamiento']
        widgets = {
            'tipo': forms.TextInput(attrs={'placeholder': 'Ej: Tonificar'}),
            'peso_deseado': forms.NumberInput(attrs={'step': '0.1'}),
            'dias_entrenamiento': forms.NumberInput(attrs={'min': 1, 'max': 7}),
        }

# Formulario de carga de progreso físico
class ProgresoForm(forms.ModelForm):
    class Meta:
        model = Progreso
        fields = ['fecha', 'imagen', 'peso_actual', 'horas']
        widgets = {
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),
            'peso_actual': forms.NumberInput(attrs={
                'step': '0.1',
                'class': 'form-input',
                'placeholder': 'Peso actual (kg)'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-input'
            }),
        }

# Formulario de registro personalizado
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
