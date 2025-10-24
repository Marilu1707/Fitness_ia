"""Vistas principales del proyecto Fitness CRM con IA."""

from datetime import date
from io import BytesIO
from typing import Iterable, List

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.views.decorators.http import require_POST
from xhtml2pdf import pisa

from ia.generador import generar_rutina

from .forms import ObjetivoForm, PerfilUsuarioForm, ProgresoForm, RegistroForm
from .models import Objetivo, PerfilUsuario, Progreso, Profesional


def _calcular_estadisticas(progresos: Iterable[Progreso]) -> tuple[List[Progreso], float | None, float | None, float, float]:
    """Convierte el iterable en lista y calcula métricas básicas."""

    registros = list(progresos)
    pesos = [float(p.peso_actual) for p in registros if p.peso_actual is not None]
    peso_actual = pesos[-1] if pesos else None
    peso_inicial = pesos[0] if pesos else None
    diferencia = round(peso_actual - peso_inicial, 1) if peso_actual is not None and peso_inicial is not None else 0.0
    total_horas = round(sum(float(p.horas or 0) for p in registros), 2)
    return registros, peso_actual, peso_inicial, diferencia, total_horas


def registro(request):
    """Registra un nuevo usuario y crea su perfil básico."""

    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            PerfilUsuario.objects.create(
                usuario=usuario,
                edad=0,
                peso=0,
                altura=0,
                nivel="medio",
                dias_entrenamiento=3,
            )
            return redirect("login")
    else:
        form = RegistroForm()
    return render(request, "registro.html", {"form": form})


def home(request):
    """Pantalla pública e inicio rápido para usuarios autenticados."""

    contexto: dict = {}
    if request.user.is_authenticated:
        perfil = PerfilUsuario.objects.filter(usuario=request.user).first()
        if perfil:
            objetivo = Objetivo.objects.filter(usuario=request.user).last()
            historial, peso_actual, _, diferencia, total_horas = _calcular_estadisticas(
                Progreso.objects.filter(usuario=request.user).order_by("fecha")
            )
            rutina = generar_rutina(perfil, objetivo, historial) if objetivo else []
            contexto = {
                "objetivo": objetivo,
                "peso_actual": peso_actual,
                "diferencia": diferencia,
                "diferencia_abs": abs(diferencia),
                "total_horas": total_horas,
                "rutina": rutina,
            }
    return render(request, "index.html", contexto)


@login_required
def dashboard(request):
    """Panel principal con resumen de pesos, horas y última foto."""

    perfil = PerfilUsuario.objects.filter(usuario=request.user).first()
    if not perfil:
        return redirect("perfil")

    historial, peso_actual, _, diferencia, total_horas = _calcular_estadisticas(
        Progreso.objects.filter(usuario=request.user).order_by("fecha")
    )
    ultima_foto = next((p for p in reversed(historial) if p.imagen), None)

    objetivo_actual = Objetivo.objects.filter(usuario=request.user).last()
    rutina = generar_rutina(perfil, objetivo_actual, historial) if objetivo_actual else []

    return render(
        request,
        "usuarios/dashboard.html",
        {
            "perfil": perfil,
            "objetivo": objetivo_actual,
            "fotos": historial,
            "ultima_foto": ultima_foto,
            "rutina": rutina,
            "peso_actual": peso_actual,
            "diferencia": diferencia,
            "diferencia_abs": abs(diferencia),
            "total_horas": total_horas,
            "modo_edicion": False,
        },
    )


@login_required
def perfil(request):
    """Permite ver y editar los datos personales y el objetivo."""

    perfil, _ = PerfilUsuario.objects.get_or_create(
        usuario=request.user,
        defaults={
            "edad": 0,
            "peso": 0,
            "altura": 0,
            "nivel": "medio",
            "dias_entrenamiento": 3,
        },
    )

    objetivo = Objetivo.objects.filter(usuario=request.user).last()
    modo_edicion = request.GET.get("editar") == "1"

    if request.method == "POST":
        perfil_form = PerfilUsuarioForm(request.POST, instance=perfil)
        objetivo_form = ObjetivoForm(request.POST, instance=objetivo)
        if perfil_form.is_valid() and objetivo_form.is_valid():
            perfil_form.save()
            nuevo_objetivo = objetivo_form.save(commit=False)
            nuevo_objetivo.usuario = request.user
            nuevo_objetivo.save()
            return redirect("perfil")
    else:
        perfil_form = PerfilUsuarioForm(instance=perfil)
        objetivo_form = ObjetivoForm(instance=objetivo)

    historial, _, _, _, _ = _calcular_estadisticas(
        Progreso.objects.filter(usuario=request.user).order_by("fecha")
    )
    rutina = generar_rutina(perfil, objetivo, historial) if objetivo else []
    ultima_foto = next((p for p in reversed(historial) if p.imagen), None)

    return render(
        request,
        "usuarios/perfil.html",
        {
            "perfil_form": perfil_form,
            "objetivo_form": objetivo_form,
            "objetivo": objetivo,
            "perfil": perfil,
            "rutina": rutina,
            "ultima_foto": ultima_foto,
            "modo_edicion": modo_edicion,
        },
    )


