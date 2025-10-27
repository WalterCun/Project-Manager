import os
from typing import Dict, Any, Optional, List
from .database import DatabaseManager


class StructureGenerator:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.default_structure = self._get_default_structure()

    def _get_default_structure(self) -> Dict[str, Any]:
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
                "Plantillas Propuestas Corporativas": {}
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
                "Proyecciones": {}
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
                "Indicadores de Desempeño (KPIs globales)": {}
            }
        }

    def create_structure(self, project_name: str, base_path: str, structure: Optional[Dict[str, Any]] = None) -> str:
        if structure is None:
            structure = self.default_structure
        root_path = os.path.join(base_path, project_name)
        try:
            os.makedirs(root_path, exist_ok=True)
            self._create_folders(root_path, structure)
            return root_path
        except OSError as e:
            raise RuntimeError(f"Failed to create structure: {e}")

    def _create_folders(self, base_path: str, structure: Dict[str, Any]) -> None:
        for folder, subfolders in structure.items():
            folder_path = os.path.join(base_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            if isinstance(subfolders, dict):
                self._create_folders(folder_path, subfolders)

    def save_to_db(self, project_name: str, structure: Dict[str, Any]) -> int:
        return self.db_manager.save_project(project_name, structure)

    def load_from_db(self, project_id: int) -> Optional[Dict[str, Any]]:
        return self.db_manager.get_project(project_id)

    def update_in_db(self, project_id: int, structure: Dict[str, Any]) -> None:
        self.db_manager.update_project(project_id, structure)

    def get_templates(self) -> List[Dict[str, Any]]:
        return self.db_manager.get_templates()

    def save_template(self, name: str, structure: Dict[str, Any]) -> None:
        self.db_manager.save_template(name, structure)
