import json
from pathlib import Path
from typing import Dict, List, Optional

class StructureTemplateLoader:
    """Loads structure templates from JSON files in templates/structures/ directory."""

    def __init__(self, templates_dir: str = "templates/structures"):
        self.templates_dir = Path(templates_dir)
        self.templates: Dict[str, Dict] = {}
        self._load_templates()

    def _load_templates(self) -> None:
        """Load all structure templates from JSON files."""
        if not self.templates_dir.exists():
            self.templates_dir.mkdir(parents=True, exist_ok=True)
            return

        for json_file in self.templates_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    template = json.load(f)
                    if self._validate_template_structure(template):
                        self.templates[template['name']] = template
                    else:
                        print(f"Warning: Invalid template structure in {json_file}")
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Warning: Could not load template {json_file}: {e}")

    @staticmethod
    def _validate_template_structure(template: Dict) -> bool:
        """Validate basic template structure."""
        required_fields = ['name', 'description', 'version', 'structure']
        return all(field in template for field in required_fields) and isinstance(template['structure'], dict)

    def get_template(self, name: str) -> Optional[Dict]:
        """Get a specific template by name."""
        return self.templates.get(name)

    def list_templates(self) -> List[str]:
        """List all available template names."""
        return list(self.templates.keys())

    def get_template_info(self, name: str) -> Optional[Dict]:
        """Get template metadata without the full structure."""
        template = self.get_template(name)
        if template:
            return {
                'name': template['name'],
                'description': template['description'],
                'version': template['version'],
                'author': template.get('author', 'Unknown'),
                'folder_count': len(template['structure'])
            }
        return None

    def list_templates_detailed(self) -> List[Dict]:
        """List all templates with detailed information."""
        return [self.get_template_info(name) for name in self.list_templates() if self.get_template_info(name)]

    def reload_templates(self) -> None:
        """Reload all templates from disk."""
        self.templates.clear()
        self._load_templates()