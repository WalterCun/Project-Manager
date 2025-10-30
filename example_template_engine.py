"""
Ejemplo de uso del motor de plantillas programables.

Este script demuestra cómo usar el nuevo motor de plantillas con:
- Variables simples
- Funciones (DATE, MATH, STRING, FORMAT, etc)
- Condicionales (if/else/elif)
- Loops (for)
- Switch/case
"""

from src.core.template_engine import TemplateRenderer

def ejemplo_basico():
    """Ejemplo básico con variables y funciones."""
    print("="*60)
    print("EJEMPLO 1: Variables y Funciones")
    print("="*60)

    template = """
# Resumen Ejecutivo - {{empresa_nombre}}

**Fecha:** {{DATE.format('DD/MM/YYYY')}}
**Año Fiscal:** {{DATE.year()}}

## Información del Proyecto
Empresa: {{empresa_nombre}}
Industria: {{industria}}
Inversión: ${{FORMAT.currency(inversion)}}

## Código de Proyecto
{{STRING.upper(empresa_nombre)}}-{{DATE.year()}}-{{RANDOM.number(1000, 9999)}}
"""

    params = {
        'empresa_nombre': 'Tech Solutions S.A.',
        'industria': 'Tecnología',
        'inversion': 150000
    }

    renderer = TemplateRenderer(params)
    resultado = renderer.render(template)
    print(resultado)
    print()


def ejemplo_condicionales():
    """Ejemplo con condicionales."""
    print("="*60)
    print("EJEMPLO 2: Condicionales")
    print("="*60)

    template = """
# Plan de Negocios - {{empresa}}

## Análisis de Mercado
Mercado Objetivo: {{mercado}}

{{#if mercado == 'B2B'}}
### Estrategia B2B
- Enfoque en empresas corporativas
- Contratos a largo plazo
- Ventas consultivas
{{else}}
### Estrategia B2C
- Marketing digital directo
- Redes sociales y e-commerce
- Ventas directas al consumidor
{{/if}}

## Análisis de Inversión
Inversión Inicial: ${{FORMAT.currency(inversion)}}

{{#if inversion > 100000}}
⚠️ **Nota Importante:**
Inversión alta - Se requiere:
- Análisis de riesgo detallado
- Plan de contingencia
- Aprobación del comité ejecutivo
{{elif inversion > 50000}}
📊 **Nota:** Inversión moderada - Requiere análisis financiero estándar
{{else}}
✅ **Nota:** Inversión baja - Proceso de aprobación simplificado
{{/if}}
"""

    # Caso 1: B2B con inversión alta
    print("\n--- Caso 1: B2B, Inversión Alta ---")
    params1 = {'empresa': 'Corp Solutions', 'mercado': 'B2B', 'inversion': 150000}
    renderer1 = TemplateRenderer(params1)
    print(renderer1.render(template))

    # Caso 2: B2C con inversión moderada
    print("\n--- Caso 2: B2C, Inversión Moderada ---")
    params2 = {'empresa': 'Consumer Tech', 'mercado': 'B2C', 'inversion': 75000}
    renderer2 = TemplateRenderer(params2)
    print(renderer2.render(template))


def ejemplo_loops():
    """Ejemplo con loops."""
    print("="*60)
    print("EJEMPLO 3: Loops")
    print("="*60)

    template = """
# Estructura de Equipo - {{empresa}}

## Posiciones a Contratar

{{#for i in 1..5}}
### Posición {{i}}
- **Rol:** [Por definir]
- **Departamento:** [Asignar]
- **Prioridad:** {{#if i <= 2}}Alta{{else}}Media{{/if}}
- **Código:** POS-{{DATE.year()}}-{{i}}

{{/for}}

## Lista de Empleados Actuales

{{#for empleado in empleados}}
- {{empleado}} (Activo desde {{DATE.year()}})
{{/for}}

## Departamentos y Responsables

{{#for dept, responsable in departamentos}}
**{{dept}}:** {{responsable}}
{{/for}}
"""

    params = {
        'empresa': 'Mi Empresa S.A.',
        'empleados': ['Juan Pérez', 'María García', 'Carlos López'],
        'departamentos': {
            'Ventas': 'Ana Martínez',
            'Marketing': 'Pedro Sánchez',
            'Operaciones': 'Laura Fernández'
        }
    }

    renderer = TemplateRenderer(params)
    print(renderer.render(template))


