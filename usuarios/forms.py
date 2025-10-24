from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Objetivo, PerfilUsuario, Progreso


class PerfilUsuarioForm(forms.ModelForm):
    """Permite editar los datos personales del usuario."""

    class Meta:
        model = PerfilUsuario
        fields = ["edad", "peso", "altura", "nivel", "dias_entrenamiento"]
        widgets = {
            "edad": forms.NumberInput(attrs={"min": 0, "max": 120}),
            "peso": forms.NumberInput(attrs={"step": "0.1", "min": 0}),
            "altura": forms.NumberInput(attrs={"step": "0.01", "min": 0}),
            "nivel": forms.Select(),
            "dias_entrenamiento": forms.NumberInput(attrs={"min": 1, "max": 7}),
        }

    def clean_edad(self):
        edad = self.cleaned_data.get("edad")
        if edad is not None and not 0 <= edad <= 120:
            raise ValidationError("La edad debe estar entre 0 y 120 años.")
        return edad

    def clean_altura(self):
        altura = self.cleaned_data.get("altura")
        if altura is not None and altura <= 0:
            raise ValidationError("La altura debe ser un número positivo.")
        return altura

    def clean_peso(self):
        peso = self.cleaned_data.get("peso")
        if peso is not None and peso <= 0:
            raise ValidationError("El peso debe ser un número positivo.")
        return peso

    def clean_dias_entrenamiento(self):
        dias = self.cleaned_data.get("dias_entrenamiento")
        if dias is not None and not 1 <= dias <= 7:
            raise ValidationError("Los días de entrenamiento deben estar entre 1 y 7.")
        return dias


class ObjetivoForm(forms.ModelForm):
    """Gestiona el objetivo principal del usuario."""

    class Meta:
        model = Objetivo
        fields = ["tipo", "peso_deseado", "dias_entrenamiento"]
        widgets = {
            "tipo": forms.TextInput(attrs={"placeholder": "Ej: Tonificar"}),
            "peso_deseado": forms.NumberInput(attrs={"step": "0.1", "min": 0}),
            "dias_entrenamiento": forms.NumberInput(attrs={"min": 1, "max": 7}),
        }

    def clean_peso_deseado(self):
        peso = self.cleaned_data.get("peso_deseado")
        if peso is not None and peso <= 0:
            raise ValidationError("Indicá un peso deseado positivo.")
        return peso

    def clean_dias_entrenamiento(self):
        dias = self.cleaned_data.get("dias_entrenamiento")
        if dias is not None and not 1 <= dias <= 7:
            raise ValidationError("Los días de entrenamiento deben estar entre 1 y 7.")
        return dias


class ProgresoForm(forms.ModelForm):
    """Registro de fotos y métricas de progreso."""

    class Meta:
        model = Progreso
        fields = ["fecha", "imagen", "peso_actual", "horas"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date", "class": "form-input"}),
            "peso_actual": forms.NumberInput(
                attrs={"step": "0.1", "class": "form-input", "placeholder": "Peso actual (kg)"}
            ),
            "imagen": forms.ClearableFileInput(attrs={"class": "form-input"}),
            "horas": forms.NumberInput(attrs={"step": "0.25", "min": 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aunque el modelo permita valores en blanco, para la carga manual exigimos una imagen.
        self.fields["imagen"].required = True

    def clean_fecha(self):
        fecha = self.cleaned_data.get("fecha")
        if fecha and fecha > date.today():
            raise ValidationError("La fecha no puede ser futura.")
        return fecha

    def clean_peso_actual(self):
        peso = self.cleaned_data.get("peso_actual")
        if peso is not None and peso <= 0:
            raise ValidationError("Ingresá un peso mayor a cero.")
        return peso

    def clean_horas(self):
        horas = self.cleaned_data.get("horas")
        if horas is not None and horas < 0:
            raise ValidationError("Las horas deben ser cero o un valor positivo.")
        return horas


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
