# Project Structure Manager 🚀

Un gestor avanzado de estructuras de proyectos empresariales con sistema de plantillas programables, motor de expresiones y arquitectura SOLID.

## ✨ Características Principales

### 📁 Gestión de Proyectos
- **Creación de Proyectos**: Define y guarda estructuras personalizadas en SQLite
- **Generación Automática**: Crea jerarquías completas de carpetas y archivos
- **Estructuras Predeterminadas**: 15+ carpetas principales para negocios
- **Import/Export JSON**: Comparte o respalda estructuras fácilmente
- **Escaneo de Directorios**: Captura estructuras existentes

### 🎨 Sistema de Plantillas Programables
- **Motor de Expresiones**: Procesa expresiones dinámicas con sintaxis `{{variable}}`
- **Funciones Integradas**: DATE, MATH, STRING, FORMAT, RANDOM, USER
- **Condicionales**: `{{#if}}`, `{{else}}`, `{{elif}}`
- **Loops**: `{{#for item in array}}`, `{{#for i in 1..10}}`
- **Switch/Case**: `{{#switch}}` con múltiples casos
- **Parámetros Dinámicos**: Personaliza plantillas con parámetros
- **Multi-Formato**: DOCX, XLSX, HTML, MD, TXT, PDF

### 🏗️ Arquitectura SOLID
- **Separación de Responsabilidades**: Módulos independientes (domain, repositories, services)
- **Motor de Plantillas**: Parser, Evaluator, Functions, Renderer separados
- **Escalable y Mantenible**: Fácil de extender sin modificar código existente

## 📦 Instalación

### Requisitos Previos
- Python 3.12+
- pip o uv para gestión de dependencias

### Instalación Rápida

```bash
# Clonar repositorio
git clone <repository-url>
cd BASE-DE-PROYECTO

# Instalar dependencias
pip install -e .

# O con uv
uv pip install -e .

# Verificar instalación
python __main__.py --help
```

### Dependencias Principales
- `sqlalchemy`: ORM para base de datos
- `python-docx`: Generación de documentos Word
- `openpyxl`: Generación de Excel
- `reportlab`: Conversión PDF
- `markdown`: Procesamiento Markdown

## 🎯 Uso Básico

### Crear Proyecto

```bash
# Crear con estructura predeterminada
python __main__.py create-project "Mi Empresa"

# Crear en ubicación específica
python __main__.py create-project "Mi Empresa" --path ./proyectos

# Usar estructura personalizada
python __main__.py create-project "Mi Empresa" --structure "Custom Structure"

# Forzar sobrescritura
python __main__.py create-project "Mi Empresa" --force

# Regenerar proyecto existente
python __main__.py create-project "Mi Empresa" --regenerate

# Reiniciar con estructura por defecto
python __main__.py create-project "Mi Empresa" --restart

# Convertir INFO.md a PDF
python __main__.py create-project "Mi Empresa" --convert-md-to-pdf all
```

### Listar Proyectos

```bash
python __main__.py list-projects
```

### Generar Estructura

```bash
python __main__.py generate-structure <project-id> <output-path>

# Ejemplo
python __main__.py generate-structure 1 ./mi-proyecto
```

### Import/Export

```bash
# Exportar a JSON
python __main__.py export-json 1 estructura.json

# Importar desde JSON
python __main__.py import-json "Proyecto Importado" estructura.json

# Escanear directorio existente
python __main__.py scan-directory "Proyecto Escaneado" ./directorio-existente
```

## 🎨 Sistema de Plantillas Programables

### Sintaxis de Expresiones

#### Variables Simples
```
{{empresa_nombre}}
{{fecha}}
{{usuario}}
```

#### Funciones

