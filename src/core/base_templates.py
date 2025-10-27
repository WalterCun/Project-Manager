"""
Base templates for common document types.
These templates are loaded automatically when the database is initialized.
"""

from typing import Dict, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.database import DatabaseManager

def get_base_templates() -> List[Dict[str, str]]:
    """Get base templates with common elements."""
    return [
        # HTML Templates
        {
            "nombre": "Plantilla HTML Base",
            "contenido": """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{titulo}}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
        }
        .header {
            text-align: center;
            border-bottom: 2px solid #333;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .title {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }
        .subtitle {
            font-size: 16px;
            color: #666;
            margin-top: 10px;
        }
        .date {
            font-size: 14px;
            color: #888;
            margin-top: 5px;
        }
        .section {
            margin: 30px 0;
        }
        .section-title {
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
            border-left: 4px solid #007acc;
            padding-left: 10px;
        }
        .content {
            margin-left: 20px;
        }
        .table-of-contents {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .toc-title {
            font-weight: bold;
            margin-bottom: 10px;
        }
        .toc-item {
            margin: 5px 0;
            padding-left: 15px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        .footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            font-size: 12px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">{{titulo}}</div>
        <div class="subtitle">{{empresa}}</div>
        <div class="date">Fecha: {{fecha}} | Hora: {{hora}}</div>
    </div>

    <div class="table-of-contents">
        <div class="toc-title">Tabla de Contenido</div>
        <div class="toc-item">1. Introducción</div>
        <div class="toc-item">2. Objetivo</div>
        <div class="toc-item">3. Contenido</div>
        <div class="toc-item">4. Conclusiones</div>
    </div>

    <div class="section">
        <div class="section-title">Introducción</div>
        <div class="content">
            <p>{{introduccion}}</p>
        </div>
    </div>

    <div class="section">
        <div class="section-title">Objetivo</div>
        <div class="content">
            <p>{{objetivo}}</p>
        </div>
    </div>

    <div class="section">
        <div class="section-title">Contenido</div>
        <div class="content">
            <table>
                <thead>
                    <tr>
                        <th>Elemento</th>
                        <th>Descripción</th>
                        <th>Estado</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{{elemento1}}</td>
                        <td>{{descripcion1}}</td>
                        <td>{{estado1}}</td>
                    </tr>
                    <tr>
                        <td>{{elemento2}}</td>
                        <td>{{descripcion2}}</td>
                        <td>{{estado2}}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <div class="section">
        <div class="section-title">Conclusiones</div>
        <div class="content">
            <p>{{conclusiones}}</p>
        </div>
    </div>

    <div class="footer">
        <p>Generado automáticamente por Project Manager | {{fecha}} {{hora}}</p>
    </div>
</body>
</html>""",
            "extension": "html"
        },

        # Markdown Template
        {
            "nombre": "Plantilla Markdown Base",
            "contenido": """# {{titulo}}

**{{empresa}}**

*Fecha: {{fecha}} | Hora: {{hora}}*

---

## Tabla de Contenido

1. [Introducción](#introducción)
2. [Objetivo](#objetivo)
3. [Contenido](#contenido)
4. [Conclusiones](#conclusiones)

---

## Introducción

{{introduccion}}

## Objetivo

{{objetivo}}

## Contenido

| Elemento | Descripción | Estado |
|----------|-------------|--------|
| {{elemento1}} | {{descripcion1}} | {{estado1}} |
| {{elemento2}} | {{descripcion2}} | {{estado2}} |

## Conclusiones

{{conclusiones}}

---

*Generado automáticamente por Project Manager | {{fecha}} {{hora}}*""",
            "extension": "md"
        },

        # DOCX Template (Text-based)
        {
            "nombre": "Plantilla DOCX Base",
            "contenido": """{{titulo}}

{{empresa}}

Fecha: {{fecha}} | Hora: {{hora}}

ÍNDICE

1. Introducción
2. Objetivo
3. Contenido
4. Conclusiones

INTRODUCCIÓN

{{introduccion}}

OBJETIVO

{{objetivo}}

CONTENIDO

Elemento: {{elemento1}}
Descripción: {{descripcion1}}
Estado: {{estado1}}

Elemento: {{elemento2}}
Descripción: {{descripcion2}}
Estado: {{estado2}}

CONCLUSIONES

{{conclusiones}}

---
Generado automáticamente por Project Manager | {{fecha}} {{hora}}""",
            "extension": "docx"
        },

        # Email Template
        {
            "nombre": "Plantilla Email Base",
            "contenido": """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{titulo}}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #f8f9fa; padding: 20px; text-align: center; }
        .content { margin: 20px 0; }
        .footer { border-top: 1px solid #ddd; padding-top: 10px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h2>{{titulo}}</h2>
        <p><strong>{{empresa}}</strong></p>
        <p>{{fecha}} | {{hora}}</p>
    </div>

    <div class="content">
        <p>Estimado {{nombre}},</p>

        <p>{{mensaje}}</p>

        <p>Atentamente,<br>{{remitente}}</p>
    </div>

    <div class="footer">
        <p>Generado automáticamente por Project Manager | {{fecha}} {{hora}}</p>
    </div>
</body>
</html>""",
            "extension": "html"
        },

        # Manual Template
        {
            "nombre": "Plantilla Manual Base",
            "contenido": """# {{titulo}}

**Manual de {{tipo}}**

*{{empresa}}*

*Versión: {{version}} | Fecha: {{fecha}} | Hora: {{hora}}*

---

## Tabla de Contenido

1. [Introducción](#introducción)
2. [Objetivos](#objetivos)
3. [Procedimientos](#procedimientos)
4. [Anexos](#anexos)

---

## Introducción

### Propósito
{{proposito}}

### Alcance
{{alcance}}

### Responsabilidades
{{responsabilidades}}

## Objetivos

{{objetivos}}

## Procedimientos

### Procedimiento 1: {{procedimiento1}}
{{descripcion1}}

### Procedimiento 2: {{procedimiento2}}
{{descripcion2}}

## Anexos

- Anexo 1: {{anexo1}}
- Anexo 2: {{anexo2}}

---

*Este manual fue generado automáticamente por Project Manager*

*{{empresa}} | {{fecha}} | {{hora}}*""",
            "extension": "md"
        },

        # Excel Template
        {
            "nombre": "Plantilla Excel Base",
            "contenido": """{
  "titulo": "{{titulo}}",
  "empresa": "{{empresa}}",
  "fecha": "{{fecha}}",
  "hora": "{{hora}}",
  "seccion1": "Introducción",
  "seccion2": "Objetivo",
  "seccion3": "Contenido",
  "seccion4": "Conclusiones",
  "introduccion": "{{introduccion}}",
  "objetivo": "{{objetivo}}",
  "contenido": {
    "Elemento": ["{{elemento1}}", "{{elemento2}}"],
    "Descripción": ["{{descripcion1}}", "{{descripcion2}}"],
    "Estado": ["{{estado1}}", "{{estado2}}"]
  },
  "conclusiones": "{{conclusiones}}"
}""",
            "extension": "xlsx"
        },

        # Report Template
        {
            "nombre": "Plantilla Reporte Base",
            "contenido": """{
  "titulo": "{{titulo}}",
  "empresa": "{{empresa}}",
  "fecha": "{{fecha}}",
  "hora": "{{hora}}",
  "seccion1": "Resumen Ejecutivo",
  "seccion2": "Metodología",
  "seccion3": "Resultados",
  "seccion4": "Recomendaciones",
  "introduccion": "{{introduccion}}",
  "objetivo": "{{objetivo}}",
  "contenido": {
    "Métrica": ["{{metrica1}}", "{{metrica2}}", "{{metrica3}}"],
    "Valor": ["{{valor1}}", "{{valor2}}", "{{valor3}}"],
    "Estado": ["{{estado1}}", "{{estado2}}", "{{estado3}}"]
  },
  "conclusiones": "{{conclusiones}}"
}""",
            "extension": "xlsx"
        }
    ]

