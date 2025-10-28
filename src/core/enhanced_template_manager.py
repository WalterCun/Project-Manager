from typing import Dict, Any, Optional, List
from pathlib import Path
import json
from .database import DatabaseManager
from .template_loader import StructureTemplateLoader
from .native_renderers import ExcelNativeRenderer, WordNativeRenderer, Jinja2Renderer

class EnhancedTemplateManager:
    """Enhanced template manager supporting multiple template types and native rendering."""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.structure_loader = StructureTemplateLoader()
        self.native_renderers = {
            'xlsx': ExcelNativeRenderer(),
            'docx': WordNativeRenderer(),
            'html': Jinja2Renderer(),
            'json': None  # JSON templates are handled differently
        }

    def get_structure_template(self, name: str) -> Optional[Dict]:
        """Get a structure template by name."""
        return self.structure_loader.get_template(name)

    def list_structure_templates(self) -> List[str]:
        """List all available structure template names."""
        return self.structure_loader.list_templates()

    def list_structure_templates_detailed(self) -> List[Dict]:
        """List all structure templates with detailed information."""
        return self.structure_loader.list_templates_detailed()

    def render_native_template(self, template_name: str, extension: str, params: Dict[str, Any]) -> bytes:
        """Render a native template (Excel, Word, HTML) with parameters."""
        if extension not in self.native_renderers:
            raise ValueError(f"Unsupported template extension: {extension}")

        renderer = self.native_renderers[extension]
        if renderer is None:
            raise ValueError(f"No renderer available for extension: {extension}")

        # Load template from file
        template_path = Path(f"templates/{extension}/{template_name}.json")
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        with open(template_path, 'r', encoding='utf-8') as f:
            template_data = json.load(f)

        return renderer.render(template_data, params)

    def render_template_from_data(self, template_data: Dict, extension: str, params: Dict[str, Any]) -> Any:
        """Render template directly from data dictionary."""
        if extension not in self.native_renderers:
            raise ValueError(f"Unsupported template extension: {extension}")

        renderer = self.native_renderers[extension]
        if renderer is None:
            raise ValueError(f"No renderer available for extension: {extension}")

        return renderer.render(template_data, params)

    def validate_template(self, template_data: Dict, extension: str) -> List[str]:
        """Validate a template structure."""
        errors = []

        if extension == 'xlsx':
            errors.extend(self._validate_excel_template(template_data))
        elif extension == 'docx':
            errors.extend(self._validate_word_template(template_data))
        elif extension == 'html':
            errors.extend(self._validate_html_template(template_data))
        elif extension == 'json':
            errors.extend(self._validate_structure_template(template_data))
        else:
            errors.append(f"Unknown template extension: {extension}")

        return errors

    @staticmethod
    def _validate_excel_template(template: Dict) -> List[str]:
        """Validate Excel template structure."""
        errors = []
        if 'sheets' not in template:
            errors.append("Excel template must have 'sheets' section")
        elif not isinstance(template['sheets'], dict):
            errors.append("'sheets' must be a dictionary")
        else:
            for sheet_name, sheet_config in template['sheets'].items():
                if not isinstance(sheet_config, dict):
                    errors.append(f"Sheet '{sheet_name}' configuration must be a dictionary")
        return errors

    @staticmethod
    def _validate_word_template(template: Dict) -> List[str]:
        """Validate Word template structure."""
        errors = []
        if 'document' not in template:
            errors.append("Word template must have 'document' section")
        elif not isinstance(template['document'], dict):
            errors.append("'document' must be a dictionary")
        return errors

    @staticmethod
    def _validate_html_template(template: Dict) -> List[str]:
        """Validate HTML template structure."""
        errors = []
        if 'content' not in template:
            errors.append("HTML template must have 'content' field")
        elif not isinstance(template['content'], str):
            errors.append("'content' must be a string")
        return errors

    @staticmethod
    def _validate_structure_template(template: Dict) -> List[str]:
        """Validate structure template."""
        errors = []
        required_fields = ['name', 'description', 'version', 'structure']
        for field in required_fields:
            if field not in template:
                errors.append(f"Missing required field: {field}")

        if 'structure' in template and not isinstance(template['structure'], dict):
            errors.append("'structure' must be a dictionary")

        return errors

    @staticmethod
    def get_template_metadata(template_name: str, extension: str) -> Optional[Dict]:
        """Get template metadata without loading full content."""
        try:
            template_path = Path(f"templates/{extension}/{template_name}.json")
            if not template_path.exists():
                return None

            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)

            return {
                'name': template_data.get('name', template_name),
                'extension': extension,
                'description': template_data.get('description', ''),
                'version': template_data.get('version', '1.0'),
                'author': template_data.get('author', 'Unknown')
            }
        except (json.JSONDecodeError, FileNotFoundError):
            return None

    def list_native_templates(self, extension: Optional[str] = None) -> List[Dict]:
        """List all native templates, optionally filtered by extension."""
        templates = []

        template_dirs = [extension] if extension else ['excel', 'docx', 'html', 'md']

        for ext in template_dirs:
            template_dir = Path(f"templates/{ext}")
            if template_dir.exists():
                for json_file in template_dir.glob("*.json"):
                    template_name = json_file.stem
                    metadata = self.get_template_metadata(template_name, ext)
                    if metadata:
                        templates.append(metadata)

        return templates

    def reload_structure_templates(self) -> None:
        """Reload structure templates from disk."""
        self.structure_loader.reload_templates()