```
# Funciones de Fecha
{{DATE.now()}}                           # 2025-01-15 10:30:00
{{DATE.year()}}                          # 2025
{{DATE.format('DD/MM/YYYY')}}            # 15/01/2025

# Funciones Matemáticas
{{MATH.round(3.14159, 2)}}               # 3.14
{{MATH.sum(10, 20, 30)}}                 # 60
{{MATH.avg(10, 20, 30)}}                 # 20
{{MATH.percentage(25, 100)}}             # 25

# Funciones de String
{{STRING.upper('hola')}}                 # HOLA
{{STRING.lower('HOLA')}}                 # hola
{{STRING.capitalize('hola mundo')}}      # Hola mundo
{{STRING.replace('hola mundo', 'mundo', 'amigo')}}  # hola amigo

# Funciones de Formato
{{FORMAT.currency(1000)}}                # $1,000.00
{{FORMAT.number(1000000, 2)}}            # 1,000,000.00
{{FORMAT.phone('1234567890')}}           # (123) 456-7890
{{FORMAT.percent(0.75)}}                 # 75.0%

# Funciones Random
{{RANDOM.number(1, 100)}}                # Número aleatorio entre 1-100
{{RANDOM.uuid()}}                        # UUID único
{{RANDOM.string(10)}}                    # String aleatorio de 10 caracteres

# Funciones de Usuario
{{USER.name}}                            # Nombre del usuario
{{USER.email}}                           # Email del usuario
```

#### Condicionales

```
{{#if inversion_inicial > 100000}}
⚠️ **Nota:** Inversión alta requiere análisis detallado
{{/if}}

{{#if mercado_objetivo == 'B2B'}}
### Estrategia B2B
- Enfoque corporativo
{{else}}
### Estrategia B2C
- Marketing directo
{{/if}}

{{#if edad >= 18}}
Mayor de edad
{{elif edad >= 13}}
Adolescente
{{else}}
Menor de edad
{{/if}}
```

#### Loops

```
# Loop simple
{{#for i in 1..5}}
Iteración {{i}}
{{/for}}

# Loop con array
{{#for empleado in empleados}}
- {{empleado}}
{{/for}}

# Loop con key-value
{{#for key, value in configuracion}}
{{key}}: {{value}}
{{/for}}
```

#### Switch/Case

```
{{#switch tipo_negocio}}
  {{#case 'turismo'}}
  ### Servicios Turísticos
  - Tours guiados
  - Experiencias locales
  {{/case}}

  {{#case 'tecnología'}}
  ### Soluciones Tecnológicas
  - Desarrollo software
  - Consultoría IT
  {{/case}}

  {{#default}}
  ### Servicios Generales
  {{/default}}
{{/switch}}
```

### Ejemplo Completo de Plantilla

```json
{
  "plan_negocios": {
    "type": "docx",
    "parameters": {
      "empresa_nombre": {"type": "string", "default": "[EMPRESA]"},
      "industria": {"type": "string", "default": "servicios"},
      "mercado_objetivo": {"type": "select", "options": ["B2B", "B2C"], "default": "B2C"},
      "inversion_inicial": {"type": "number", "default": 50000},
      "equipo_size": {"type": "number", "default": 5}
    },
    "content_template": "# Plan de Negocios - {{empresa_nombre}}\n\n## Resumen Ejecutivo\n**Empresa:** {{empresa_nombre}}\n**Industria:** {{industria}}\n**Fecha:** {{DATE.format('DD/MM/YYYY')}}\n\n## Análisis de Mercado\n{{#if mercado_objetivo == 'B2B'}}\n### Estrategia B2B\n- Contratos largo plazo\n{{else}}\n### Estrategia B2C\n- Marketing digital\n{{/if}}\n\n## Estructura Financiera\nInversión: ${{FORMAT.currency(inversion_inicial)}}\n\n## Equipo Inicial\n{{#for i in 1..equipo_size}}\n### Posición {{i}}\n- Rol: [Definir]\n{{/for}}\n\n---\n*Generado: {{DATE.now()}}*"
  }
}
```

### Uso con Parámetros

```bash
# Crear proyecto con parámetros personalizados
python __main__.py create-project "Mi Empresa" \
  --param empresa_nombre="Tech Solutions S.A." \
  --param industria="tecnología" \
  --param mercado_objetivo="B2B" \
  --param inversion_inicial=150000 \
  --param equipo_size=10

# O usar archivo de configuración
python __main__.py create-project "Mi Empresa" --config params.json
```

**params.json:**
```json
{
  "empresa_nombre": "EcoTours Ecuador",
  "proyecto_tipo": "turismo",
  "industria": "turismo sostenible",
  "mercado_objetivo": "B2C",
  "inversion_inicial": 75000,
  "equipo_size": 8,
  "incluir_financiero": true,
  "años_proyeccion": 5
}
```

## 📂 Estructura del Proyecto

