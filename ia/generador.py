"""Pequeño módulo de apoyo para generar rutinas con OpenAI."""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargamos la clave desde ``.env`` y creamos el cliente
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generar_rutina(perfil, objetivo):
    """Genera una rutina personalizada para el usuario.

    ``perfil`` y ``objetivo`` son instancias de nuestros modelos. Si alguno de
    ellos falta devolvemos ``None`` para que la vista pueda manejarlo sin
    errores.  El prompt se construye con todos los datos relevantes y se envía a
    la API de OpenAI, devolviendo el texto con la propuesta de rutina semanal.
    """

    if not perfil or not objetivo:
        return None

    prompt = f"""
    Sos un entrenador personal. Creá una rutina semanal de ejercicios para esta persona:

    Edad: {perfil.edad}
    Peso: {perfil.peso} kg
    Altura: {perfil.altura} m
    Nivel de actividad: {perfil.get_nivel_display()}
    Objetivo: {getattr(objetivo, 'tipo', '')}
    Peso deseado: {getattr(objetivo, 'peso_deseado', '')} kg
    Días disponibles: {getattr(objetivo, 'dias_entrenamiento', perfil.dias_entrenamiento)}

    Formato solicitado:
    Día 1: [ejercicios con series y repeticiones]
    Día 2: ...
    Día 3: ...
    (Hasta cubrir todos los días indicados)
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sos un entrenador personal experto en planificación semanal."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error al generar rutina: {e}")
        return "No se pudo generar la rutina en este momento."