def ejemplo_switch():
    """Ejemplo con switch/case."""
    print("="*60)
    print("EJEMPLO 4: Switch/Case")
    print("="*60)

    template = """
# Manual de Beneficios - {{empresa}}

## Empleado: {{empleado}}
**Cargo:** {{cargo}}
**Departamento:** {{departamento}}

## Beneficios Según Departamento

{{#switch departamento}}
  {{#case 'Ventas'}}
  ### Beneficios de Ventas
  - Comisiones por venta (hasta 15%)
  - Gastos de representación
  - Bono trimestral por cumplimiento de metas
  - Vehículo de la empresa
  {{/case}}

  {{#case 'IT'}}
  ### Beneficios de IT
  - Equipo de cómputo de última generación
  - Capacitación técnica continua
  - Certificaciones pagadas por la empresa
  - Home office flexible
  {{/case}}

  {{#case 'Marketing'}}
  ### Beneficios de Marketing
  - Budget para eventos y networking
  - Herramientas de diseño premium
  - Capacitación en marketing digital
  - Horario flexible
  {{/case}}

  {{#default}}
  ### Beneficios Estándar
  - Seguro médico
  - Bonificación anual
  - Vacaciones pagadas
  - Desarrollo profesional
  {{/default}}
{{/switch}}

## Compensación
Salario Base: ${{FORMAT.currency(salario)}}
{{#if cargo == 'Gerente'}}
Bono Anual (20%): ${{FORMAT.currency(MATH.round(salario * 0.20, 2))}}
{{elif cargo == 'Supervisor'}}
Bono Anual (10%): ${{FORMAT.currency(MATH.round(salario * 0.10, 2))}}
{{else}}
Bono Anual (5%): ${{FORMAT.currency(MATH.round(salario * 0.05, 2))}}
{{/if}}

---
**Generado:** {{DATE.now()}}
**Código:** {{STRING.upper(departamento)}}-{{DATE.year()}}-{{RANDOM.string(6)}}
"""

    # Caso 1: Empleado de Ventas
    print("\n--- Caso 1: Departamento de Ventas ---")
    params1 = {
        'empresa': 'Ventas Corp',
        'empleado': 'Juan Pérez',
        'cargo': 'Gerente',
        'departamento': 'Ventas',
        'salario': 3000
    }
    renderer1 = TemplateRenderer(params1)
    print(renderer1.render(template))

    # Caso 2: Empleado de IT
    print("\n--- Caso 2: Departamento de IT ---")
    params2 = {
        'empresa': 'Tech Solutions',
        'empleado': 'María García',
        'cargo': 'Desarrollador',
        'departamento': 'IT',
        'salario': 2500
    }
    renderer2 = TemplateRenderer(params2)
    print(renderer2.render(template))