```
BASE-DE-PROYECTO/
├── __main__.py                  # Punto de entrada CLI
├── pyproject.toml               # Configuración y dependencias
├── project-manager.db           # Base de datos SQLite
├── README.md                    # Esta documentación
│
├── src/
│   ├── cli/
│   │   ├── commands.py          # Comandos CLI
│   │   └── __init__.py
│   │
│   ├── core/
│   │   ├── database.py          # Gestión BD
│   │   ├── structure_generator.py  # Generador principal
│   │   ├── enhanced_template_manager.py
│   │   ├── template_loader.py
│   │   ├── external_templates.py
│   │   ├── base_templates.py
│   │   ├── native_renderers.py
│   │   │
│   │   ├── domain/              # Entidades de dominio
│   │   ├── repositories/        # Repositorios (acceso datos)
│   │   ├── services/            # Servicios de negocio
│   │   ├── builders/            # Builders para construcción
│   │   │
│   │   └── template_engine/     # Motor de plantillas programables
│   │       ├── parser.py        # Parser de expresiones
│   │       ├── evaluator.py     # Evaluador de condicionales
│   │       ├── functions.py     # Funciones integradas
│   │       └── renderer.py      # Renderizador final
│   │
│   └── templates/
│       ├── models.py            # Gestión de plantillas
│       ├── renderers.py         # Renderizadores por formato
│       └── cli.py               # CLI de plantillas
│
├── templates/
│   ├── structures/
│   │   ├── default_business_structure.json
│   │   └── content/
│   │       ├── folder_descriptions.json    # INFO.md carpetas
│   │       ├── file_templates.json         # Plantillas archivos
│   │       └── template_functions.json     # Definición funciones
│   │
│   ├── docx/                    # Plantillas DOCX
│   ├── excel/                   # Plantillas Excel
│   ├── html/                    # Plantillas HTML
│   ├── md/                      # Plantillas Markdown
│   └── xlsx/                    # Plantillas XLSX
│
└── tests/
    ├── test_core.py
    ├── test_cli.py
    ├── test_edge_cases.py
    └── templates/
        └── test_models.py
```

## 🏗️ Arquitectura SOLID

### Principios Aplicados

1. **Single Responsibility (SRP)**
   - Cada clase tiene una única responsabilidad
   - `TemplateParser`: Solo parsea
   - `ExpressionEvaluator`: Solo evalúa
   - `TemplateFunctions`: Solo ejecuta funciones
   - `TemplateRenderer`: Solo renderiza

2. **Open/Closed (OCP)**
   - Extensible sin modificar código existente
   - Nuevas funciones se agregan sin cambiar `TemplateFunctions`
   - Nuevos renderers sin modificar `RendererFactory`

3. **Liskov Substitution (LSP)**
   - Renderers intercambiables
   - Repositorios intercambiables

4. **Interface Segregation (ISP)**
   - Interfaces específicas por responsabilidad
   - No interfaces gordas

5. **Dependency Inversion (DIP)**
   - Dependencias a abstracciones, no implementaciones
   - Inyección de dependencias en constructores

## 🎯 Estructura Empresarial Predeterminada

### Carpetas Principales

1. **00 ADMINISTRATIVO**: Información general, documentos legales, contratos, propiedad intelectual
2. **01 ESTRATÉGICO**: Visión/misión, business model, análisis mercado, roadmap, KPIs
3. **02 LEGAL Y CONSTITUCIÓN**: RUC, permisos, seguros, acuerdos socios, términos
4. **03 OPERACIONES**: Manuales, procesos, protocolos, control proveedores, calidad
5. **04 COMERCIAL Y VENTAS**: Manual ventas, scripts, objeciones, precios, promociones
6. **05 MARKETING Y CONTENIDO**: Plan marketing, calendario, brand, contenido, diseños
7. **06 CLIENTES Y USUARIOS**: CRM, comunicación, contratos, feedback, fidelización
8. **07 FINANZAS Y CONTABILIDAD**: Balance, presupuesto, gastos/ingresos, flujo caja
9. **08 RECURSOS HUMANOS Y EQUIPO**: Organigrama, roles, KPIs, cultura, contratos
10. **09 CAPACITACIÓN Y DOCUMENTACIÓN**: Manuales inducción, guías, capacitación
11. **10 ANALÍTICA Y REPORTES**: Dashboards, reportes periódicos, KPIs globales
12. **11 TECNOLOGÍA E IT**: Infraestructura, licencias, backup, seguridad
13. **12 GESTIÓN DE RIESGOS**: Matriz riesgos, contingencia, auditorías, compliance
14. **13 INNOVACIÓN Y DESARROLLO**: Proyectos I+D, POCs, pilotos, alianzas
15. **14 SOSTENIBILIDAD Y RSE**: Responsabilidad social, sostenibilidad, reportes
16. **15 ARCHIVO HISTÓRICO**: Documentos históricos, proyectos cerrados

