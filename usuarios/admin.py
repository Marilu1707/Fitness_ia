from django.contrib import admin
from .models import PerfilUsuario, Objetivo, Progreso, Profesional

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'edad', 'peso', 'altura', 'nivel', 'dias_entrenamiento')
    search_fields = ('usuario__username',)

@admin.register(Objetivo)
class ObjetivoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo')
    list_filter = ('tipo',)

@admin.register(Progreso)
class ProgresoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'fecha', 'peso_actual']
    list_filter = ('fecha',)
    readonly_fields = ('imagen',)

@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'especialidad', 'telefono', 'ubicacion')
    list_filter = ('tipo',)
    search_fields = ('nombre', 'especialidad')
