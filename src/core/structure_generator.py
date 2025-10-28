import os
from typing import Dict, Any, Optional, List
from .database import DatabaseManager
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from templates.models import TemplateManager
from templates.renderers import RendererFactory
from .base_templates import get_template_params_for_file


class StructureGenerator:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.default_structure = self._get_default_structure()

        self.template_manager = TemplateManager(db_manager)
        self.folder_descriptions = self._get_folder_descriptions()

    @staticmethod
    def _get_default_structure() -> Dict[str, Any]:
        # Integrated from generate_architecture.py with improvements
        return {
            "00 ADMINISTRATIVO": {
                "Información General del Proyecto": [
                    "Resumen_Ejecutivo.docx",
                    "Ficha_Técnica_Proyecto.docx",
                    "Datos_Contacto_Equipo.docx",
                    "Cronograma_Global.xlsx",
                    "Presentación_Corporativa.pptx"
                ],
                "Contratos - Acuerdos": [
                    "Contrato_Servicios.docx",
                    "Contrato_Confidencialidad_NDA.docx",
                    "Acuerdo_Colaboración.docx"
                ],
                "Documentos de Propiedad Intelectual": [
                    "Registro_Marca.pdf",
                    "Derechos_Autor.pdf",
                    "Patentes_y_Modelos_Utilidad.pdf"
                ],
                "Correspondencia Oficial - Ofertas - Licencias": [
                    "Carta_Presentación.docx",
                    "Solicitud_Licencia.docx",
                    "Ofertas_Comerciales.docx"
                ]
            },
            "01 ESTRATÉGICO": {
                "Visión - Misión - Valores": [
                    "Declaración_Estrategica.docx"
                ],
                "Business Model Canvas": [
                    "Canvas_Modelo_Negocio.pdf",
                    "Propuesta_Valor.docx"
                ],
                "Plan de Negocios": [
                    "Plan_Negocio_Completo.docx",
                    "Resumen_Ejecutivo.pdf"
                ],
                "Análisis de Mercado y Competencia": [
                    "Estudio_Mercado.pdf",
                    "Competencia_Directa_Indirecta.xlsx",
                    "Benchmarking.docx"
                ],
                "Roadmap Estratégico (Anual - Semestral)": [
                    "Roadmap_2025.xlsx",
                    "Metas_Trimestrales.docx"
                ],
                "Objetivos y KPIs": [
                    "OKRs_Globales.xlsx",
                    "Indicadores_Estrategicos.docx"
                ],
                "Proyecciones Financieras": [
                    "Proyeccion_5_Años.xlsx",
                    "Escenarios_Optimista_Pesimista.xlsx"
                ]
            },
            "02 LEGAL Y CONSTITUCIÓN": {
                "RUC y documentos fiscales": [
                    "Certificado_RUC.pdf",
                    "Constancia_Inscripción.pdf"
                ],
                "Permisos de Operaciones": [
                    "Permiso_Municipal.pdf",
                    "Certificado_Seguridad.pdf"
                ],
                "Póliza de Seguros": [
                    "Seguro_Responsabilidad_Civil.pdf",
                    "Seguro_Equipo.pdf"
                ],
                "Acuerdo entre Socios Fundadores": [
                    "Pacto_Socios.docx",
                    "Acta_Constitución.pdf"
                ],
                "Términos y Condiciones Clientes": [
                    "Términos_Servicio.docx",
                    "Política_Privacidad.docx"
                ],
                "Contrato Servicios (Cliente)": [
                    "Plantilla_Contrato_Cliente.docx"
                ],
                "Waiver - Liberación Responsabilidad": [
                    "Documento_Waiver.docx"
                ],
                "Plantilla Contrato Proveedores": [
                    "Plantilla_Proveedor.docx"
                ]
            },
            "03 OPERACIONES": {
                "Manuales": [
                    "Manual_Operativo.docx",
                    "Guía_Logística.docx"
                ],
                "Procesos": [
                    "Mapa_Procesos.pdf",
                    "Procedimientos_Operativos_Estandar.docx"
                ],
                "Protocolos y Checklists": [
                    "Checklist_Control_Calidad.xlsx",
                    "Protocolo_Seguridad.docx"
                ],
                "Control de Proveedores": [
                    "Base_Proveedores.xlsx",
                    "Evaluación_Proveedores.xlsx"
                ],
                "Manual de Calidad - Estándares": [
                    "Normas_ISO_Requeridas.pdf",
                    "Manual_Calidad.docx"
                ],
                "Calendario Operativo - Cronogramas": [
                    "Cronograma_Mensual.xlsx",
                    "Plan_Actividades_Semanales.xlsx"
                ]
            },
            "04 COMERCIAL Y VENTAS": {
                "Manual de Ventas": [
                    "Proceso_Ventas.docx"
                ],
                "Scripts de Venta WhatsApp": [
                    "Mensajes_Promocionales.docx"
                ],
                "Respuestas a Objeciones Comunes": [
                    "Listado_Objeciones.docx"
                ],
                "Política de Precios y Descuentos": [
                    "Lista_Precios.xlsx",
                    "Política_Descuentos.docx"
                ],
                "Paquetes y Promociones Vigentes": [
                    "Promociones_2025.xlsx"
                ],
                "Calculadora de Costos": [
                    "Costeo_Productos.xlsx"
                ],
                "Análisis de Rentabilidad": [
                    "Rentabilidad_Lineas_Negocio.xlsx"
                ],
                "Plantillas Propuestas Corporativas": [
                    "Plantilla_Propuesta_Corporativa.docx"
                ],
                "Base de Datos de Clientes": [
                    "Base_de_Datos_Clientes.xlsx"
                ]
            },
            "05 MARKETING Y CONTENIDO": {
                "Plan de Marketing": [
                    "Plan_Marketing_Anual.docx"
                ],
                "Calendario Editorial": [
                    "Calendario_Contenido.xlsx"
                ],
                "Guía de Marca (Brand Guidelines)": [
                    "Manual_Marca.pdf",
                    "Paleta_Colores.png",
                    "Tipografías.pdf"
                ],
                "Banco de Contenido (Posts pre-creados)": {
                    "Material Promocional": [
                        "Banners.jpg",
                        "Post_Instagram.docx"
                    ],
                    "Diseños": [
                        "Flyers.png",
                        "Plantillas_Canva.pdf"
                    ],
                    "Plantillas": [
                        "Plantilla_Post_Redes.docx",
                        "Plantilla_Reel.docx"
                    ]
                },
                "Estrategia Comercial": [
                    "Campañas_Promocionales.docx",
                    "Buyer_Personas.docx"
                ],
                "Plantillas de Diseño": [
                    "Plantillas_Canales_Sociales.zip"
                ],
                "Análisis de Mercado y Competencia": [
                    "Analisis_Redes.xlsx",
                    "Benchmark_Marketing.docx"
                ],
                "Reportes de Marketing": [
                    "Reporte_Mensual.pdf",
                    "Reporte_Anual.pdf"
                ]
            },
            "06 CLIENTES Y USUARIOS": {
                "CRM": {
                    "Base de Datos - CRM": [
                        "Clientes_Activos.xlsx",
                        "Historial_Interacciones.xlsx"
                    ]
                },
                "Plantillas de Comunicación": {
                    "Emails Templates": [
                        "Confirmación.html",
                        "Recordatorio_48h.html",
                        "Recordatorio_24h.html",
                        "Recordatorio_Día.html",
                        "Agradecimiento_Post_Venta.html",
                        "Solicitud_Review.html",
                        "Newsletter_Mensual.html"
                    ],
                    "Whatsapp": [
                        "Respuestas_Rápidas.docx",
                        "Mensajes_Automáticos.docx"
                    ]
                },
                "Contratos o Acuerdos con Clientes": [
                    "Contrato_Servicio_Cliente.docx"
                ],
                "Formulario de Feedback": [
                    "Encuesta_Satisfacción.docx",
                    "Formulario_Google_Link.txt"
                ],
                "Registro de Reviews y Testimonios": [
                    "Testimonios_Clientes.xlsx"
                ],
                "Programa de Fidelización y Referidos": [
                    "Programa_Referidos.docx",
                    "Bonificaciones.xlsx"
                ]
            },
            "07 FINANZAS Y CONTABILIDAD": {
                "Balance Inicial": [
                    "Balance_2025.xlsx"
                ],
                "Presupuesto Anual": [
                    "Presupuesto_Anual.xlsx"
                ],
                "Control de Gastos e Ingresos": [
                    "Registro_Gastos.xlsx",
                    "Ingresos_Mensuales.xlsx"
                ],
                "Flujo de Caja Proyectado": [
                    "Cash_Flow_Proyectado.xlsx"
                ],
                "Reportes Financieros": [
                    "Reporte_Trimestral.pdf",
                    "Estado_Resultados.pdf"
                ],
                "Proyecciones": [
                    "Proyeccion_Crecimiento.xlsx"
                ],
                "Calculadora Financiera": [
                    "Calculadora_Financiera.xlsx"
                ]
            },
            "08 RECURSOS HUMANOS Y EQUIPO": {
                "Organigrama": [
                    "Organigrama_Actualizado.pdf"
                ],
                "Roles y Responsabilidades": [
                    "Matriz_Roles.xlsx"
                ],
                "Job Descriptions": [
                    "JD_Marketing.docx",
                    "JD_Operaciones.docx",
                    "JD_Admin.docx"
                ],
                "KPIs": [
                    "Rol.docx",
                    "Evaluaciones.docx"
                ],
                "Manual de Cultura Organizacional": [
                    "Valores_Corporativos.docx"
                ],
                "Descripciones de Puesto": [
                    "Perfil_Puesto.docx"
                ],
                "Contratos - Freelancers": [
                    "Contrato_Freelancer_Base.docx"
                ],
                "Políticas Internas - Cultura": [
                    "Código_Conducta.docx",
                    "Política_Teletrabajo.docx"
                ],
                "Política de Compensaciones": [
                    "Tabla_Salarial.xlsx",
                    "Bonos_Incentivos.docx"
                ],
                "Contratos Guías Freelance": [
                    "Guía_Freelancer.docx"
                ],
                "Evaluaciones de Desempeño": [
                    "Plantilla_Evaluacion.xlsx"
                ]
            },
            "09_CAPACITACIÓN Y DOCUMENTACIÓN INTERNA": {
                "Manuales": [
                    "Manual_de_Inducción_Nuevos_Miembros.docx",
                    "Manual_de_Inducción.docx"
                ],
                "Guías Operativas": [
                    "Guía_Atención_Cliente.docx",
                    "Guía_Procesos_Internos.docx"
                ],
                "Capacitación Técnica": [
                    "Atencion_al_Cliente.docx",
                    "Ventas.docx",
                    "Operaciones.docx",
                    "Uso_de_Herramientas.docx"
                ],
                "Videos - Material Didáctico": [
                    "Video_Inducción.mp4",
                    "Demo_Herramientas.mp4"
                ],
                "Registro de Capacitación": [
                    "Asistencia_Capacitaciones.xlsx",
                    "Historial_Entrenamientos.xlsx"
                ]
            },
            "10 ANALÍTICA Y REPORTES": {
                "Dashboards (Operativos - Financieros - Marketing)": [
                    "Dashboard_PowerBI.pbix",
                    "Dashboard_Online_Link.txt"
                ],
                "Reportes Periódicos (Semanal - Mensual - Trimestral)": [
                    "Reporte_Semanal.xlsx",
                    "Reporte_Mensual.xlsx",
                    "Reporte_Trimestral.pdf"
                ],
                "Lecciones Aprendidas - Retrospectivas": [
                    "Retrospectiva_Q1.docx",
                    "Lecciones_Proyecto.docx"
                ],
                "Indicadores de Desempeño (KPIs globales)": [
                    "KPIs_Globales.xlsx",
                    "Indicadores_Por_Area.xlsx"
                ],
                "Dashboard Principal": [
                    "Dashboard_Principal.xlsx"
                ],
                "KPIs Operativos": [
                    "KPIs_Operativos.xlsx"
                ],
                "Análisis de Tendencias": [
                    "Analisis_Tendencias.xlsx"
                ]
            }
        }

    @staticmethod
    def _get_folder_descriptions() -> Dict[str, str]:
        """Get descriptions for main folders."""
        return {
            "00_ADMINISTRATIVO": """# 00_ADMINISTRATIVO

Esta carpeta contiene documentos administrativos generales del proyecto.

## Propósito
Almacenar información esencial para la gestión administrativa y legal del proyecto.

## Estructura
- **Información General del Proyecto**: Datos básicos y descripción del proyecto.
- **Datos Legales - RUC - Permisos**: Documentos legales, RUC y permisos necesarios.
- **Contratos - Acuerdos**: Contratos y acuerdos firmados.
- **Documentos de Propiedad Intelectual**: Patentes, marcas, derechos de autor.
- **Correspondencia Oficial - Ofertas - Licencias**: Cartas oficiales, ofertas y licencias.

## Uso
Coloca aquí todos los documentos relacionados con la administración y legalidad del proyecto.""",
            "01_ESTRATÉGICO": """# 01_ESTRATÉGICO

Esta carpeta contiene elementos estratégicos del proyecto.

## Propósito
Definir la dirección estratégica, objetivos y planificación del negocio.

## Estructura
- **Visión - Misión - Valores**: Declaraciones de visión, misión y valores.
- **Business Model Canvas**: Modelo de negocio canvas.
- **Plan de Negocios**: Plan detallado del negocio.
- **Análisis de Mercado y Competencia**: Estudios de mercado y análisis competitivo.
- **Roadmap Estratégico (Anual - Semestral)**: Planificación estratégica temporal.
- **Objetivos y KPIs**: Objetivos específicos y indicadores clave de rendimiento.
- **Proyecciones Financieras**: Proyecciones y presupuestos financieros.

## Uso
Utiliza esta carpeta para todos los documentos que guíen la estrategia del proyecto.""",
            "02_LEGAL_Y_CONSTITUCIÓN": """# 02_LEGAL_Y_CONSTITUCIÓN

Documentos legales y de constitución del proyecto.

## Propósito
Mantener todos los aspectos legales y de constitución en orden.

## Estructura
- **RUC y documentos fiscales**: RUC y documentos relacionados con impuestos.
- **Permisos de Operaciones**: Permisos necesarios para operar.
- **Póliza de Seguros**: Pólizas de seguro vigentes.
- **Acuerdo entre Socios Fundadores**: Acuerdos entre los fundadores.
- **Términos y Condiciones Clientes**: T&C para clientes.
- **Contrato Servicios (Cliente)**: Plantillas de contratos de servicios.
- **Waiver - Liberación Responsabilidad**: Documentos de liberación de responsabilidad.
- **Plantilla Contrato Proveedores**: Plantillas para contratos con proveedores.

## Uso
Archiva aquí todos los documentos legales y de constitución.""",
            "03_OPERACIONES": """# 03_OPERACIONES

Documentos operativos del proyecto.

## Propósito
Gestionar las operaciones diarias y procesos del negocio.

## Estructura
- **Manuales**: Manuales de procedimientos.
- **Procesos**: Definición de procesos operativos.
- **Protocolos y Checklists**: Protocolos y listas de verificación.
- **Control de Proveedores**: Gestión de proveedores.
- **Manual de Calidad - Estándares**: Estándares de calidad.
- **Calendario Operativo - Cronogramas**: Calendarios y cronogramas operativos.

## Uso
Coloca aquí documentos relacionados con las operaciones diarias.""",
            "04_COMERCIAL_Y_VENTAS": """# 04_COMERCIAL_Y_VENTAS

Materiales comerciales y de ventas.

## Propósito
Apoyar las actividades de ventas y comerciales.

## Estructura
- **Manual de Ventas**: Guías de ventas.
- **Scripts de Venta WhatsApp**: Scripts para ventas por WhatsApp.
- **Respuestas a Objeciones Comunes**: Respuestas estándar a objeciones.
- **Política de Precios y Descuentos**: Políticas de pricing.
- **Paquetes y Promociones Vigentes**: Ofertas actuales.
- **Calculadora de Costos**: Herramientas para calcular costos.
- **Análisis de Rentabilidad**: Análisis de rentabilidad.
- **Plantillas Propuestas Corporativas**: Plantillas para propuestas.

## Uso
Archiva aquí todo lo relacionado con ventas y comercialización.""",
            "05_MARKETING_Y_CONTENIDO": """# 05_MARKETING_Y_CONTENIDO

Estrategias y contenido de marketing.

## Propósito
Gestionar el marketing y la creación de contenido.

## Estructura
- **Plan de Marketing**: Estrategia de marketing.
- **Calendario Editorial**: Calendario de publicaciones.
- **Guía de Marca (Brand Guidelines)**: Directrices de marca.
- **Banco de Contenido (Posts pre-creados)**: Contenido listo para usar.
- **Estrategia Comercial**: Estrategias comerciales.
- **Plantillas de Diseño**: Plantillas para diseños.
- **Análisis de Mercado y Competencia**: Análisis de mercado.
- **Reportes de Marketing**: Reportes de campañas.

## Uso
Utiliza para marketing y contenido.""",
            "06_CLIENTES_Y_USUARIOS": """# 06_CLIENTES_Y_USUARIOS

Gestión de clientes y usuarios.

## Propósito
Mantener información y herramientas para clientes.

## Estructura
- **CRM**: Sistema de gestión de clientes.
- **Plantillas de Comunicación**: Templates para emails y WhatsApp.
- **Contratos o Acuerdos con Clientes**: Contratos con clientes.
- **Formulario de Feedback**: Formularios de retroalimentación.
- **Registro de Reviews y Testimonios**: Reseñas y testimonios.
- **Programa de Fidelización y Referidos**: Programas de lealtad.

## Uso
Archiva información relacionada con clientes.""",
            "07_FINANZAS_Y_CONTABILIDAD": """# 07_FINANZAS_Y_CONTABILIDAD

Documentos financieros y contables.

## Propósito
Gestionar aspectos financieros del proyecto.

## Estructura
- **Balance Inicial**: Balance inicial.
- **Presupuesto Anual**: Presupuesto anual.
- **Control de Gastos e Ingresos**: Control financiero.
- **Flujo de Caja Proyectado**: Proyecciones de flujo de caja.
- **Reportes Financieros**: Reportes financieros.
- **Proyecciones**: Proyecciones financieras.

## Uso
Coloca aquí todos los documentos financieros.""",
            "08_RECURSOS_HUMANOS_Y_EQUIPO": """# 08_RECURSOS_HUMANOS_Y_EQUIPO

Gestión de recursos humanos.

## Propósito
Administrar el equipo y recursos humanos.

## Estructura
- **Organigrama**: Estructura organizacional.
- **Roles y Responsabilidades**: Definición de roles.
- **Job Descriptions**: Descripciones de puestos.
- **KPIs**: Indicadores de rendimiento.
- **Manual de Cultura Organizacional**: Cultura de la empresa.
- **Descripciones de Puesto**: Detalles de puestos.
- **Contratos - Freelancers**: Contratos con freelancers.
- **Políticas Internas - Cultura**: Políticas internas.
- **Política de Compensaciones**: Políticas de compensación.
- **Contratos Guías Freelance**: Contratos específicos.
- **Evaluaciones de Desempeño**: Evaluaciones.

## Uso
Archiva documentos de RRHH.""",
            "09_CAPACITACIÓN_Y_DOCUMENTACIÓN_INTERNA": """# 09_CAPACITACIÓN_Y_DOCUMENTACIÓN_INTERNA

Capacitación y documentación interna.

## Propósito
Formar y documentar internamente.

## Estructura
- **Manuales**: Manuales de capacitación.
- **Guías Operativas**: Guías para operaciones.
- **Capacitación Técnica**: Capacitación técnica.
- **Videos - Material Didáctico**: Material audiovisual.
- **Registro de Capacitación**: Registros de capacitaciones.

## Uso
Utiliza para capacitación y documentación.""",
            "10_ANALÍTICA_Y_REPORTES": """# 10_ANALÍTICA_Y_REPORTES

Análisis y reportes del proyecto.

## Propósito
Analizar rendimiento y generar reportes.

## Estructura
- **Dashboards (Operativos - Financieros - Marketing)**: Paneles de control.
- **Reportes Periódicos (Semanal - Mensual - Trimestral)**: Reportes regulares.
- **Lecciones Aprendidas - Retrospectivas**: Lecciones y retrospectivas.
- **Indicadores de Desempeño (KPIs globales)**: KPIs globales.

## Uso
Archiva análisis y reportes."""
        }

    def create_structure(self, project_name: str, base_path: str, structure: Optional[Dict[str, Any]] = None) -> str:
        if structure is None:
            structure = self.default_structure
        root_path = os.path.join(base_path, project_name)
        try:
            os.makedirs(root_path, exist_ok=True)
            self._create_folders(root_path, structure, is_root=True)
            # Create root INFO.md file
            self._create_root_info_md(root_path, structure)
            return root_path
        except OSError as e:
            raise RuntimeError(f"Failed to create structure: {e}")

    def _create_folders(self, base_path: str, structure: Dict[str, Any], is_root: bool = True) -> None:
        for folder, subfolders in structure.items():
            folder_path = os.path.join(base_path, folder)
            os.makedirs(folder_path, exist_ok=True)

            # Create INFO.md for main folders
            if is_root and folder in self.folder_descriptions:
                readme_path = os.path.join(folder_path, "INFO.md")
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(self.folder_descriptions[folder])

            # Handle subfolders or files
            if isinstance(subfolders, dict):
                self._create_folders(folder_path, subfolders, is_root=False)
            elif isinstance(subfolders, list):
                # Create files from the list
                self._create_files_from_list(folder_path, subfolders)

    def _create_files_from_list(self, folder_path: str, file_list: List[str]) -> None:
        """Create files from a list, using templates if available."""
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)

            # Try to find a template for this file (external first, then database)
            template = self._find_template_for_file(file_name)
            if template:
                try:
                    # Check if it's an external template
                    if 'content' in template or 'sheets' in template:
                        # External template - use external rendering
                        content = self.template_manager.render_external_template(file_name)
                        if content:
                            extension = file_name.split('.')[-1] if '.' in file_name else 'txt'
                            renderer = RendererFactory.get_renderer(extension)
                            renderer.render(content, file_path)
                        else:
                            # Fallback to default parameters
                            default_params = self._get_default_params_for_file(file_name)
                            content = self.template_manager.render_template(template, default_params)
                            renderer = RendererFactory.get_renderer(template.get('extension', 'txt'))
                            renderer.render(content, file_path)
                    else:
                        # Database template - use traditional rendering
                        default_params = self._get_default_params_for_file(file_name)
                        content = self.template_manager.render_template(template, default_params)
                        renderer = RendererFactory.get_renderer(template.get('extension', 'txt'))
                        renderer.render(content, file_path)
                except Exception as e:
                    # If template rendering fails, create the empty file
                    print(f"Warning: Failed to render template for {file_name}: {e}")
                    self._create_empty_file(file_path)
            else:
                # Create the empty file
                self._create_empty_file(file_path)

    def _create_empty_file(self, file_path: str) -> None:
        """Create an empty file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# {os.path.basename(file_path)}\n\nContenido base para {os.path.basename(file_path)}.")

    def _create_root_info_md(self, root_path: str, structure: Dict[str, Any]) -> None:
        """Create INFO.md file in the root directory with complete structure information."""
        info_content = f"""# Estructura del Proyecto: {os.path.basename(root_path)}

