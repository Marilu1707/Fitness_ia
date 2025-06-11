# 🧠 Fitness CRM con Inteligencia Artificial

Este proyecto es un **sistema web inteligente** para usuarios que desean alcanzar objetivos de entrenamiento físico, con un panel personalizado que registra su progreso, genera rutinas automáticas y permite visualizar estadísticas y fotos. Está desarrollado con **Django**, integrando una lógica de IA para crear rutinas adaptadas al perfil del usuario.

---

## 🚀 Funcionalidades

- ✅ Registro/Login de usuarios
- 👤 Gestión del perfil (edad, altura, peso, nivel)
- 🎯 Definición de objetivos: tipo, peso deseado, días de entrenamiento
- 📸 Carga de fotos de progreso
- 📅 Historial de progreso (fecha, peso, horas entrenadas)
- 📈 Estadísticas automáticas: peso actual, diferencia, total de horas
- 🧠 Generación automática de rutina personalizada (IA simulada)
- 📄 Descarga de reporte en PDF
- 🌙 Modo oscuro + estilo moderno con detalles flúo

---

## 🛠️ Tecnologías usadas

- **Backend**: Django 5.x
- **Frontend**: HTML5 + CSS3 (modo oscuro), JavaScript (ligero)
- **Base de datos**: SQLite
- **PDF Generator**: xhtml2pdf
- **IA (simulada)**: `generador.py` (reglas inteligentes adaptadas)
- **Control de versiones**: Git + GitHub

---

## 📂 Estructura del proyecto

```
fitness_crm_ia/
├── usuarios/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── templates/
│   │   └── usuarios/
│   │       ├── dashboard.html
│   │       ├── perfil.html
│   │       ├── rutina.html
│   │       └── ...
├── ia/
│   └── generador.py
├── static/
│   └── css/
│       └── styles.css
├── media/
│   └── (fotos de progreso)
├── db.sqlite3
└── manage.py
```

---

## 🔧 Instalación y uso

1. **Cloná el repositorio**  
```bash
git clone https://github.com/tuusuario/fitness-crm-ia.git
cd fitness-crm-ia
```

2. **Crea y activa un entorno virtual**  
```bash
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate
```

3. **Instala las dependencias**  
```bash
pip install -r requirements.txt
```

4. **Realizá migraciones**  
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Corre el servidor local**  
```bash
python manage.py runserver
```

6. **Accedé a la app**  
📍 Ir a [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📸 Capturas de pantalla

> (Podés agregar imágenes de tu dashboard, rutina y progreso acá)

---

## 📌 Nota

Este proyecto está diseñado como portfolio personal, demostrando habilidades en:

- Manejo de datos de usuarios
- Generación de contenido automatizado
- Diseño responsive y visual atractivo
- Lógica condicional personalizada

---

## 📬 Contacto

Si tenés dudas o sugerencias, podés escribirme a: **[tuemail@dominio.com]**

---

## 🧠 Autor

Maria Lujan Massironi — 2025