def ejemplo_completo():
    """Ejemplo completo combinando todas las características."""
    print("="*60)
    print("EJEMPLO 5: Template Completo")
    print("="*60)

    template = """
# Plan de Negocios Completo
## {{empresa_nombre}}

**Fecha de Creación:** {{DATE.format('DD/MM/YYYY')}}
**Versión:** 1.0

---

## 1. Resumen Ejecutivo

{{empresa_nombre}} es una empresa dedicada al sector de {{industria}}.
Con una inversión inicial de ${{FORMAT.currency(inversion)}}, buscamos
{{#if mercado == 'B2B'}}establecer relaciones comerciales a largo plazo
con empresas corporativas{{else}}llegar directamente al consumidor final
a través de canales digitales{{/if}}.

{{#if inversion > 100000}}
### ⚠️ Inversión Alta
Esta inversión requiere aprobación especial y análisis de riesgo exhaustivo.
**ROI Proyectado:** {{MATH.percentage(roi_esperado, inversion)}}%
{{/if}}

---

## 2. Estructura del Equipo

Planeamos iniciar con un equipo de {{equipo_size}} personas:

{{#for i in 1..equipo_size}}
**Posición {{i}}:**
- Código: {{STRING.upper(empresa_nombre)}}-POS-{{i}}
- Estado: {{#if i <= 2}}Contratado{{else}}En proceso{{/if}}
- Prioridad: {{#if i <= 3}}Alta{{else}}Media{{/if}}

{{/for}}

---

## 3. Proyecciones Financieras

### Inversión y Retorno
- Inversión Inicial: ${{FORMAT.currency(inversion)}}
- ROI Esperado: ${{FORMAT.currency(roi_esperado)}}
- Período de Retorno: {{años_proyeccion}} años

### Proyección por Año
{{#for año in 1..años_proyeccion}}
**Año {{año}}:**
- Ingresos Proyectados: ${{FORMAT.currency(MATH.round(inversion * 1.15 * año, 2))}}
- Crecimiento: {{MATH.percentage(15 * año, 100)}}%

{{/for}}

---

## 4. Estrategia por Mercado

{{#switch mercado}}
  {{#case 'B2B'}}
  ### Estrategia Business-to-Business

  **Enfoque Principal:**
  - Ventas consultivas y relaciones a largo plazo
  - Contratos corporativos multi-año
  - Servicio personalizado por cuenta

  **Canales:**
  - LinkedIn y networking profesional
  - Ferias y eventos de industria
  - Referencias y partnerships

  {{/case}}

  {{#case 'B2C'}}
  ### Estrategia Business-to-Consumer

  **Enfoque Principal:**
  - Marketing digital y redes sociales
  - E-commerce y ventas directas
  - Experiencia de usuario optimizada

  **Canales:**
  - Redes sociales (Instagram, Facebook, TikTok)
  - Google Ads y SEO
  - Influencer marketing

  {{/case}}

  {{#default}}
  ### Estrategia Mixta

  Combinaremos elementos de B2B y B2C según oportunidades del mercado.
  {{/default}}
{{/switch}}

---

## 5. Indicadores Clave

| Métrica | Valor | Objetivo Año 1 |
|---------|-------|----------------|
| Inversión | ${{FORMAT.currency(inversion)}} | - |
| ROI Esperado | {{FORMAT.percent(MATH.round(roi_esperado / inversion, 2))}} | 15% |
| Equipo | {{equipo_size}} personas | {{equipo_size + 3}} personas |
| Mercado | {{mercado}} | Expansión |

---

## 6. Conclusión

Con base en el análisis presentado, {{empresa_nombre}} está bien
posicionada para {{#if inversion > 100000}}convertirse en un
líder del mercado{{else}}establecer una presencia sólida{{/if}}
en el sector de {{industria}}.

{{#if años_proyeccion >= 5}}
**Visión a Largo Plazo:** Con una proyección de {{años_proyeccion}} años,
esperamos alcanzar un crecimiento sostenido y generar valor significativo
para nuestros stakeholders.
{{/if}}

---

**Documento Generado Automáticamente**
- Fecha: {{DATE.now()}}
- Usuario: {{USER.name}}
- Código: {{STRING.upper(empresa_nombre)}}-PLAN-{{DATE.year()}}-{{RANDOM.uuid()}}
- Versión: 1.0
"""

    params = {
        'empresa_nombre': 'Innovatech Solutions',
        'industria': 'Tecnología e Innovación',
        'mercado': 'B2B',
        'inversion': 250000,
        'roi_esperado': 50000,
        'años_proyeccion': 5,
        'equipo_size': 8
    }

    renderer = TemplateRenderer(params)
    resultado = renderer.render(template)
    print(resultado)


if __name__ == '__main__':
    print("\n" + "="*60)
    print("DEMO: Motor de Plantillas Programables")
    print("="*60 + "\n")

    ejemplo_basico()
    input("Presiona Enter para continuar...")

    ejemplo_condicionales()
    input("Presiona Enter para continuar...")

    ejemplo_loops()
    input("Presiona Enter para continuar...")

    ejemplo_switch()
    input("Presiona Enter para continuar...")

    ejemplo_completo()

    print("\n" + "="*60)
    print("FIN DE LA DEMO")
    print("="*60)