Esta carpeta contiene la estructura completa del proyecto organizacional, diseñada para empresas de servicios turísticos y similares.

## Propósito General
Proporcionar una organización sistemática y profesional para todos los aspectos de gestión empresarial, desde lo administrativo hasta lo operativo, financiero y de recursos humanos.

## Árbol de Carpetas Completo

```
{os.path.basename(root_path)}/
{self._generate_tree_structure(structure, "", 0)}
```

## Estructura Detallada del Proyecto

"""

        # Add main folders with detailed descriptions
        for folder_name, folder_content in structure.items():
            if folder_name in self.folder_descriptions:
                # Add the full description from folder_descriptions
                info_content += self.folder_descriptions[folder_name]
                info_content += "\n\n"

                # Add detailed content breakdown
                info_content += "### Contenido Específico:\n\n"
                info_content += self._get_detailed_folder_contents(folder_name, folder_content, level=0)
                info_content += "\n---\n\n"

        # Add summary statistics
        total_folders, total_files = self._count_structure_items(structure)
        info_content += f"""## Estadísticas de la Estructura

- **Total de carpetas principales**: {len(structure)}
- **Total de subcarpetas**: {total_folders}
- **Total de archivos**: {total_files}

## Uso Recomendado

1. **Organización**: Mantén la estructura de carpetas tal como está definida
2. **Nomenclatura**: Usa nombres descriptivos para los archivos
3. **Versionado**: Implementa control de versiones para documentos importantes
4. **Acceso**: Define permisos apropiados según el nivel de confidencialidad
5. **Backup**: Realiza copias de seguridad regulares

