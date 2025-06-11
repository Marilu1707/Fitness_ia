from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil/', views.perfil, name='perfil'),
    path('rutina/', views.rutina, name='rutina'),
    path('progreso/', views.progreso, name='progreso'),
    path('subir-progreso/', views.subir_progreso, name='subir_progreso'),
    path('editar-objetivo/', views.editar_objetivo, name='editar_objetivo'),
    path('nutricionistas/', views.nutricionistas, name='nutricionistas'),
    path('entrenadores/', views.entrenadores, name='entrenadores'),
    path('registro/', views.registro, name='registro'),
    path('reporte-pdf/', views.reporte_pdf, name='reporte_pdf'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('agregar-horas/', views.agregar_horas, name='agregar_horas'),
]
