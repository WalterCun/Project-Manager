# Diseño del Sistema de Plantillas Mejorado

## 🎯 Objetivo
Crear un sistema de plantillas flexible y extensible que permita:
- Cargar estructuras de proyecto desde archivos JSON
- Usar plantillas nativas DOCX/Excel con parámetros dinámicos
- Implementar templates web con Jinja2 para mayor legibilidad
- Sistema de validación y versionado

## 🏗️ Arquitectura General

### 1. Sistema de Carga de Estructuras
```
templates/structures/
├── default_business_structure.json
├── startup_structure.json
├── consulting_structure.json
└── custom_structure.json
```

**Formato JSON de Estructura:**
```json
{
  "name": "Default Business Structure",
  "description": "Complete business project structure",
  "version": "1.0",
  "author": "Project Manager",
  "structure": {
    "00_ADMINISTRATIVO": {
      "Información General": {},
      "Documentos Legales": {
        "contrato.docx": "Plantilla de contrato",
        "permisos.pdf": "Documentos de permisos"
      }
    }
  }
}
```

### 2. Sistema de Plantillas Nativas

#### Excel Templates (`templates/excel/`)
```json
{
  "name": "Multi-Sheet Dashboard",
  "extension": "xlsx",
  "sheets": {
    "Data": {
      "cells": {
        "A1": {"value": "{{titulo}}", "style": {"bold": true}},
        "B2": {"formula": "=SUM(B3:B10)"}
      },
      "tables": {
        "DataTable": {
          "range": "A1:D10",
          "headers": true,
          "style": {"header_fill": "0070C0"}
        }
      }
    }
  }
}
```

#### Word Templates (`templates/docx/`)
```json
{
  "name": "Business Document",
  "extension": "docx",
  "document": {
    "settings": {
      "page_size": "A4",
      "margins": {"top": 2.54, "bottom": 2.54}
    },
    "styles": {
      "title_style": {"font_size": 18, "bold": true},
      "normal_style": {"font_size": 12, "line_spacing": 1.5}
    },
    "sections": [
      {"type": "header", "content": "{{titulo}}", "style": "title_style"},
      {"type": "paragraph", "content": "{{contenido}}", "style": "normal_style"},
      {"type": "table", "headers": ["Col1", "Col2"], "rows": [["{{dato1}}", "{{dato2}}"]]}
    ]
  }
}
```

### 3. Sistema de Templates Web con Jinja2

#### HTML Templates (`templates/html/`)
```json
{
  "name": "Professional Report",
  "extension": "html",
  "framework": "bootstrap",
  "template_engine": "jinja2",
  "content": "<!DOCTYPE html>{% raw %}
<html>
<head>
    <title>{{titulo}}</title>
    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css\" rel=\"stylesheet\">
</head>
<body>
    <div class=\"container\">
        <h1>{{titulo}}</h1>
        <div class=\"row\">
        {% for item in items %}
            <div class=\"col-md-4\">
                <div class=\"card\">
                    <div class=\"card-body\">
                        <h5 class=\"card-title\">{{item.nombre}}</h5>
                        <p class=\"card-text\">{{item.descripcion}}</p>
                        <span class=\"badge bg-{{item.estado}}\">{{item.estado}}</span>
                    </div>
                </div>
            </div>
        {% endfor %}
        </div>
    </div>
</body>
</html>{% endraw %}"
}
```

## 🔧 Componentes del Sistema

### 1. StructureTemplateLoader
```python
class StructureTemplateLoader:
    def __init__(self, templates_dir: str = "templates/structures"):
        self.templates_dir = templates_dir
        self.templates = {}

    def load_templates(self) -> Dict[str, Dict]:
        """Load all structure templates from JSON files"""
        for file_path in Path(self.templates_dir).glob("*.json"):
            with open(file_path, 'r', encoding='utf-8') as f:
                template = json.load(f)
                self.templates[template['name']] = template
        return self.templates

    def get_template(self, name: str) -> Optional[Dict]:
        """Get specific template by name"""
        return self.templates.get(name)

    def list_templates(self) -> List[str]:
        """List all available template names"""
        return list(self.templates.keys())
```

### 2. Enhanced TemplateManager
```python
class EnhancedTemplateManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.structure_loader = StructureTemplateLoader()
        self.native_renderers = {
            'xlsx': ExcelNativeRenderer(),
            'docx': WordNativeRenderer(),
            'html': Jinja2Renderer()
        }

    def render_native_template(self, template_name: str, extension: str, params: Dict) -> bytes:
        """Render native template with parameters"""
        template_path = f"templates/{extension}/{template_name}.json"
        with open(template_path, 'r') as f:
            template_data = json.load(f)

        renderer = self.native_renderers[extension]
        return renderer.render(template_data, params)
```

### 3. Native Renderers

#### ExcelNativeRenderer
```python
class ExcelNativeRenderer:
    def render(self, template_data: Dict, params: Dict) -> bytes:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill

        wb = Workbook()

        for sheet_name, sheet_config in template_data.get('sheets', {}).items():
            ws = wb.create_sheet(sheet_name) if sheet_name != 'Sheet' else wb.active

            # Render cells
            for cell_ref, cell_config in sheet_config.get('cells', {}).items():
                cell = ws[cell_ref]
                value = self._render_value(cell_config['value'], params)
                cell.value = value

                # Apply styles
                if 'style' in cell_config:
                    self._apply_style(cell, cell_config['style'])

            # Render tables
            for table_name, table_config in sheet_config.get('tables', {}).items():
                self._create_table(ws, table_config)

            # Render charts
            for chart_name, chart_config in sheet_config.get('charts', {}).items():
                self._create_chart(ws, chart_config)

        # Save to bytes
        from io import BytesIO
        bio = BytesIO()
        wb.save(bio)
        return bio.getvalue()
```