## Mantenimiento

- Revisa periódicamente la estructura para asegurar que se adapte a las necesidades cambiantes
- Actualiza documentos según evolucione el negocio
- Mantén consistencia en la nomenclatura y organización

---
*Estructura generada automáticamente por Project Structure Manager*
"""

        info_path = os.path.join(root_path, "INFO.md")
        with open(info_path, 'w', encoding='utf-8') as f:
            f.write(info_content)

    def _generate_tree_structure(self, structure: Dict[str, Any], prefix: str = "", level: int = 0) -> str:
        """Generate a tree-like structure representation."""
        result = ""
        items = list(structure.items())

        for i, (key, value) in enumerate(items):
            is_last = (i == len(items) - 1)
            current_prefix = "└── " if is_last else "├── "
            next_prefix = prefix + ("    " if is_last else "│   ")

            result += f"{prefix}{current_prefix}{key}/\n"

            if isinstance(value, dict):
                result += self._generate_tree_structure(value, next_prefix, level + 1)
            elif isinstance(value, list):
                for j, item in enumerate(value):
                    item_is_last = (j == len(value) - 1)
                    item_prefix = "└── " if item_is_last else "├── "
                    result += f"{next_prefix}{item_prefix}{item}\n"

        return result

    def _get_folder_contents(self, content: Any, level: int = 0) -> str:
        """Recursively get folder contents as formatted text."""
        indent = "  " * (level + 1)
        result = ""

        if isinstance(content, dict):
            for key, value in content.items():
                if isinstance(value, dict):
                    if value:  # Has subcontent
                        result += f"{indent}- **{key}**\n"
                        result += self._get_folder_contents(value, level + 1)
                    else:  # Empty folder
                        result += f"{indent}- **{key}** (carpeta)\n"
                elif isinstance(value, list):
                    result += f"{indent}- **{key}**\n"
                    for item in value:
                        result += f"{indent}  - {item}\n"
                else:
                    result += f"{indent}- {key}\n"
        elif isinstance(content, list):
            for item in content:
                result += f"{indent}- {item}\n"

        return result

    def _get_detailed_folder_contents(self, folder_name: str, content: Any, level: int = 0) -> str:
        """Get detailed folder contents with descriptions of what goes in each folder/file."""
        result = ""

        if isinstance(content, dict):
            for key, value in content.items():
                if isinstance(value, dict):
                    if value:  # Has subcontent
                        result += f"#### 📁 {key}\n"
                        result += f"**Propósito**: {self._get_folder_purpose(key)}\n\n"
                        result += f"**Contenido**:\n"
                        result += self._get_detailed_folder_contents(folder_name, value, level + 1)
                    else:  # Empty folder
                        result += f"#### 📁 {key}\n"
                        result += f"**Propósito**: {self._get_folder_purpose(key)}\n\n"
                        result += f"**Contenido**: Carpeta destinada para {key.lower()}\n\n"
                elif isinstance(value, list):
                    result += f"#### 📄 Archivos en {key}\n"
                    result += f"**Propósito**: {self._get_folder_purpose(key)}\n\n"
                    result += f"**Archivos incluidos**:\n"
                    for item in value:
                        result += f"- **{item}**: {self._get_file_description(item)}\n"
                    result += "\n"
                else:
                    result += f"#### 📄 {key}\n"
                    result += f"**Propósito**: {self._get_file_description(key)}\n\n"
        elif isinstance(content, list):
            for item in content:
                result += f"- **{item}**: {self._get_file_description(item)}\n"

        return result

    @staticmethod
    def _get_folder_purpose(folder_name: str) -> str:
        """Get a brief description of what goes in a folder."""
        purposes = {
            "Información General del Proyecto": "Documentos básicos del proyecto como descripción, alcance y objetivos",
            "Datos Legales - RUC - Permisos": "Documentación legal, RUC, permisos y licencias necesarias",
            "Contratos - Acuerdos": "Todos los contratos y acuerdos firmados",
            "Documentos de Propiedad Intelectual": "Patentes, marcas, derechos de autor y propiedad intelectual",
            "Correspondencia Oficial - Ofertas - Licencias": "Cartas oficiales, ofertas comerciales y licencias",
            "Visión - Misión - Valores": "Declaraciones estratégicas de la empresa",
            "Business Model Canvas": "Modelo de negocio canvas con componentes clave",
            "Plan de Negocios": "Plan detallado del negocio con proyecciones",
            "Análisis de Mercado y Competencia": "Estudios de mercado y análisis competitivo",
            "Roadmap Estratégico (Anual - Semestral)": "Planificación estratégica temporal",
            "Objetivos y KPIs": "Objetivos específicos e indicadores clave de rendimiento",
            "Proyecciones Financieras": "Proyecciones y presupuestos financieros",
            "RUC y documentos fiscales": "Documentos fiscales y RUC de la empresa",
            "Permisos de Operaciones": "Permisos necesarios para operar legalmente",
            "Póliza de Seguros": "Pólizas de seguro vigentes",
            "Acuerdo entre Socios Fundadores": "Acuerdos entre los fundadores",
            "Términos y Condiciones Clientes": "T&C para clientes",
            "Contrato Servicios (Cliente)": "Plantillas de contratos de servicios",
            "Waiver - Liberación Responsabilidad": "Documentos de liberación de responsabilidad",
            "Plantilla Contrato Proveedores": "Plantillas para contratos con proveedores",
            "Manuales": "Manuales de procedimientos operativos",
            "Procesos": "Definición de procesos operativos",
            "Protocolos y Checklists": "Protocolos y listas de verificación",
            "Control de Proveedores": "Gestión y control de proveedores",
            "Manual de Calidad - Estándares": "Estándares de calidad y procedimientos",
            "Calendario Operativo - Cronogramas": "Calendarios y cronogramas operativos",
            "Manual de Ventas": "Guías y procedimientos de ventas",
            "Scripts de Venta WhatsApp": "Scripts para ventas por WhatsApp",
            "Respuestas a Objeciones Comunes": "Respuestas estándar a objeciones de venta",
            "Política de Precios y Descuentos": "Políticas de pricing y descuentos",
            "Paquetes y Promociones Vigentes": "Ofertas y promociones actuales",
            "Calculadora de Costos": "Herramientas para calcular costos",
            "Análisis de Rentabilidad": "Análisis de rentabilidad de productos/servicios",
            "Plantillas Propuestas Corporativas": "Plantillas para propuestas comerciales",
            "Base de Datos de Clientes.xlsx": "Base de datos de clientes en Excel",
            "Plan de Marketing": "Estrategia general de marketing",
            "Calendario Editorial": "Calendario de publicaciones y contenido",
            "Guía de Marca (Brand Guidelines)": "Directrices de marca e identidad",
            "Banco de Contenido (Posts pre-creados)": "Contenido preparado para redes sociales",
            "Estrategia Comercial": "Estrategias comerciales específicas",
            "Plantillas de Diseño": "Plantillas para diseños gráficos",
            "Análisis de Mercado y Competencia": "Estudios de mercado y competencia",
            "Reportes de Marketing": "Reportes de campañas de marketing",
            "CRM": "Sistema de gestión de relaciones con clientes",
            "Plantillas de Comunicación": "Templates para emails y WhatsApp",
            "Contratos o Acuerdos con Clientes": "Contratos y acuerdos con clientes",
            "Formulario de Feedback": "Formularios para retroalimentación",
            "Registro de Reviews y Testimonios": "Reseñas y testimonios de clientes",
            "Programa de Fidelización y Referidos": "Programas de lealtad y referidos",
            "Balance Inicial": "Balance inicial del negocio",
            "Presupuesto Anual": "Presupuesto anual detallado",
            "Control de Gastos e Ingresos": "Control financiero diario",
            "Flujo de Caja Proyectado": "Proyecciones de flujo de caja",
            "Reportes Financieros": "Reportes financieros periódicos",
            "Proyecciones": "Proyecciones financieras futuras",
            "Calculadora Financiera.xlsx": "Herramientas financieras en Excel",
            "Organigrama": "Estructura organizacional de la empresa",
            "Roles y Responsabilidades": "Definición de roles y responsabilidades",
            "Job Descriptions": "Descripciones detalladas de puestos",
            "KPIs": "Indicadores clave de rendimiento",
            "Manual de Cultura Organizacional": "Cultura y valores de la empresa",
            "Descripciones de Puesto": "Detalles específicos de cada puesto",
            "Contratos - Freelancers": "Contratos con freelancers",
            "Políticas Internas - Cultura": "Políticas internas y cultura",
            "Política de Compensaciones": "Políticas de compensación y beneficios",
            "Contratos Guías Freelance": "Plantillas de contratos freelance",
            "Evaluaciones de Desempeño": "Evaluaciones de empleados",
            "Manuales": "Manuales de inducción y procedimientos",
            "Guías Operativas": "Guías para operaciones diarias",
            "Capacitación Técnica": "Material de capacitación técnica",
            "Videos - Material Didáctico": "Contenido audiovisual educativo",
            "Registro de Capacitación": "Registros de capacitaciones realizadas",
            "Dashboards (Operativos - Financieros - Marketing)": "Paneles de control interactivos",
            "Reportes Periódicos (Semanal - Mensual - Trimestral)": "Reportes regulares de rendimiento",
            "Lecciones Aprendidas - Retrospectivas": "Análisis de experiencias y mejoras",
            "Indicadores de Desempeño (KPIs globales)": "KPIs generales del negocio",
            "Dashboard Principal.xlsx": "Dashboard principal en Excel",
            "KPIs Operativos.xlsx": "KPIs operativos en Excel",
            "Análisis de Tendencias.xlsx": "Análisis de tendencias en Excel"
        }
        return purposes.get(folder_name, f"Contenido relacionado con {folder_name.lower()}")

    @staticmethod
    def _get_file_description(file_name: str) -> str:
        """Get description of what goes in a specific file."""
        descriptions = {
            "Confirmación_Reserva.html": "Email template para confirmar reservas de clientes",
            "Recordatorio_48h.html": "Email recordatorio 48 horas antes del servicio",
            "Recordatorio_24h.html": "Email recordatorio 24 horas antes del servicio",
            "Recordatorio_Día_Tour.html": "Email recordatorio el día del tour",
            "Agradecimiento_Post_Tour.html": "Email de agradecimiento después del servicio",
            "Solicitud_Review.html": "Email solicitando reseñas y testimonios",
            "Newsletter_Mensual.html": "Boletín mensual informativo",
            "Respuestas_Rápidas.docx": "Documento con respuestas rápidas para WhatsApp",
            "Rol.docx": "Documento con definición de roles",
            "Evaluaciones.docx": "Documento de evaluaciones de desempeño",
            "Manual_de_Inducción_Nuevos_Miembros.docx": "Manual completo de inducción",
            "Manual_de_Inducción.docx": "Manual de inducción para nuevos miembros",
            "Atencion_al_Cliente.docx": "Manual de atención al cliente",
            "Ventas.docx": "Manual de procedimientos de ventas",
            "Operaciones.docx": "Manual de operaciones",
            "Uso_de_Herramientas.docx": "Guía de uso de herramientas",
            "Base de Datos de Clientes.xlsx": "Base de datos completa de clientes",
            "Calculadora Financiera.xlsx": "Herramientas de cálculo financiero",
            "Dashboard Principal.xlsx": "Dashboard principal con métricas clave",
            "KPIs Operativos.xlsx": "Indicadores operativos en Excel",
            "Análisis de Tendencias.xlsx": "Análisis de tendencias del negocio"
        }
        return descriptions.get(file_name, f"Archivo {file_name} con contenido específico del área")

    @staticmethod
    def _count_structure_items(structure: Dict[str, Any]) -> tuple[int, int]:
        """Count total folders and files in the structure."""
        total_folders = 0
        total_files = 0

        def count_recursive(content: Any) -> None:
            nonlocal total_folders, total_files
            if isinstance(content, dict):
                for key, value in content.items():
                    if isinstance(value, dict):
                        total_folders += 1
                        count_recursive(value)
                    elif isinstance(value, list):
                        total_files += len(value)
                    else:
                        total_files += 1
            elif isinstance(content, list):
                total_files += len(content)

        count_recursive(structure)
        return total_folders, total_files

    def _find_template_for_file(self, file_name: str) -> Optional[Dict[str, Any]]:
        """Find a template that matches the file name or extension."""
        try:
            extension = file_name.split('.')[-1] if '.' in file_name else ''

            # First, try to find an external template
            external_template = self.template_manager.find_external_template(file_name)
            if external_template:
                return external_template

            # Fallback to database templates
            templates = self.template_manager.list_templates()

            # Try to find by exact name (without extension)
            base_name = file_name.replace('.' + extension, '').lower()
            for template in templates:
                template_base_name = template['nombre'].lower().replace('plantilla ', '').replace(' base', '')
                if template_base_name in base_name or base_name in template_base_name:
                    return self.template_manager.load_template(template['id'])

            # Then, try by extension
            for template in templates:
                if template['extension'] == extension:
                    return self.template_manager.load_template(template['id'])

            # Special cases for Excel files
            if extension == 'xlsx':
                # Try to find report or data templates
                for template in templates:
                    if 'reporte' in template['nombre'].lower() or 'excel' in template['nombre'].lower():
                        return self.template_manager.load_template(template['id'])

            # Special cases for DOCX files - try advanced template
            if extension == 'docx':
                # Try to find an advanced business document template
                for template in templates:
                    if 'advanced' in template['nombre'].lower() or 'business' in template['nombre'].lower():
                        return self.template_manager.load_template(template['id'])
        except Exception:
            return None

    @staticmethod
    def _get_default_params_for_file(file_name: str) -> Dict[str, str]:
        """Get default parameters for a file based on its name."""
        # Try external template parameters first
        from core.external_templates import get_external_template_params
        return get_external_template_params(file_name)

    def save_to_db(self, project_name: str, structure: Dict[str, Any], path: Optional[str] = None) -> int:
        return self.db_manager.save_project(project_name, structure, path)

    def load_from_db(self, project_id: int) -> Optional[Dict[str, Any]]:
        return self.db_manager.get_project(project_id)

    def update_in_db(self, project_id: int, structure: Dict[str, Any]) -> None:
        self.db_manager.update_project(project_id, structure)

    def get_templates(self) -> List[Dict[str, Any]]:
        return self.db_manager.get_templates()

    def save_template(self, name: str, structure: Dict[str, Any]) -> None:
        self.db_manager.save_template(name, structure)

    def scan_directory(self, path: str) -> Dict[str, Any]:
        """Scan a directory and return its structure as a nested dict."""
        structure = {}
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    structure[item] = self.scan_directory(item_path)
                else:
                    # For files, we can store them as a list with one element or just the filename
                    structure[item] = [item]
        except OSError as e:
            raise RuntimeError(f"Failed to scan directory {path}: {e}")
        return structure

    def save_scanned_structure(self, project_name: str, path: str) -> int:
        """Scan a directory and save its structure to the database."""
        structure = self.scan_directory(path)
        return self.save_to_db(project_name, structure)

    def create_structure_and_save(self, project_name: str, base_path: str,
                                  structure: Optional[Dict[str, Any]] = None) -> str:
        """Create a structure and save to the database."""
        if structure is None:
            structure = self.default_structure
        root_path = self.create_structure(project_name, base_path, structure)
        project_id = self.save_to_db(project_name, structure, root_path)
        return root_path

    def check_duplicate_name(self, project_name: str) -> bool:
        """Check if a project name already exists."""
        return self.db_manager.check_duplicate_name(project_name)

    def regenerate_structure(self, project_name: str, base_path: str) -> str:
        """Regenerate existing project structure."""
        existing_project = self.db_manager.get_project_by_name(project_name)
        if not existing_project:
            raise RuntimeError(f"Project '{project_name}' not found in database.")

        root_path = self.create_structure(project_name, base_path, existing_project['structure'])
        self.db_manager.update_project(existing_project['id'], path=root_path)
        return root_path

    def restart_structure(self, project_name: str, base_path: str) -> str:
        """Restart project with default structure."""
        root_path = self.create_structure(project_name, base_path, self.default_structure)
        existing_project = self.db_manager.get_project_by_name(project_name)

        if existing_project:
            # Update existing project
            self.db_manager.update_project(existing_project['id'], structure=self.default_structure, path=root_path)
        else:
            # Create new project
            self.save_to_db(project_name, self.default_structure, root_path)

        return root_path

    def check_path_conflict(self, project_name: str, path: str) -> Optional[str]:
        """Check if there's a conflict with the project path."""
        return self.db_manager.check_project_path_conflict(project_name, path)
