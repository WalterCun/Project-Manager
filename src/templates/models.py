import re
from typing import Dict, Any, Optional, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.database import DatabaseManager, Template

class TemplateNotFoundError(Exception):
    pass

class InvalidPlaceholderError(Exception):
    pass

class TemplateManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

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