Cada carpeta incluye:
- ✅ Archivo `INFO.md` con descripción detallada
- ✅ Subcarpetas organizadas por tema
- ✅ Archivos de plantilla pre-generados

## 🔧 Desarrollo

### Ejecutar en Modo Desarrollo

```bash
# Activar entorno virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instalar en modo editable
pip install -e .

# Ejecutar
python __main__.py create-project "Test"
```

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/test_core.py
pytest tests/templates/test_models.py

# Con coverage
pytest --cov=src tests/
```

### Agregar Nuevas Funciones al Motor

```python
# En src/core/template_engine/functions.py

class TemplateFunctions:
    def custom_function(self, param1, param2):
        """Tu nueva función."""
        return param1 + param2
```

Uso en plantilla:
```
{{CUSTOM.function(10, 20)}}
```

### Renderizado de Plantillas (nuevo)

El antiguo sistema basado en RendererFactory fue retirado. Ahora existen dos flujos:

- Plantillas en base de datos (texto con placeholders) → se renderizan a texto y se escriben directamente a archivo.
- Plantillas externas nativas (docx, xlsx, html) → se renderizan con los renderers nativos desde src/core/native_renderers.py a través de EnhancedTemplateManager.

Ejemplo de uso programático:

```python
from src.core.database import DatabaseManager
from src.core.enhanced_template_manager import EnhancedTemplateManager

db = DatabaseManager()
etm = EnhancedTemplateManager(db)

# Renderizar plantilla nativa desde archivo JSON (templates/html/Professional Report.json)
params = {"titulo": "Reporte", "empresa": "ACME"}
html_bytes_or_str = etm.render_native_template("Professional Report", "html", params)

# O renderizar desde un diccionario ya cargado (sin tocar disco)
template_data = {"content": "<h1>{{titulo}}</h1>", "extension": "html"}
rendered = etm.render_template_from_data(template_data, "html", params)
```

## 📝 Ejemplos Avanzados

### Plantilla con Lógica Compleja

```
# Manual de Empleado - {{empresa_nombre}}

## Información Personal
Nombre: {{empleado_nombre}}
Cargo: {{cargo}}
Fecha Ingreso: {{DATE.format('DD/MM/YYYY')}}

## Compensación
Salario Base: ${{FORMAT.currency(salario_base)}}

{{#if cargo == 'Gerente'}}
Bono Anual: ${{FORMAT.currency(MATH.round(salario_base * 0.20, 2))}}
{{elif cargo == 'Supervisor'}}
Bono Anual: ${{FORMAT.currency(MATH.round(salario_base * 0.10, 2))}}
{{/if}}

## Beneficios
{{#for beneficio in beneficios}}
- {{beneficio}}
{{/for}}

## Políticas Aplicables
{{#switch departamento}}
  {{#case 'Ventas'}}
  - Comisiones por venta
  - Gastos de representación
  {{/case}}
  {{#case 'IT'}}
  - Equipo de cómputo
  - Capacitación técnica
  {{/case}}
  {{#default}}
  - Beneficios estándar
  {{/default}}
{{/switch}}

---
Generado: {{DATE.now()}}
Código: {{STRING.upper(empresa_nombre)}}-{{DATE.year()}}-{{RANDOM.number(1000, 9999)}}
```

## 🤝 Contribuir

1. Fork el repositorio
2. Crea branch: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -am 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crea Pull Request

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles

## 💡 Soporte

- **Issues**: [GitHub Issues](https://github.com/tu-repo/issues)
- **Documentación**: Este README
- **Email**: soporte@proyecto.com

## 🎉 Créditos

Desarrollado con ❤️ para facilitar la gestión de proyectos empresariales

---

**Versión**: 2.0.0
**Última Actualización**: Enero 2025
**Estado**: ✅ Producción
