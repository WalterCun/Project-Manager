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
            "00_ADMINISTRATIVO": {
                "Información General del Proyecto": {},
                "Datos Legales - RUC - Permisos": {},
                "Contratos - Acuerdos": {},
                "Documentos de Propiedad Intelectual": {},
                "Correspondencia Oficial - Ofertas - Licencias": {}
            },
            "01_ESTRATÉGICO": {
                "Visión - Misión - Valores": {},
                "Business Model Canvas": {},
                "Plan de Negocios": {},
                "Análisis de Mercado y Competencia": {},
                "Roadmap Estratégico (Anual - Semestral)": {},
                "Objetivos y KPIs": {},
                "Proyecciones Financieras": {}
            },
            "02_LEGAL_Y_CONSTITUCIÓN": {
                "RUC y documentos fiscales": {},
                "Permisos de Operaciones": {},
                "Póliza de Seguros": {},
                "Acuerdo entre Socios Fundadores": {},
                "Términos y Condiciones Clientes": {},
                "Contrato Servicios (Cliente)": {},
                "Waiver - Liberación Responsabilidad": {},
                "Plantilla Contrato Proveedores": {}
            },
            "03_OPERACIONES": {
                "Manuales": {},
                "Procesos": {},
                "Protocolos y Checklists": {},
                "Control de Proveedores": {},
                "Manual de Calidad - Estándares": {},
                "Calendario Operativo - Cronogramas": {}
            },
            "04_COMERCIAL_Y_VENTAS": {
               "Manual de Ventas": {},
               "Scripts de Venta WhatsApp": {},
               "Respuestas a Objeciones Comunes": {},
               "Política de Precios y Descuentos": {},
               "Paquetes y Promociones Vigentes": {},
               "Calculadora de Costos": {},
               "Análisis de Rentabilidad": {},
               "Plantillas Propuestas Corporativas": {},
               "Base de Datos de Clientes.xlsx": {}
           },
            "05_MARKETING_Y_CONTENIDO": {
                "Plan de Marketing": {},
                "Calendario Editorial": {},
                "Guía de Marca (Brand Guidelines)": {},
                "Banco de Contenido (Posts pre-creados)": {
                    "Material Promocional": {},
                    "Diseños": {},
                    "Plantillas": {}
                },
                "Estrategia Comercial": {},
                "Plantillas de Diseño": {},
                "Análisis de Mercado y Competencia": {},
                "Reportes de Marketing": {}
            },
            "06_CLIENTES_Y_USUARIOS": {
                "CRM": {
                    "Base de Datos - CRM": {}
                },
                "Plantillas de Comunicación": {
                    "Emails Templates": [
                        "Confirmación_Reserva.html",
                        "Recordatorio_48h.html",
                        "Recordatorio_24h.html",
                        "Recordatorio_Día_Tour.html",
                        "Agradecimiento_Post_Tour.html",
                        "Solicitud_Review.html",
                        "Newsletter_Mensual.html"
                    ],
                    "Whatsapp": [
                        "Respuestas_Rápidas.docx"
                    ]
                },
                "Contratos o Acuerdos con Clientes": {},
                "Formulario de Feedback": {},
                "Registro de Reviews y Testimonios": {},
                "Programa de Fidelización y Referidos": {}
            },
            "07_FINANZAS_Y_CONTABILIDAD": {
               "Balance Inicial": {},
               "Presupuesto Anual": {},
               "Control de Gastos e Ingresos": {},
               "Flujo de Caja Proyectado": {},
               "Reportes Financieros": {},
               "Proyecciones": {},
               "Calculadora Financiera.xlsx": {}
           },
            "08_RECURSOS_HUMANOS_Y_EQUIPO": {
                "Organigrama": {},
                "Roles y Responsabilidades": {},
                "Job Descriptions": {},
                "KPIs": [
                    "Rol.docx",
                    "Evaluaciones.docx"
                ],
                "Manual de Cultura Organizacional": {},
                "Descripciones de Puesto": {},
                "Contratos - Freelancers": {},
                "Políticas Internas - Cultura": {},
                "Política de Compensaciones": {},
                "Contratos Guías Freelance": {},
                "Evaluaciones de Desempeño": {}
            },
            "09_CAPACITACIÓN_Y_DOCUMENTACIÓN_INTERNA": {
                "Manuales": [
                    "Manual_de_Inducción_Nuevos_Miembros.docx",
                    "Manual_de_Inducción.docx"
                ],
                "Guías Operativas": {},
                "Capacitación Técnica": [
                    "Atencion_al_Cliente.docx",
                    "Ventas.docx",
                    "Operaciones.docx",
                    "Uso_de_Herramientas.docx"
                ],
                "Videos - Material Didáctico": {},
                "Registro de Capacitación": {}
            },
            "10_ANALÍTICA_Y_REPORTES": {
               "Dashboards (Operativos - Financieros - Marketing)": {},
               "Reportes Periódicos (Semanal - Mensual - Trimestral)": {},
               "Lecciones Aprendidas - Retrospectivas": {},
               "Indicadores de Desempeño (KPIs globales)": {},
               "Dashboard Principal.xlsx": {},
               "KPIs Operativos.xlsx": {},
               "Análisis de Tendencias.xlsx": {}
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
            return root_path
        except OSError as e:
            raise RuntimeError(f"Failed to create structure: {e}")

    def _create_folders(self, base_path: str, structure: Dict[str, Any], is_root: bool = True) -> None:
        for folder, subfolders in structure.items():
            folder_path = os.path.join(base_path, folder)
            os.makedirs(folder_path, exist_ok=True)

            # Create README.md for main folders
            if is_root and folder in self.folder_descriptions:
                readme_path = os.path.join(folder_path, "README.md")
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

    def _find_template_for_file(self, file_name: str) -> Optional[Dict[str, Any]]:
        """Find a template that matches the file name or extension."""
        try:
            extension = file_name.split('.')[-1] if '.' in file_name else ''

            # First, try to find external template
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

        except Exception:
            pass
        return None

    def _get_default_params_for_file(self, file_name: str) -> Dict[str, str]:
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
