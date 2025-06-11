from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import PerfilUsuario, Objetivo, Progreso, Profesional
from .forms import PerfilUsuarioForm, ObjetivoForm, ProgresoForm, RegistroForm
from ia.generador import generar_rutina
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from datetime import date
from django.db.models import Q

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
                nivel='medio',
                dias_entrenamiento=3
            )
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})




def index(request):
    """Pantalla de inicio pública y resumen si el usuario está logueado."""

    contexto = {}
    if request.user.is_authenticated:
        perfil = PerfilUsuario.objects.filter(usuario=request.user).first()
        if perfil:
            objetivo = Objetivo.objects.filter(usuario=request.user).last()
            progreso = Progreso.objects.filter(usuario=request.user).order_by('fecha')

            fotos = progreso.order_by('-fecha') if progreso.exists() else None
            peso_actual = progreso.last().peso_actual if progreso.exists() else None
            peso_inicial = progreso.first().peso_actual if progreso.exists() else None
            diferencia = round(peso_actual - peso_inicial, 1) if peso_actual and peso_inicial else 0
            diferencia_abs = abs(diferencia)
            total_horas = progreso.aggregate(Sum('horas'))['horas__sum'] or 0
            rutina = generar_rutina(perfil, objetivo) if objetivo else None

            contexto = {
                'objetivo': objetivo,
                'fotos': fotos,
                'peso_actual': peso_actual,
                'diferencia': diferencia,
                'diferencia_abs': diferencia_abs,
                'total_horas': total_horas,
                'rutina': rutina
            }

    return render(request, 'index.html', contexto)



@login_required
def dashboard(request):
    """Panel principal con resumen de pesos, horas y última foto."""

    perfil = PerfilUsuario.objects.filter(usuario=request.user).first()
    if not perfil:
        return redirect('perfil')

    objetivos = Objetivo.objects.filter(usuario=request.user)
    progresos = Progreso.objects.filter(usuario=request.user).order_by('fecha')

    pesos = [float(p.peso_actual) for p in progresos if p.peso_actual]
    peso_actual = pesos[-1] if pesos else 0
    peso_inicial = pesos[0] if pesos else 0
    diferencia = round(peso_actual - peso_inicial, 2) if pesos else 0
    diferencia_abs = abs(diferencia)

    total_horas = sum([p.horas for p in progresos if p.horas])
    ultima_foto = progresos.order_by('-fecha').first()
    rutina = generar_rutina(perfil, objetivos.last()) if objetivos else None
    modo_edicion = False

    return render(request, 'usuarios/dashboard.html', {
        'perfil': perfil,
        'objetivo': objetivos.last() if objetivos else None,
        'fotos': progresos,
        'ultima_foto': ultima_foto,
        'rutina': rutina,
        'peso_actual': peso_actual,
        'diferencia': diferencia,
        'diferencia_abs': diferencia_abs,
        'total_horas': total_horas,
        'modo_edicion': modo_edicion,
    })



@login_required
def perfil(request):
    """Permite ver y editar los datos personales y el objetivo."""
    perfil, _ = PerfilUsuario.objects.get_or_create(
        usuario=request.user,
        defaults={
            'edad': 0,
            'peso': 0,
            'altura': 0,
            'nivel': 'medio',
            'dias_entrenamiento': 3
        }
    )

    objetivo = Objetivo.objects.filter(usuario=request.user).last()
    modo_edicion = request.GET.get('editar') == '1'

    if request.method == 'POST':
        perfil_form = PerfilUsuarioForm(request.POST, instance=perfil)
        objetivo_form = ObjetivoForm(request.POST, instance=objetivo)

        if perfil_form.is_valid() and objetivo_form.is_valid():
            perfil_form.save()
            nuevo_objetivo = objetivo_form.save(commit=False)
            nuevo_objetivo.usuario = request.user
            nuevo_objetivo.save()
            return redirect('perfil')
    else:
        perfil_form = PerfilUsuarioForm(instance=perfil)
        objetivo_form = ObjetivoForm(instance=objetivo)

   
    rutina = generar_rutina(perfil, objetivo) if objetivo else None
    ultima_foto = Progreso.objects.filter(usuario=request.user).order_by('-fecha').first()

    return render(request, 'usuarios/perfil.html', {
        'perfil_form': perfil_form,
        'objetivo_form': objetivo_form,
        'objetivo': objetivo,
        'perfil': perfil,
        'rutina': rutina,           
        'ultima_foto': ultima_foto, 
        'modo_edicion': modo_edicion,
    })