def initialize_base_templates(db_manager: DatabaseManager) -> None:
    """Initialize base templates in the database."""
    templates = get_base_templates()

    for template_data in templates:
        try:
            # Check if template already exists
            existing = db_manager.list_templates()
            if not any(t['nombre'] == template_data['nombre'] for t in existing):
                db_manager.save_template(
                    nombre=template_data['nombre'],
                    contenido=template_data['contenido'],
                    extension=template_data['extension']
                )
                print(f"Template '{template_data['nombre']}' initialized.")
        except Exception as e:
            print(f"Error initializing template '{template_data['nombre']}': {e}")

def get_template_params_for_file(file_name: str) -> Dict[str, str]:
    """Get default parameters for a specific file type with comprehensive defaults."""
    from datetime import datetime

    # Base parameters that all templates should have
    base_params = {
        # Basic info
        "titulo": "Documento Base",
        "empresa": "Empresa Ejemplo",
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "hora": datetime.now().strftime("%H:%M:%S"),
        "version": "1.0",

        # Contact info
        "nombre": "Usuario Ejemplo",
        "remitente": "Sistema Automático",
        "email": "contacto@empresa.com",
        "telefono": "+593 999 999 999",

        # Content sections
        "introduccion": "Este es un documento base generado automáticamente.",
        "objetivo": "Proporcionar información estructurada sobre el tema.",
        "contenido": "Contenido detallado del documento.",
        "conclusiones": "Se han presentado los elementos principales del documento.",

        # Generic elements
        "elemento1": "Elemento 1",
        "descripcion1": "Descripción del elemento 1",
        "estado1": "Activo",
        "elemento2": "Elemento 2",
        "descripcion2": "Descripción del elemento 2",
        "estado2": "Pendiente",
        "elemento3": "Elemento 3",
        "descripcion3": "Descripción del elemento 3",
        "estado3": "Planificado",

        # Metrics
        "metrica1": "Métrica 1",
        "valor1": "100",
        "metrica2": "Métrica 2",
        "valor2": "85%",
        "metrica3": "Métrica 3",
        "valor3": "50",

        # Manual specific
        "tipo": "General",
        "proposito": "Establecer procedimientos estándar.",
        "alcance": "Aplicanble a todo el personal.",
        "responsabilidades": "El personal debe seguir estos procedimientos.",
        "procedimiento1": "Procedimiento 1",
        "procedimiento2": "Procedimiento 2",
        "anexo1": "Anexo 1",
        "anexo2": "Anexo 2",

        # Email specific
        "asunto": "Documento Generado Automáticamente",
        "mensaje": "Este es un mensaje generado automáticamente por el sistema.",

        # Excel specific
        "seccion1": "Introducción",
        "seccion2": "Objetivo",
        "seccion3": "Contenido",
        "seccion4": "Conclusiones"
    }

    file_lower = file_name.lower()

    # Customize based on file name patterns
    if "confirmacion" in file_lower or "reserva" in file_lower:
        base_params.update({
            "titulo": "Confirmación de Reserva",
            "introduccion": "Se confirma la reserva del servicio solicitado.",
            "objetivo": "Confirmar la reserva y proporcionar detalles del servicio.",
            "elemento1": "Servicio",
            "descripcion1": "Tour guiado",
            "estado1": "Confirmado",
            "elemento2": "Fecha",
            "descripcion2": "Próxima semana",
            "estado2": "Programado",
            "conclusiones": "La reserva ha sido confirmada exitosamente.",
            "mensaje": "Su reserva ha sido confirmada. Los detalles del servicio se encuentran a continuación.",
            "asunto": "Confirmación de Reserva - {{empresa}}"
        })
    elif "recordatorio" in file_lower:
        base_params.update({
            "titulo": "Recordatorio de Servicio",
            "introduccion": "Este es un recordatorio de su servicio programado.",
            "objetivo": "Recordar al cliente sobre el servicio próximo.",
            "elemento1": "Recordatorio",
            "descripcion1": "24 horas antes",
            "estado1": "Enviado",
            "elemento2": "Confirmación",
            "descripcion2": "Requerida",
            "estado2": "Pendiente",
            "conclusiones": "Se ha enviado el recordatorio exitosamente.",
            "mensaje": "Le recordamos que su servicio está programado para mañana.",
            "asunto": "Recordatorio de Servicio - {{empresa}}"
        })
    elif "agradecimiento" in file_lower:
        base_params.update({
            "titulo": "Agradecimiento por su Preferencia",
            "introduccion": "Gracias por elegir nuestros servicios.",
            "objetivo": "Agradecer al cliente y solicitar feedback.",
            "elemento1": "Servicio",
            "descripcion1": "Completado",
            "estado1": "Finalizado",
            "elemento2": "Feedback",
            "descripcion2": "Solicitado",
            "estado2": "Pendiente",
            "conclusiones": "El servicio ha concluido satisfactoriamente.",
            "mensaje": "Gracias por su preferencia. Nos gustaría conocer su opinión sobre el servicio recibido.",
            "asunto": "Agradecimiento - {{empresa}}"
        })
    elif "manual" in file_lower or "guia" in file_lower:
        base_params.update({
            "titulo": "Manual de Procedimientos",
            "tipo": "Operativos",
            "proposito": "Establecer procedimientos estándar para las operaciones.",
            "alcance": "Aplicanble a todo el personal operativo.",
            "responsabilidades": "El personal debe seguir estos procedimientos.",
            "objetivos": "Estandarizar procesos y mejorar la eficiencia.",
            "procedimiento1": "Inicio de Operaciones",
            "descripcion1": "Verificar equipos y materiales necesarios.",
            "procedimiento2": "Cierre de Operaciones",
            "descripcion2": "Registrar actividades y limpiar área de trabajo.",
            "anexo1": "Lista de Equipos",
            "anexo2": "Formato de Reporte",
            "conclusiones": "Este manual establece los procedimientos estándar a seguir."
        })
    elif "evaluacion" in file_lower or "kpi" in file_lower:
        base_params.update({
            "titulo": "Evaluación de Desempeño",
            "introduccion": "Evaluación periódica del desempeño del personal.",
            "objetivo": "Medir y mejorar el rendimiento del equipo.",
            "elemento1": "Productividad",
            "descripcion1": "Tareas completadas",
            "estado1": "85%",
            "elemento2": "Calidad",
            "descripcion2": "Satisfacción del cliente",
            "estado2": "92%",
            "elemento3": "Eficiencia",
            "descripcion3": "Tiempo de respuesta",
            "estado3": "78%",
            "conclusiones": "El desempeño general es satisfactorio con áreas de mejora identificadas.",
            "metrica1": "Productividad",
            "metrica2": "Calidad",
            "metrica3": "Eficiencia"
        })
    elif "reporte" in file_lower or "report" in file_lower:
        base_params.update({
            "titulo": "Reporte de Actividades",
            "introduccion": "Reporte periódico de las actividades realizadas.",
            "objetivo": "Documentar y analizar el progreso de las operaciones.",
            "metrica1": "Tareas Completadas",
            "valor1": "25",
            "metrica2": "Tiempo Promedio",
            "valor2": "2.5 horas",
            "metrica3": "Satisfacción",
            "valor3": "4.2/5",
            "conclusiones": "Las operaciones se desarrollan según lo planificado."
        })
    elif "calendario" in file_lower or "calendar" in file_lower:
        base_params.update({
            "titulo": "Calendario de Actividades",
            "introduccion": "Planificación temporal de las actividades programadas.",
            "objetivo": "Organizar y coordinar las actividades del equipo.",
            "elemento1": "Reunión Semanal",
            "descripcion1": "Lunes 9:00 AM",
            "estado1": "Programado",
            "elemento2": "Revisión Mensual",
            "descripcion2": "Último viernes del mes",
            "estado2": "Programado",
            "conclusiones": "El calendario está actualizado y coordinado."
        })
    elif "presupuesto" in file_lower or "budget" in file_lower:
        base_params.update({
            "titulo": "Presupuesto y Proyecciones",
            "introduccion": "Análisis financiero y proyecciones económicas.",
            "objetivo": "Planificar y controlar los recursos financieros.",
            "metrica1": "Ingresos",
            "valor1": "$10,000",
            "metrica2": "Gastos",
            "valor2": "$7,500",
            "metrica3": "Utilidad",
            "valor3": "$2,500",
            "conclusiones": "El presupuesto se mantiene dentro de los parámetros establecidos."
        })

    # Add current date/time if not already set
    if base_params["fecha"] == "2023-01-01":
        base_params["fecha"] = datetime.now().strftime("%Y-%m-%d")
    if base_params["hora"] == "12:00:00":
        base_params["hora"] = datetime.now().strftime("%H:%M:%S")

    return base_params