#### WordNativeRenderer
```python
class WordNativeRenderer:
    def render(self, template_data: Dict, params: Dict) -> bytes:
        from docx import Document
        from docx.shared import Inches, Pt
        from docx.enum.text import WD_ALIGN_PARAGRAPH

        doc = Document()

        # Apply document settings
        settings = template_data.get('document', {}).get('settings', {})
        self._apply_document_settings(doc, settings)

        # Apply styles
        styles_config = template_data.get('document', {}).get('styles', {})
        self._apply_styles(doc, styles_config)

        # Render sections
        sections = template_data.get('document', {}).get('sections', [])
        for section in sections:
            self._render_section(doc, section, params)

        # Save to bytes
        from io import BytesIO
        bio = BytesIO()
        doc.save(bio)
        return bio.getvalue()
```

#### Jinja2Renderer
```python
class Jinja2Renderer:
    def render(self, template_data: Dict, params: Dict) -> str:
        from jinja2 import Template

        template_content = template_data['content']
        template = Template(template_content)
        return template.render(**params)
```

## 🔄 Flujo de Trabajo Mejorado

### 1. Creación de Proyecto con Estructura Personalizada
```bash
# Crear proyecto con estructura específica
project-manager create-project MiProyecto --structure default_business_structure

# Crear proyecto con estructura personalizada
project-manager create-project MiProyecto --structure-file custom_structure.json
```

### 2. Renderizado de Plantillas Nativas
```python
# Renderizar Excel con parámetros
params = {
    'titulo': 'Dashboard Q4',
    'empresa': 'Mi Empresa',
    'metrica1': 'Ventas',
    'valor1': 150000,
    'estado1': 'Excelente'
}
excel_bytes = template_manager.render_native_template('multi_sheet_dashboard', 'xlsx', params)

# Renderizar Word con parámetros
word_bytes = template_manager.render_native_template('business_document', 'docx', params)

# Renderizar HTML con Jinja2
html_content = template_manager.render_native_template('professional_report', 'html', params)
```

## ✅ Sistema de Validación

### TemplateValidator
```python
class TemplateValidator:
    def validate_structure_template(self, template: Dict) -> List[str]:
        """Validate structure template format"""
        errors = []

        required_fields = ['name', 'description', 'version', 'structure']
        for field in required_fields:
            if field not in template:
                errors.append(f"Missing required field: {field}")

        if 'structure' in template:
            if not isinstance(template['structure'], dict):
                errors.append("Structure must be a dictionary")
            else:
                errors.extend(self._validate_structure_hierarchy(template['structure']))

        return errors

    def validate_native_template(self, template: Dict, extension: str) -> List[str]:
        """Validate native template format"""
        errors = []

        # Extension-specific validation
        if extension == 'xlsx':
            errors.extend(self._validate_excel_template(template))
        elif extension == 'docx':
            errors.extend(self._validate_word_template(template))
        elif extension == 'html':
            errors.extend(self._validate_html_template(template))

        return errors
```

## 📋 CLI Mejorado

### Nuevos Comandos
```bash
# Listar estructuras disponibles
project-manager structures list

# Crear proyecto con estructura específica
project-manager create-project MiProyecto --structure "Default Business"

# Renderizar plantilla nativa
project-manager render-template multi_sheet_dashboard.xlsx --params titulo="Mi Dashboard" empresa="Mi Empresa"

# Validar plantilla
project-manager validate-template template.json
```

## 🔄 Migración del Sistema Actual

### Compatibilidad Hacia Atrás
- Mantener plantillas existentes en base de datos
- Sistema híbrido: DB + archivos JSON
- Migración gradual de plantillas existentes

### Actualización de Código Existente
```python
# En StructureGenerator.__init__
self.structure_templates = StructureTemplateLoader().load_templates()
self.enhanced_template_manager = EnhancedTemplateManager(self.db_manager)

# En create_structure
def create_structure(self, project_name: str, base_path: str, structure_name: str = None):
    if structure_name and structure_name in self.structure_templates:
        structure = self.structure_templates[structure_name]['structure']
    else:
        structure = self.default_structure

    # ... resto del código existente
```

## 🎯 Beneficios del Nuevo Sistema

1. **Flexibilidad**: Estructuras definidas en archivos JSON editables
2. **Mantenibilidad**: Plantillas versionadas y validadas
3. **Extensibilidad**: Fácil agregar nuevos tipos de plantillas
4. **Profesionalismo**: Templates nativos con formato avanzado
5. **Legibilidad**: Jinja2 para templates web complejos
6. **Rendimiento**: Carga eficiente de plantillas desde archivos

## 🚀 Implementación por Fases

### Fase 1: Sistema de Estructuras JSON
- ✅ Crear StructureTemplateLoader
- ✅ Implementar carga desde templates/structures/
- ✅ Actualizar CLI para selección de estructura

### Fase 2: Renderers Nativos
- 🔄 ExcelNativeRenderer con openpyxl
- 🔄 WordNativeRenderer con python-docx
- 🔄 Soporte completo de estilos y formatos

### Fase 3: Jinja2 Integration
- 🔄 Jinja2Renderer para templates HTML
- 🔄 Soporte de loops, conditionals, macros
- 🔄 Framework integration (Bootstrap, etc.)

### Fase 4: Sistema de Validación
- 🔄 TemplateValidator completo
- 🔄 Validación automática al cargar
- 🔄 Reportes de errores detallados

### Fase 5: CLI Enhancement
- 🔄 Nuevos comandos para gestión de plantillas
- 🔄 Interfaz mejorada para selección
- 🔄 Soporte batch processing