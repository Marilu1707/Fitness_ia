"""Generador de rutinas simulado para el proyecto Fitness CRM.

El objetivo es ofrecer una experiencia "tipo IA" sin depender de servicios
externos. A partir de la información del perfil, los objetivos y el historial de
entrenamientos se construye una propuesta de rutina semanal estructurada.

La interfaz pública expone una única función ``generar_rutina`` que retorna una
lista de diccionarios fácilmente serializable a JSON y directa de recorrer en
las plantillas.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable, List

# --- Configuración base ----------------------------------------------------

@dataclass(frozen=True)
class Ejercicio:
    nombre: str
    series: str
    descripcion: str


# Plantillas base según el foco principal de cada día
PLANTILLAS_EJERCICIOS = {
    "fuerza": [
        Ejercicio("Sentadillas con peso corporal", "3 x 12", "Controlá la bajada y mantené el core firme."),
        Ejercicio("Flexiones", "3 x 10", "Apoyá rodillas si necesitás reducir la carga."),
        Ejercicio("Estocadas alternadas", "3 x 12", "Zancadas largas y torso erguido."),
        Ejercicio("Plancha", "3 x 40" , "Mantené glúteos alineados con hombros."),
    ],
    "cardio": [
        Ejercicio("Caminata / trote suave", "20-25 min", "Buscá un ritmo que te permita hablar."),
        Ejercicio("Jumping jacks", "3 x 45 seg", "Mantené el abdomen activo y brazos extendidos."),
        Ejercicio("Mountain climbers", "3 x 30 seg", "Apoyá bien las manos y llevá rodillas al pecho."),
        Ejercicio("Bicicleta / elíptico", "15 min", "Enfocate en la respiración."),
    ],
    "movilidad": [
        Ejercicio("Movilidad de cadera", "2 x 8", "Círculos amplios, sin dolor."),
        Ejercicio("Estiramiento de cadena posterior", "3 x 30 seg", "Sostené sin rebotes."),
        Ejercicio("Gato-camello", "3 x 12", "Coordiná respiración con movimiento."),
        Ejercicio("Respiración diafragmática", "5 min", "Inhalá por nariz, exhalá por boca."),
    ],
    "potencia": [
        Ejercicio("Sentadillas con salto", "4 x 10", "Aterrizá suave, rodillas alineadas."),
        Ejercicio("Burpees controlados", "3 x 10", "Mantené un ritmo constante."),
        Ejercicio("Press militar con mancuernas", "3 x 12", "Activá abdomen para proteger la zona lumbar."),
        Ejercicio("Remo con banda", "3 x 15", "Escapulas hacia atrás, sin balanceo."),
    ],
}

FOCOS_DISPONIBLES = [
    ("fuerza", "Fuerza y Core"),
    ("cardio", "Resistencia y Cardio"),
    ("movilidad", "Movilidad y Recuperación"),
    ("potencia", "Potencia y HIIT"),
]

OBJETIVOS_MAP = {
    "perder_peso": ["cardio", "fuerza", "cardio", "movilidad", "fuerza", "cardio"],
    "ganar_masa": ["fuerza", "potencia", "fuerza", "movilidad", "fuerza", "cardio"],
    "rendimiento": ["potencia", "fuerza", "cardio", "movilidad", "potencia", "cardio"],
    "bienestar": ["movilidad", "fuerza", "cardio", "movilidad", "cardio", "fuerza"],
}


def _normalizar_objetivo(texto: str | None) -> str:
    """Clasifica el objetivo en una de las categorías conocidas."""

    if not texto:
        return "bienestar"

    texto = texto.lower()
    if any(token in texto for token in ("bajar", "perder", "definir")):
        return "perder_peso"
    if any(token in texto for token in ("masa", "musculo", "hipertrofia")):
        return "ganar_masa"
    if any(token in texto for token in ("rendimiento", "resistencia", "competencia")):
        return "rendimiento"
    return "bienestar"


def _duracion_sugerida(promedio_horas: float, nivel: str) -> int:
    base = 45 if nivel in {"medio", "alto"} else 30
    ajuste = round(min(max(promedio_horas * 60 - base, -10), 20))
    return max(25, base + ajuste)


def _extra_recomendaciones(diferencia_peso: float | None, nivel: str) -> List[str]:
    recomendaciones = [
        "Calentá 5-10 minutos antes de empezar.",
        "Cerrá la sesión con estiramientos suaves.",
        "Hidratate durante todo el día.",
    ]
    if diferencia_peso is not None:
        if diferencia_peso > 0:
            recomendaciones.append("Priorizá déficit calórico suave y proteínas magras.")
        elif diferencia_peso < 0:
            recomendaciones.append("Sumá colaciones proteicas para acompañar el aumento de masa.")
    if nivel == "alto":
        recomendaciones.append("Podés incrementar el peso un 5-10% si te sentís con energía.")
    elif nivel == "bajo":
        recomendaciones.append("Mantené intensidad moderada y descansos de 90 segundos entre series.")
    return recomendaciones


def generar_rutina(perfil, objetivo=None, historial: Iterable | None = None) -> list[dict]:
    """Genera una rutina semanal basada en los datos disponibles.

    Parameters
    ----------
    perfil: PerfilUsuario
        Instancia del perfil vinculada al usuario.
    objetivo: Objetivo | None
        Último objetivo registrado. Si no existe se retorna una lista vacía.
    historial: iterable
        Colección opcional de objetos con atributos ``fecha`` y ``horas``.
    """

    if not perfil or not objetivo:
        return []

    dias_plan = getattr(objetivo, "dias_entrenamiento", None) or getattr(perfil, "dias_entrenamiento", 3)
    dias_plan = int(max(1, min(7, dias_plan)))

    registros = list(historial or [])
    registros.sort(key=lambda prog: getattr(prog, "fecha", date.today()))

    horas_totales = 0.0
    sesiones = 0
    for prog in registros:
        horas = getattr(prog, "horas", 0) or 0
        try:
            horas_float = float(horas)
        except (TypeError, ValueError):
            horas_float = 0.0
        if horas_float > 0:
            sesiones += 1
            horas_totales += horas_float

    promedio_horas = horas_totales / sesiones if sesiones else 1.0

    peso_actual = None
    if registros:
        peso_actual = getattr(registros[-1], "peso_actual", None)
    peso_deseado = getattr(objetivo, "peso_deseado", None)

    diferencia_peso = None
    try:
        if peso_actual is not None and peso_deseado is not None:
            diferencia_peso = float(peso_actual) - float(peso_deseado)
    except (TypeError, ValueError):
        diferencia_peso = None

    categoria_objetivo = _normalizar_objetivo(getattr(objetivo, "tipo", None))
    secuencia = OBJETIVOS_MAP.get(categoria_objetivo, OBJETIVOS_MAP["bienestar"])

    nivel = getattr(perfil, "nivel", "medio")
    rutina: list[dict] = []
    recomendaciones_generales = _extra_recomendaciones(diferencia_peso, nivel)
    duracion = _duracion_sugerida(promedio_horas, nivel)

    for indice in range(dias_plan):
        foco_clave = secuencia[indice % len(secuencia)]
        titulo = next((etiqueta for clave, etiqueta in FOCOS_DISPONIBLES if clave == foco_clave), foco_clave.title())
        ejercicios = PLANTILLAS_EJERCICIOS.get(foco_clave, PLANTILLAS_EJERCICIOS["fuerza"])

        rutina.append(
            {
                "dia": indice + 1,
                "titulo": titulo,
                "foco": foco_clave,
                "ejercicios": [
                    {
                        "nombre": ejercicio.nombre,
                        "series": ejercicio.series,
                        "descripcion": ejercicio.descripcion,
                    }
                    for ejercicio in ejercicios
                ],
                "recomendaciones": recomendaciones_generales,
                "duracion_estimada": duracion,
            }
        )

    return rutina
