# Sistema de Plantillas del Project Manager

Esta carpeta contiene todas las plantillas del sistema organizadas por tipo y funcionalidad.

## 📁 Estructura de Carpetas

```
templates/
├── structures/          # Estructuras de proyecto JSON
├── excel/              # Plantillas Excel nativas
├── docx/               # Plantillas Word nativas
├── html/               # Plantillas web con Jinja2
├── md/                 # Plantillas Markdown
├── json/               # Configuraciones JSON
└── xlsx/               # Alias para Excel
```

## 🎯 Tipos de Plantillas

### 1. Estructuras de Proyecto (`structures/`)
**Propósito**: Definir la organización completa de carpetas y archivos
**Formato**: JSON con estructura jerárquica
**Ejemplo**: `default_business_structure.json`

### 2. Plantillas Nativas Excel (`excel/`)
**Propósito**: Documentos Excel con formato profesional
**Características**:
- Múltiples hojas de cálculo
- Gráficos y tablas dinámicas
- Estilos y formatos avanzados
- Parámetros personalizables

### 3. Plantillas Nativas Word (`docx/`)
**Propósito**: Documentos Word con diseño profesional
**Características**:
- Estructura de documento completa
- Tablas, listas y estilos
- Encabezados y pies de página
- Contenido dinámico

### 4. Plantillas Web (`html/`)
**Propósito**: Reportes web responsivos
**Características**:
- Bootstrap/CSS frameworks
- Diseño responsivo
- Interactividad con JavaScript
- Templates Jinja2

### 5. Plantillas Markdown (`md/`)
**Propósito**: Documentación técnica
**Características**:
- Formato Markdown puro
- Estructura clara y legible
- Fácil conversión a otros formatos

## 🔧 Sistema de Parámetros

Todas las plantillas soportan parámetros dinámicos usando sintaxis `{{parametro}}`:

### Parámetros Comunes
- `{{titulo}}` - Título del documento
- `{{empresa}}` - Nombre de la empresa
- `{{fecha}}` - Fecha de generación
- `{{hora}}` - Hora de generación
- `{{autor}}` - Autor del documento

### Parámetros Específicos por Tipo
- **Excel**: `{{metrica1}}`, `{{valor1}}`, `{{estado1}}`
- **Word**: `{{introduccion}}`, `{{objetivo}}`, `{{conclusiones}}`
- **HTML**: `{{estado1_class}}` (para clases CSS)

## 🚀 Uso del Sistema

### Carga Automática
```python
# El sistema carga automáticamente todas las plantillas
template_manager = TemplateManager(db_manager)
templates = template_manager.list_templates()
```

### Renderizado
```python
# Renderizar con parámetros
params = {
    'titulo': 'Mi Reporte',
    'empresa': 'Mi Empresa',
    'fecha': '2024-01-15'
}
content = template_manager.render_template(template, params)
```

### Validación
```python
# Validar estructura de plantilla
validator = TemplateValidator()
is_valid = validator.validate_structure(template_data)
```

## 📋 Creación de Nuevas Plantillas

### 1. Estructura de Proyecto
```json
{
  "name": "Mi Estructura",
  "description": "Descripción",
  "version": "1.0",
  "structure": {
    "Carpeta1": {
      "Subcarpeta": {},
      "archivo.txt": "Descripción"
    }
  }
}
```

### 2. Plantilla Excel
```json
{
  "name": "Mi Dashboard",
  "extension": "xlsx",
  "sheets": {
    "Data": {
      "cells": {
        "A1": {"value": "{{titulo}}", "style": {"bold": true}}
      }
    }
  }
}
```

### 3. Plantilla Word
```json
{
  "name": "Mi Documento",
  "extension": "docx",
  "document": {
    "sections": [
      {"type": "header", "content": "{{titulo}}"}
    ]
  }
}
```

## 🔍 Sistema de Búsqueda

El sistema busca plantillas por:
- **Nombre exacto**: `plantilla.docx`
- **Extensión**: `.xlsx`, `.docx`
- **Tipo**: `reporte`, `dashboard`, `documento`

## ✅ Validación y Versionado

- **Validación automática** al cargar plantillas
- **Versionado semántico** (1.0, 1.1, 2.0)
- **Metadata completa** (autor, descripción, fecha)
- **Compatibilidad hacia atrás** mantenida

## 🛠️ Mantenimiento

### Actualización de Plantillas
1. Modificar archivo JSON
2. Incrementar versión
3. Probar con datos de ejemplo
4. Actualizar documentación

### Agregar Nuevos Tipos
1. Crear subcarpeta en `templates/`
2. Implementar renderer específico
3. Actualizar sistema de carga
4. Documentar nuevo tipo

## 📚 Referencias

- [JSON Schema](https://json-schema.org/) para validación
- [Jinja2](https://jinja.palletsprojects.com/) para templates web
- [python-docx](https://python-docx.readthedocs.io/) para Word
- [openpyxl](https://openpyxl.readthedocs.io/) para Excel