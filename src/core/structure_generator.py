from typing import Dict, Any, Optional, List
import json
import os
from .database import DatabaseManager
from .enhanced_template_manager import EnhancedTemplateManager
from ..templates.models import TemplateManager

class StructureGenerator:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.template_manager = TemplateManager(db_manager)
        self.enhanced_template_manager = EnhancedTemplateManager(db_manager)
        self.default_structure = self._get_default_structure()

    @staticmethod
    def _get_default_structure() -> List[Dict[str, Any]]:
        """Load the default structure directly from the 'meta-JSON' file."""
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        structure_path = os.path.join(base_dir, 'templates', 'structures', 'default_business_structure.json')

        try:
            with open(structure_path, 'r', encoding='utf-8') as f:
                meta_json = json.load(f)
                return meta_json.get('structure', [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error: Could not load default structure from {structure_path}. Error: {e}")
            return []

    def create_structure(self, project_name: str, base_path: str, structure: Optional[List[Dict[str, Any]]] = None,
                         structure_name: Optional[str] = None) -> str:
        """Creates the full project structure from a hierarchical definition."""
        if not project_name or not project_name.strip():
            raise ValueError("Project name cannot be empty")
        if any(sep in project_name for sep in ['/', '\\']):
            raise ValueError("Project name cannot contain path separators")
        if not base_path or not base_path.strip():
            raise ValueError("Base path cannot be empty")

        structure_to_use = structure if structure is not None else self.default_structure

        root_path = os.path.join(base_path, project_name)
        abs_base = os.path.abspath(base_path)
        abs_root = os.path.abspath(root_path)
        if not abs_root.startswith(abs_base):
            raise ValueError("Invalid base path; path traversal detected")

        try:
            os.makedirs(root_path, exist_ok=True)
            self._create_items_recursively(root_path, structure_to_use)
            self._create_root_structure_md(root_path, structure_to_use)
            return root_path
        except OSError as e:
            raise RuntimeError(f"Failed to create structure: {e}")

    def _create_items_recursively(self, base_path: str, items: List[Dict[str, Any]]):
        """Recursively create directories and files based on the structure definition."""
        for item in items:
            item_name = item.get("name")
            item_type = item.get("type")
            item_path = os.path.join(base_path, item_name)

            if item_type == "dir":
                os.makedirs(item_path, exist_ok=True)
                
                if "description" in item and item["description"]:
                    info_path = os.path.join(item_path, "INFO.md")
                    with open(info_path, 'w', encoding='utf-8') as f:
                        f.write(item["description"])
                
                if "content" in item and isinstance(item["content"], list):
                    self._create_items_recursively(item_path, item["content"])

            elif item_type == "file":
                content = item.get("content_template", f"# {item_name}\n\nContenido base.")
                with open(item_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            elif item.get('template'):
                content = item.get("content_template", f"# {item_name}\n\nContenido base.")
                with open(item_path, 'w', encoding='utf-8') as f:
                    f.write(content)

    def _create_root_structure_md(self, root_path: str, structure: List[Dict[str, Any]]) -> None:
        """Create the main STRUCTURE.md file from the hierarchical structure."""
        tree_structure = self._generate_tree_from_list(structure)
        detailed_structure = self._generate_detailed_docs_from_list(structure)
        total_folders, total_files = self._count_items_from_list(structure)

        info_content = f"""# Estructura del Proyecto: {os.path.basename(root_path)}

Esta carpeta contiene la estructura completa del proyecto organizacional.

## Propósito General
Proporcionar una organización sistemática y profesional para todos los aspectos de gestión empresarial.

## Árbol de Carpetas Completo
```
{os.path.basename(root_path)}/
{tree_structure}
```

## Estructura Detallada del Proyecto
{detailed_structure}

## Estadísticas de la Estructura
- **Total de carpetas**: {total_folders}
- **Total de archivos**: {total_files}

---
*Estructura generada automáticamente por Project Structure Manager*
"""
        structure_path = os.path.join(root_path, "STRUCTURE.md")
        with open(structure_path, 'w', encoding='utf-8') as f:
            f.write(info_content)

    def _generate_tree_from_list(self, items: List[Dict[str, Any]], prefix: str = "") -> str:
        """Generate a string representation of the directory tree from the list structure."""
        result = ""
        for i, item in enumerate(items):
            is_last = (i == len(items) - 1)
            connector = "└── " if is_last else "├── "
            name = item.get("name", "Unnamed")
            
            result += f"{prefix}{connector}{name}"
            
            if item.get("type") == "dir":
                result += "/\n"
                new_prefix = prefix + ("    " if is_last else "│   ")
                if "content" in item and item["content"]:
                    result += self._generate_tree_from_list(item["content"], new_prefix)
            else:
                result += "\n"
        return result

    def _generate_detailed_docs_from_list(self, items: List[Dict[str, Any]], level: int = 0) -> str:
        """Generate the detailed documentation section for STRUCTURE.md."""
        result = ""
        heading = "#" * (level + 2)

        for item in items:
            name = item.get("name")
            description = item.get("description")
            
            if item.get("type") == "dir":
                result += f"\n{heading} 📁 {name}\n\n"
                if description:
                    result += f"{description}\n\n"
                if "content" in item and item["content"]:
                    result += self._generate_detailed_docs_from_list(item["content"], level + 1)
            elif item.get("type") == "file":
                 result += f"- **📄 {name}**: {description or 'Archivo de datos.'}\n"
        return result

    def _count_items_from_list(self, items: List[Dict[str, Any]]) -> tuple[int, int]:
        """Count total folders and files recursively from the list structure."""
        folders = 0
        files = 0
        for item in items:
            if item.get("type") == "dir":
                folders += 1
                sub_folders, sub_files = self._count_items_from_list(item.get("content", []))
                folders += sub_folders
                files += sub_files
            else:
                files += 1
        return folders, files

    def _convert_dict_to_list_structure(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recursively converts the old dict-based structure to the new list-based format."""
        new_list = []
        for key, value in data.items():
            dir_item = {
                "type": "dir",
                "name": key,
                "description": f"Carpeta para {key}",
                "content": []
            }
            if isinstance(value, dict):
                dir_item["content"] = self._convert_dict_to_list_structure(value)
            elif isinstance(value, list):
                file_content = []
                for filename in value:
                    file_content.append({
                        "type": "file",
                        "name": filename,
                        "description": f"Archivo {filename}",
                        "content_template": f"# {filename}\n\nContenido para {filename}."
                    })
                dir_item["content"] = file_content
            new_list.append(dir_item)
        return new_list

    def regenerate_structure(self, project_name: str, base_path: str) -> str:
        """Regenerate existing project structure from the database, handling both old and new formats."""
        existing_project = self.db_manager.get_project_by_name(project_name)
        if not existing_project:
            raise RuntimeError(f"Project '{project_name}' not found in database.")

        structure_from_db = existing_project.get('structure')
        
        if isinstance(structure_from_db, dict):
            structure_to_use = self._convert_dict_to_list_structure(structure_from_db)
        elif isinstance(structure_from_db, list):
            structure_to_use = structure_from_db
        else:
            raise TypeError("Project structure in database is in an unknown or corrupt format.")

        root_path = self.create_structure(project_name, base_path, structure=structure_to_use)
        self.db_manager.update_project(existing_project['id'], structure=structure_to_use, path=root_path)
        return root_path

    def restart_structure(self, project_name: str, base_path: str) -> str:
        """Restart project with the default structure."""
        root_path = self.create_structure(project_name, base_path, self.default_structure)
        existing_project = self.db_manager.get_project_by_name(project_name)

        if existing_project:
            self.db_manager.update_project(existing_project['id'], structure=self.default_structure, path=root_path)
        else:
            self.save_to_db(project_name, self.default_structure, root_path)
        return root_path

    def save_to_db(self, project_name: str, structure: List[Dict[str, Any]], path: Optional[str] = None) -> int:
        return self.db_manager.save_project(project_name, structure, path)

    def load_from_db(self, project_id: int) -> Optional[Dict[str, Any]]:
        return self.db_manager.get_project(project_id)

    def update_in_db(self, project_id: int, structure: List[Dict[str, Any]], path: Optional[str] = None) -> None:
        self.db_manager.update_project(project_id, structure=structure, path=path)

    def get_templates(self) -> List[Dict[str, Any]]:
        return self.db_manager.get_templates()

    def save_template(self, name: str, structure: List[Dict[str, Any]]) -> None:
        self.db_manager.save_template(name, structure)

    def scan_directory(self, path: str) -> List[Dict[str, Any]]:
        """Scan a directory and return its structure in the new list format."""
        items = []
        try:
            for entry in os.scandir(path):
                if entry.is_dir():
                    items.append({
                        "type": "dir",
                        "name": entry.name,
                        "description": f"Carpeta para {entry.name}",
                        "content": self.scan_directory(entry.path)
                    })
                else:
                    items.append({
                        "type": "file",
                        "name": entry.name,
                        "description": f"Archivo {entry.name}"
                    })
        except OSError as e:
            raise RuntimeError(f"Failed to scan directory {path}: {e}")
        return items

    def create_structure_and_save(self, project_name: str, base_path: str,
                                  structure: Optional[List[Dict[str, Any]]] = None,
                                  structure_name: Optional[str] = None) -> str:
        """Create a structure and save to the database."""
        structure_to_use = structure if structure is not None else self.default_structure
        root_path = self.create_structure(project_name, base_path, structure_to_use, structure_name)
        self.save_to_db(project_name, structure_to_use, root_path)
        return root_path

    def check_duplicate_name(self, project_name: str) -> bool:
        """Check if a project name already exists."""
        return self.db_manager.check_duplicate_name(project_name)

    def check_path_conflict(self, project_name: str, path: str) -> Optional[str]:
        """Proxy to database path conflict check."""
        return self.db_manager.check_project_path_conflict(project_name, path)