@login_required
def rutina(request):
    """Muestra la rutina generada por la IA para el usuario."""
    perfil = get_object_or_404(PerfilUsuario, usuario=request.user)
    objetivo = Objetivo.objects.filter(usuario=request.user).last()

    if not objetivo:
        return render(request, 'usuarios/rutina.html', {
            'rutina': None,
            'sin_objetivo': True
        })

    rutina_generada = generar_rutina(perfil, objetivo)

    return render(request, 'usuarios/rutina.html', {
        'rutina': rutina_generada,
        'sin_objetivo': False
    })



@login_required
def progreso(request):
    """Galería de fotos y estadísticas de avance."""

    # Solo progresos con imagen válida
    progresos = (
        Progreso.objects
        .filter(usuario=request.user)
        .exclude(Q(imagen='') | Q(imagen__isnull=True))
        .order_by('-fecha')
    )

    ultima_foto = progresos.first() if progresos.exists() else None

    pesos = [float(p.peso_actual) for p in progresos if p.peso_actual]
    peso_actual = pesos[-1] if pesos else 0
    peso_inicial = pesos[0] if pesos else 0
    diferencia = round(peso_actual - peso_inicial, 1) if pesos else 0
    total_horas = sum(p.horas for p in progresos if p.horas)

    return render(request, 'usuarios/progreso.html', {
        'progresos': progresos,
        'ultima_foto': ultima_foto,
        'peso_actual': peso_actual,
        'peso_inicial': peso_inicial,
        'diferencia': diferencia,
        'total_horas': total_horas,
    })

@login_required
def subir_progreso(request):
    """Formulario para agregar una nueva foto y datos de progreso."""
    if request.method == 'POST':
        form = ProgresoForm(request.POST, request.FILES)
        if form.is_valid():
            progreso = form.save(commit=False)
            progreso.usuario = request.user
            progreso.save()
            return redirect('progreso')  # Redirige a la galería
    else:
        form = ProgresoForm()
    return render(request, 'usuarios/subir_progreso.html', {'form': form})




@login_required
def editar_objetivo(request):
    """Permite crear o modificar el objetivo del usuario."""
    if request.method == 'POST':
        form = ObjetivoForm(request.POST)
        if form.is_valid():
            objetivo = form.save(commit=False)
            objetivo.usuario = request.user
            objetivo.save()
            return redirect('dashboard')
    else:
        form = ObjetivoForm()
    return render(request, 'usuarios/objetivo.html', {'form': form})


@login_required
def nutricionistas(request):
    """Lista de nutricionistas disponibles."""
    profesionales = Profesional.objects.filter(tipo='nutricionista')
    return render(request, 'usuarios/nutricionistas.html', {'profesionales': profesionales})


@login_required
def entrenadores(request):
    """Listado de entrenadores personales."""
    profesionales = Profesional.objects.filter(tipo='entrenador')
    return render(request, 'usuarios/entrenadores.html', {'profesionales': profesionales})

@login_required
def reporte_pdf(request):
    """Genera un PDF con el historial de progreso del usuario."""
    usuario = request.user
    perfil = PerfilUsuario.objects.filter(usuario=usuario).first()
    objetivo = Objetivo.objects.filter(usuario=usuario).last()
    progresos = Progreso.objects.filter(usuario=usuario).order_by('fecha')

    template = get_template("usuarios/reporte_pdf.html")
    html = template.render({
        "usuario": usuario,
        "perfil": perfil,
        "objetivo": objetivo,
        "progresos": progresos
    })

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="reporte.pdf"'

    pisa_status = pisa.CreatePDF(src=html, dest=response, encoding='utf-8')
    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)
    return response



@login_required
def editar_perfil(request):
    """Formulario para actualizar los datos del perfil."""

    # Traemos (o creamos) el perfil
    perfil, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # o a 'dashboard', como prefieras
    else:
        form = PerfilUsuarioForm(instance=perfil)

    return render(request, 'usuarios/editar_perfil.html', {'form': form})



@login_required
@require_POST
def agregar_horas(request):
    """Registra horas de entrenamiento de manera rápida."""
    horas = request.POST.get('horas')
    if horas:
        perfil = PerfilUsuario.objects.filter(usuario=request.user).first()
        peso_actual = perfil.peso if perfil else 0  # O algún valor seguro
        Progreso.objects.create(
            usuario=request.user,
            horas=horas,
            fecha=date.today(),
            peso_actual=peso_actual  # 👈 Esto evita el error
        )
    return redirect('dashboard')