@login_required
def rutina(request):
    """Muestra la rutina generada para el usuario."""

    perfil = get_object_or_404(PerfilUsuario, usuario=request.user)
    objetivo = Objetivo.objects.filter(usuario=request.user).last()
    if not objetivo:
        return render(request, "usuarios/rutina.html", {"rutina": [], "sin_objetivo": True})

    historial, _, _, _, _ = _calcular_estadisticas(
        Progreso.objects.filter(usuario=request.user).order_by("fecha")
    )
    rutina_generada = generar_rutina(perfil, objetivo, historial)

    return render(
        request,
        "usuarios/rutina.html",
        {"rutina": rutina_generada, "sin_objetivo": False},
    )


@login_required
def progreso(request):
    """Galería de fotos y estadísticas de avance."""

    progresos_con_imagen = (
        Progreso.objects.filter(usuario=request.user)
        .exclude(Q(imagen="") | Q(imagen__isnull=True))
        .order_by("-fecha")
    )
    historial, peso_actual, peso_inicial, diferencia, total_horas = _calcular_estadisticas(
        Progreso.objects.filter(usuario=request.user).order_by("fecha")
    )

    return render(
        request,
        "usuarios/progreso.html",
        {
            "progresos": progresos_con_imagen,
            "ultima_foto": progresos_con_imagen.first() if progresos_con_imagen.exists() else None,
            "peso_actual": peso_actual,
            "peso_inicial": peso_inicial,
            "diferencia": diferencia,
            "total_horas": total_horas,
        },
    )


@login_required
def subir_progreso(request):
    """Formulario para agregar una nueva foto y datos de progreso."""

    if request.method == "POST":
        form = ProgresoForm(request.POST, request.FILES)
        if form.is_valid():
            progreso = form.save(commit=False)
            progreso.usuario = request.user
            progreso.save()
            return redirect("progreso")
    else:
        form = ProgresoForm()
    return render(request, "usuarios/subir_progreso.html", {"form": form})


@login_required
def editar_objetivo(request):
    """Permite crear o modificar el objetivo del usuario."""

    objetivo = Objetivo.objects.filter(usuario=request.user).last()
    if request.method == "POST":
        form = ObjetivoForm(request.POST, instance=objetivo)
        if form.is_valid():
            objetivo = form.save(commit=False)
            objetivo.usuario = request.user
            objetivo.save()
            return redirect("dashboard")
    else:
        form = ObjetivoForm(instance=objetivo)
    return render(request, "usuarios/objetivo.html", {"form": form})


@login_required
def nutricionistas(request):
    """Lista de nutricionistas disponibles."""

    profesionales = Profesional.objects.filter(tipo="nutricionista")
    return render(request, "usuarios/nutricionistas.html", {"profesionales": profesionales})


@login_required
def entrenadores(request):
    """Listado de entrenadores personales."""

    profesionales = Profesional.objects.filter(tipo="entrenador")
    return render(request, "usuarios/entrenadores.html", {"profesionales": profesionales})


@login_required
def reporte_pdf(request):
    """Genera un PDF con el historial de progreso del usuario."""

    usuario = request.user
    perfil = PerfilUsuario.objects.filter(usuario=usuario).first()
    objetivo = Objetivo.objects.filter(usuario=usuario).last()
    historial, peso_actual, peso_inicial, diferencia, total_horas = _calcular_estadisticas(
        Progreso.objects.filter(usuario=usuario).order_by("fecha")
    )
    rutina = generar_rutina(perfil, objetivo, historial) if objetivo else []

    template = get_template("usuarios/reporte_pdf.html")
    html = template.render(
        {
            "usuario": usuario,
            "perfil": perfil,
            "objetivo": objetivo,
            "progresos": historial,
            "peso_actual": peso_actual,
            "peso_inicial": peso_inicial,
            "diferencia": diferencia,
            "total_horas": total_horas,
            "rutina": rutina,
        }
    )

    buffer = BytesIO()
    pisa_status = pisa.CreatePDF(src=html, dest=buffer, encoding="utf-8")
    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)

    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="reporte.pdf"'
    return response


@login_required
def editar_perfil(request):
    """Formulario para actualizar los datos del perfil."""

    perfil, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    if request.method == "POST":
        form = PerfilUsuarioForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect("perfil")
    else:
        form = PerfilUsuarioForm(instance=perfil)
    return render(request, "usuarios/editar_perfil.html", {"form": form})


@login_required
@require_POST
def agregar_horas(request):
    """Registra horas de entrenamiento de manera rápida."""

    horas = request.POST.get("horas")
    if horas:
        try:
            horas_float = float(horas)
        except (TypeError, ValueError):
            horas_float = 0
        if horas_float > 0:
            perfil = PerfilUsuario.objects.filter(usuario=request.user).first()
            peso_actual = float(perfil.peso) if perfil and perfil.peso is not None else None
            Progreso.objects.create(
                usuario=request.user,
                horas=horas_float,
                fecha=date.today(),
                peso_actual=peso_actual,
            )
    return redirect("dashboard")
