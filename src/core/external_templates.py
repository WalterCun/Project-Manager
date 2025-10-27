"""
External template management system.
Loads templates from external JSON files in the templates/ directory.
Supports multi-sheet Excel templates and other formats.
"""

import os
import json
from typing import Dict, List, Any, Optional
from pathlib import Path

class ExternalTemplateLoader:
    """Loads and manages external templates from JSON files."""

    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(exist_ok=True)

    def get_template_path(self, template_name: str, extension: str) -> Optional[Path]:
        """Get the path to an external template file."""
        template_file = self.templates_dir / extension / f"{template_name}.json"
        return template_file if template_file.exists() else None

    def load_template(self, template_name: str, extension: str) -> Optional[Dict[str, Any]]:
        """Load an external template by name and extension."""
        template_path = self.get_template_path(template_name, extension)
        if not template_path:
            return None

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
            print(f"Warning: Failed to load external template {template_name}.{extension}: {e}")
            return None

    def list_templates(self, extension: Optional[str] = None) -> List[Dict[str, str]]:
        """List all available external templates."""
        templates = []

        if extension:
            template_dir = self.templates_dir / extension
            if template_dir.exists():
                for template_file in template_dir.glob("*.json"):
                    try:
                        with open(template_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        templates.append({
                            'name': data.get('name', template_file.stem),
                            'extension': extension,
                            'description': data.get('description', ''),
                            'file': str(template_file)
                        })
                    except Exception:
                        continue
        else:
            for ext_dir in self.templates_dir.iterdir():
                if ext_dir.is_dir():
                    for template_file in ext_dir.glob("*.json"):
                        try:
                            with open(template_file, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                            templates.append({
                                'name': data.get('name', template_file.stem),
                                'extension': ext_dir.name,
                                'description': data.get('description', ''),
                                'file': str(template_file)
                            })
                        except Exception:
                            continue

        return templates

    def save_template(self, template_data: Dict[str, Any], extension: str) -> bool:
        """Save a template to external file."""
        template_dir = self.templates_dir / extension
        template_dir.mkdir(exist_ok=True)

        template_name = template_data.get('name', 'unnamed_template')
        template_file = template_dir / f"{template_name}.json"

        try:
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving template {template_name}.{extension}: {e}")
            return False

    def delete_template(self, template_name: str, extension: str) -> bool:
        """Delete an external template."""
        template_path = self.get_template_path(template_name, extension)
        if template_path and template_path.exists():
            try:
                template_path.unlink()
                return True
            except Exception as e:
                print(f"Error deleting template {template_name}.{extension}: {e}")
                return False
        return False

def create_excel_multi_sheet_template() -> Dict[str, Any]:
    """Create a multi-sheet Excel template example."""
    return {
        "name": "Multi-Sheet Dashboard",
        "extension": "xlsx",
        "description": "Excel template with data, summary, and dashboard sheets",
        "version": "1.0",
        "author": "Project Manager",
        "sheets": {
            "Data": {
                "description": "Raw data input sheet",
                "cells": {
                    "A1": {
                        "value": "📊 {{titulo}}",
                        "style": {
                            "bold": True,
                            "font_size": 16,
                            "font_color": "1F4E79",
                            "fill": {"pattern": "solid", "color": "E6F3FF"}
                        }
                    },
                    "A2": {
                        "value": "{{empresa}}",
                        "style": {"italic": True, "font_size": 12}
                    },
                    "A3": {
                        "value": "Fecha: {{fecha}} | Hora: {{hora}}",
                        "style": {"font_size": 10, "font_color": "666666"}
                    },
                    "A5": {
                        "value": "📋 DATOS PRINCIPALES",
                        "style": {
                            "bold": True,
                            "font_size": 14,
                            "fill": {"pattern": "solid", "color": "F2F2F2"}
                        }
                    },
                    "B7": {"value": "{{metrica1}}"},
                    "C7": {"value": "{{metrica2}}"},
                    "D7": {"value": "{{metrica3}}"},
                    "B8": {"value": "{{valor1}}", "style": {"bold": True}},
                    "C8": {"value": "{{valor2}}", "style": {"bold": True}},
                    "D8": {"value": "{{valor3}}", "style": {"bold": True}},
                    "B9": {"value": "{{estado1}}", "style": {"font_color": "28A745"}},
                    "C9": {"value": "{{estado2}}", "style": {"font_color": "28A745"}},
                    "D9": {"value": "{{estado3}}", "style": {"font_color": "28A745"}}
                },
                "tables": {
                    "DataTable": {
                        "range": "B7:D9",
                        "headers": True,
                        "style": {
                            "header_fill": "0070C0",
                            "header_font_color": "FFFFFF",
                            "border": "thin"
                        }
                    }
                }
            },
            "Summary": {
                "description": "Summary and calculations sheet",
                "cells": {
                    "A1": {
                        "value": "📈 RESUMEN EJECUTIVO",
                        "style": {
                            "bold": True,
                            "font_size": 16,
                            "font_color": "1F4E79",
                            "fill": {"pattern": "solid", "color": "E6F3FF"}
                        }
                    },
                    "A3": {
                        "value": "Indicadores Clave",
                        "style": {"bold": True, "font_size": 12}
                    },
                    "B4": {"value": "Total Items"},
                    "C4": {"formula": "COUNTA(Data!B8:D8)"},
                    "B5": {"value": "Promedio"},
                    "C5": {"formula": "AVERAGE(Data!C8:D8)"},
                    "B6": {"value": "Máximo"},
                    "C6": {"formula": "MAX(Data!C8:D8)"},
                    "B7": {"value": "Mínimo"},
                    "C7": {"formula": "MIN(Data!C8:D8)"},
                    "A9": {
                        "value": "💡 ANÁLISIS",
                        "style": {"bold": True, "font_size": 12}
                    },
                    "B10": {"value": "{{analisis}}"}
                }
            },
            "Dashboard": {
                "description": "Visual dashboard with KPIs and insights",
                "cells": {
                    "A1": {
                        "value": "🎯 DASHBOARD EJECUTIVO",
                        "style": {
                            "bold": True,
                            "font_size": 18,
                            "font_color": "1F4E79",
                            "fill": {"pattern": "solid", "color": "E6F3FF"}
                        }
                    },
                    "A3": {
                        "value": "KPIs Principales",
                        "style": {"bold": True, "font_size": 14}
                    },
                    "B5": {
                        "value": "Estado General",
                        "style": {"bold": True}
                    },
                    "C5": {
                        "value": "{{estado_general}}",
                        "style": {
                            "bold": True,
                            "font_size": 14,
                            "font_color": "28A745"
                        }
                    },
                    "B6": {
                        "value": "Tendencia",
                        "style": {"bold": True}
                    },
                    "C6": {
                        "value": "{{tendencia}}",
                        "style": {"font_color": "0070C0"}
                    },
                    "A8": {
                        "value": "📊 GRÁFICOS Y VISUALIZACIONES",
                        "style": {"bold": True, "font_size": 12}
                    },
                    "B10": {"value": "Gráfico de barras: Métricas vs Valores"},
                    "B11": {"value": "Gráfico circular: Distribución por estados"},
                    "B12": {"value": "Gráfico de líneas: Tendencia temporal"},
                    "A14": {
                        "value": "🔍 CONCLUSIONES",
                        "style": {"bold": True, "font_size": 12}
                    },
                    "B15": {"value": "{{conclusiones}}"}
                },
                "charts": {
                    "MetricsChart": {
                        "type": "bar",
                        "title": "Métricas Principales",
                        "data_range": "Data!B7:D8",
                        "position": "B10:D15",
                        "style": {
                            "chart_type": "clustered_bar",
                            "legend": True,
                            "data_labels": True
                        }
                    },
                    "StatusChart": {
                        "type": "pie",
                        "title": "Distribución por Estados",
                        "data_range": "Data!B9:D9",
                        "position": "B16:D20",
                        "style": {
                            "legend": True,
                            "data_labels": True,
                            "colors": ["28A745", "FFC107", "DC3545"]
                        }
                    }
                }
            }
        },
        "global_styles": {
            "header_style": {
                "bold": True,
                "font_size": 12,
                "fill": {"pattern": "solid", "color": "F2F2F2"}
            },
            "data_style": {
                "border": "thin",
                "alignment": "center"
            }
        }
    }

def create_html_template() -> Dict[str, Any]:
    """Create an HTML template example."""
    return {
        "name": "Professional Report",
        "extension": "html",
        "description": "Professional HTML report with responsive design",
        "css_framework": "bootstrap",
        "content": """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{titulo}}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .report-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 0;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            border-left: 4px solid #007bff;
        }
        .status-badge {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
        }
        .status-active { background-color: #d4edda; color: #155724; }
        .status-pending { background-color: #fff3cd; color: #856404; }
        .status-completed { background-color: #d1ecf1; color: #0c5460; }
    </style>
</head>
<body>
    <div class="report-header text-center">
        <h1>{{titulo}}</h1>
        <h5>{{empresa}}</h5>
        <p class="mb-0">Generado el {{fecha}} a las {{hora}}</p>
    </div>

    <div class="container-fluid">
        <div class="row">
            <div class="col-md-8 mx-auto">
                <div class="metric-card">
                    <h4>📋 Introducción</h4>
                    <p>{{introduccion}}</p>
                </div>

                <div class="metric-card">
                    <h4>🎯 Objetivo</h4>
                    <p>{{objetivo}}</p>
                </div>

                <div class="row">
                    <div class="col-md-4">
                        <div class="metric-card text-center">
                            <h5>{{metrica1}}</h5>
                            <h3 class="text-primary">{{valor1}}</h3>
                            <span class="status-badge status-{{estado1_class}}">{{estado1}}</span>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="metric-card text-center">
                            <h5>{{metrica2}}</h5>
                            <h3 class="text-success">{{valor2}}</h3>
                            <span class="status-badge status-{{estado2_class}}">{{estado2}}</span>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="metric-card text-center">
                            <h5>{{metrica3}}</h5>
                            <h3 class="text-info">{{valor3}}</h3>
                            <span class="status-badge status-{{estado3_class}}">{{estado3}}</span>
                        </div>
                    </div>
                </div>

                <div class="metric-card">
                    <h4>💡 Análisis</h4>
                    <p>{{analisis}}</p>
                </div>

                <div class="metric-card">
                    <h4>🔍 Conclusiones</h4>
                    <p>{{conclusiones}}</p>
                </div>
            </div>
        </div>
    </div>

    <footer class="text-center mt-5 py-3 bg-light">
        <p class="mb-0">Generado automáticamente por Project Manager | {{fecha}} {{hora}}</p>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""
    }

def create_docx_template() -> Dict[str, Any]:
    """Create a DOCX template example."""
    return {
        "name": "Business Document",
        "extension": "docx",
        "description": "Professional Word document template",
        "content": """{{titulo}}

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

Métricas del Proyecto:
- {{metrica1}}: {{valor1}} ({{estado1}})
- {{metrica2}}: {{valor2}} ({{estado2}})
- {{metrica3}}: {{valor3}} ({{estado3}})

ANÁLISIS

{{analisis}}

CONCLUSIONES

{{conclusiones}}

---
Generado automáticamente por Project Manager
{{empresa}} | {{fecha}} | {{hora}}""",
        "styles": {
            "title": {"bold": True, "font_size": 18},
            "heading1": {"bold": True, "font_size": 16},
            "heading2": {"bold": True, "font_size": 14},
            "normal": {"font_size": 12}
        }
    }

def create_markdown_template() -> Dict[str, Any]:
    """Create a Markdown template example."""
    return {
        "name": "Technical Documentation",
        "extension": "md",
        "description": "Technical markdown documentation template",
        "content": """# {{titulo}}

**{{empresa}}**

*Fecha: {{fecha}} | Hora: {{hora}}*

---

## 📋 Tabla de Contenido

1. [Introducción](#introducción)
2. [Objetivo](#objetivo)
3. [Contenido](#contenido)
4. [Análisis](#análisis)
5. [Conclusiones](#conclusiones)

---

## Introducción

{{introduccion}}

## Objetivo

{{objetivo}}

## Contenido

### Métricas Principales

| Métrica | Valor | Estado |
|---------|-------|--------|
| {{metrica1}} | {{valor1}} | {{estado1}} |
| {{metrica2}} | {{valor2}} | {{estado2}} |
| {{metrica3}} | {{valor3}} | {{estado3}} |

### Análisis Detallado

{{analisis}}

## Conclusiones

{{conclusiones}}

---

*Este documento fue generado automáticamente por Project Manager*

*{{empresa}} | {{fecha}} | {{hora}}*"""
    }

def initialize_external_templates() -> None:
    """Initialize external templates with examples."""
    loader = ExternalTemplateLoader()

    templates = [
        create_excel_multi_sheet_template(),
        create_html_template(),
        create_docx_template(),
        create_markdown_template()
    ]

    for template in templates:
        extension = template['extension']
        success = loader.save_template(template, extension)
        if success:
            print(f"External template '{template['name']}' ({extension}) initialized.")
        else:
            print(f"Failed to initialize template '{template['name']}' ({extension}).")

def get_external_template_params(file_name: str) -> Dict[str, str]:
    """Get default parameters for external templates."""
    from datetime import datetime

    base_params = {
        # Basic info
        "titulo": "Documento Generado",
        "empresa": "Empresa Ejemplo",
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "hora": datetime.now().strftime("%H:%M:%S"),

        # Content sections
        "introduccion": "Este documento fue generado automáticamente desde una plantilla externa.",
        "objetivo": "Proporcionar información estructurada y profesional.",
        "analisis": "El análisis muestra resultados positivos en las métricas principales.",
        "conclusiones": "Las operaciones se desarrollan según lo planificado.",

        # Metrics
        "metrica1": "Productividad",
        "valor1": "85%",
        "estado1": "Activo",
        "metrica2": "Calidad",
        "valor2": "92%",
        "estado2": "Excelente",
        "metrica3": "Eficiencia",
        "valor3": "78%",
        "estado3": "Mejorable",

        # Status classes for HTML
        "estado1_class": "active",
        "estado2_class": "completed",
        "estado3_class": "pending",

        # Additional fields
        "version": "1.0",
        "autor": "Sistema Automático",
        "estado_general": "Operativo",
        "tendencia": "Estable",

        # Analysis fields
        "analisis1": "Muestra resultados positivos",
        "proyeccion2": "Se espera crecimiento del 15%",
        "recomendacion3": "Implementar mejoras de eficiencia",
        "tendencia1": "↗️ Ascendente",
        "tendencia2": "➡️ Estable",
        "tendencia3": "↘️ Descendente",

        # Calculations
        "total_general": "150",
        "promedio_general": "85.5",
        "maximo_general": "95"
    }

    # Customize based on file name
    file_lower = file_name.lower()

    if "dashboard" in file_lower or "principal" in file_lower:
        base_params.update({
            "titulo": "Dashboard Principal",
            "introduccion": "Panel de control principal con métricas clave del negocio.",
            "objetivo": "Proporcionar una visión general del estado actual de las operaciones.",
            "analisis": "El dashboard muestra indicadores positivos en productividad y calidad, con oportunidades de mejora en eficiencia.",
            "conclusiones": "El estado general del negocio es positivo con tendencias estables."
        })
    elif "financiera" in file_lower or "calculator" in file_lower:
        base_params.update({
            "titulo": "Calculadora Financiera",
            "metrica1": "Ingresos",
            "valor1": "$10,000",
            "metrica2": "Gastos",
            "valor2": "$7,500",
            "metrica3": "Utilidad",
            "valor3": "$2,500",
            "introduccion": "Análisis financiero y proyecciones económicas del proyecto.",
            "objetivo": "Calcular y analizar los indicadores financieros clave.",
            "analisis": "Los ingresos superan los gastos con una utilidad neta positiva.",
            "conclusiones": "La situación financiera es saludable con margen de beneficio adecuado."
        })
    elif "cliente" in file_lower or "customer" in file_lower:
        base_params.update({
            "titulo": "Base de Datos de Clientes",
            "metrica1": "Clientes Activos",
            "valor1": "150",
            "metrica2": "Nuevos Clientes",
            "valor2": "25",
            "metrica3": "Satisfacción",
            "valor3": "4.2/5",
            "introduccion": "Base de datos actualizada con información de clientes.",
            "objetivo": "Mantener información actualizada de la cartera de clientes.",
            "analisis": "Crecimiento positivo en la base de clientes con alta satisfacción.",
            "conclusiones": "La estrategia de captación de clientes está funcionando correctamente."
        })

    return base_params