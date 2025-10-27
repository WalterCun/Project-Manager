import re
import json
from typing import Dict, Any, Optional, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.database import DatabaseManager, Template
from core.external_templates import ExternalTemplateLoader, get_external_template_params

class TemplateNotFoundError(Exception):
    pass

class InvalidPlaceholderError(Exception):
    pass

class TemplateManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.external_loader = ExternalTemplateLoader()

    def load_template(self, template_id: int) -> Dict[str, Any]:
        """Load template with inheritance applied recursively."""
        template = self.db_manager.get_template(template_id)
        if not template:
            raise TemplateNotFoundError(f"Template with ID {template_id} not found.")

        # Apply inheritance
        if template['padre_id']:
            parent = self.load_template(template['padre_id'])
            template = self._merge_templates(parent, template)

        return template

    def _merge_templates(self, parent: Dict[str, Any], child: Dict[str, Any]) -> Dict[str, Any]:
        """Merge child template with parent, child overrides parent."""
        merged = parent.copy()
        merged['contenido'] = child.get('contenido', parent['contenido'])
        merged['nombre'] = child.get('nombre', parent['nombre'])
        merged['extension'] = child.get('extension', parent['extension'])
        # Other fields from child if present
        for key in ['id', 'padre_id', 'project_id', 'created_at', 'updated_at']:
            if key in child:
                merged[key] = child[key]
        return merged

    def render_template(self, template: Dict[str, Any], params: Dict[str, str]) -> str:
        """Render template by replacing placeholders with values."""
        contenido = template['contenido']
        placeholders = re.findall(r'\{\{(\w+)\}\}', contenido)

        # Validate all placeholders are provided
        missing = set(placeholders) - set(params.keys())
        if missing:
            raise InvalidPlaceholderError(f"Missing placeholders: {', '.join(missing)}")

        # Replace placeholders
        for key, value in params.items():
            contenido = contenido.replace(f"{{{{{key}}}}}", str(value))

        return contenido

    def save_template(self, nombre: str, contenido: str, extension: str, padre_id: Optional[int] = None, project_id: Optional[int] = None) -> int:
        """Save a new template."""
        return self.db_manager.save_template(nombre, contenido, extension, padre_id, project_id)

    def update_template(self, template_id: int, **kwargs) -> None:
        """Update an existing template."""
        self.db_manager.update_template(template_id, **kwargs)

    def list_templates(self, project_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """List all templates."""
        return self.db_manager.list_templates(project_id)

    def delete_template(self, template_id: int) -> None:
        """Delete a template."""
        self.db_manager.delete_template(template_id)

    def find_external_template(self, file_name: str) -> Optional[Dict[str, Any]]:
        """Find an external template that matches the file name."""
        extension = file_name.split('.')[-1] if '.' in file_name else ''

        # Try to find by exact name first
        base_name = file_name.replace('.' + extension, '').lower()
        templates = self.external_loader.list_templates(extension)

        for template_info in templates:
            template_base_name = template_info['name'].lower().replace(' ', '_')
            if template_base_name in base_name or base_name in template_base_name:
                return self.external_loader.load_template(template_info['name'], extension)

        # Try by extension
        for template_info in templates:
            if template_info['extension'] == extension:
                return self.external_loader.load_template(template_info['name'], extension)

        return None

    def load_external_template(self, template_name: str, extension: str) -> Optional[Dict[str, Any]]:
        """Load an external template by name and extension."""
        return self.external_loader.load_template(template_name, extension)

    def list_external_templates(self, extension: Optional[str] = None) -> List[Dict[str, str]]:
        """List all external templates."""
        return self.external_loader.list_templates(extension)

    def save_external_template(self, template_data: Dict[str, Any], extension: str) -> bool:
        """Save a template to external file."""
        return self.external_loader.save_template(template_data, extension)

    def delete_external_template(self, template_name: str, extension: str) -> bool:
        """Delete an external template."""
        return self.external_loader.delete_template(template_name, extension)

    def render_external_template(self, file_name: str, custom_params: Optional[Dict[str, str]] = None) -> Optional[str]:
        """Render an external template for a file."""
        template = self.find_external_template(file_name)
        if not template:
            return None

        # Get default parameters for this file type
        params = get_external_template_params(file_name)

        # Override with custom parameters if provided
        if custom_params:
            params.update(custom_params)

        # Handle different template formats
        if 'content' in template:
            # Simple template with content field - convert to database format
            db_template = {
                'contenido': template['content'],
                'extension': template.get('extension', 'txt'),
                'nombre': template.get('name', 'External Template')
            }
            return self.render_template(db_template, params)
        elif 'sheets' in template and template.get('extension') == 'xlsx':
            # Excel multi-sheet template
            return self._render_excel_template(template, params)
        else:
            # Fallback - try to use as database template
            db_template = {
                'contenido': str(template),
                'extension': template.get('extension', 'txt'),
                'nombre': template.get('name', 'External Template')
            }
            return self.render_template(db_template, params)

    def _render_excel_template(self, template: Dict[str, Any], params: Dict[str, str]) -> str:
        """Render an Excel multi-sheet template to JSON format."""
        # Convert the template to a JSON string that the Excel renderer can understand
        rendered_template = template.copy()

        # Replace placeholders in all text fields
        def replace_placeholders(obj: Any) -> Any:
            if isinstance(obj, str):
                for key, value in params.items():
                    obj = obj.replace(f"{{{{{key}}}}}", str(value))
                return obj
            elif isinstance(obj, dict):
                return {k: replace_placeholders(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_placeholders(item) for item in obj]
            else:
                return obj

        rendered_template = replace_placeholders(rendered_template)
        return json.dumps(rendered_template, indent=2, ensure_ascii=False)