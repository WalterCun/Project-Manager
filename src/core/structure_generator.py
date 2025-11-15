from typing import Dict, Any, Optional, List
import json
import os
from .database import DatabaseManager
from .enhanced_template_manager import EnhancedTemplateManager
from ..templates.models import TemplateManager

# Import PDF generation libraries, handling potential ImportError
try:
    import markdown
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

class StructureGenerator:
    def __init__(self, db_manager: DatabaseManager, doc_format: str = 'pdf'):
        if doc_format == 'pdf' and not PDF_SUPPORT:
            raise ImportError("PDF generation is selected, but required libraries (reportlab, markdown) are not installed. Please run 'pip install reportlab markdown'.")
        self.db_manager = db_manager
        self.template_manager = TemplateManager(db_manager)
        self.enhanced_template_manager = EnhancedTemplateManager(db_manager)
        self.default_structure = self._get_default_structure()
        self.doc_format = doc_format

    def _get_default_structure(self) -> List[Dict[str, Any]]:
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
            self._create_root_structure_file(root_path, structure_to_use)
            return root_path
        except OSError as e:
            raise RuntimeError(f"Failed to create structure: {e}")

    def _write_doc_file(self, file_path_without_ext: str, content: str):
        """Writes content to a file, either .md or .pdf based on doc_format."""
        if self.doc_format == 'pdf':
            pdf_path = file_path_without_ext + '.pdf'
            self._convert_md_to_pdf(content, pdf_path)
        else:
            md_path = file_path_without_ext + '.md'
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(content)

    def _convert_md_to_pdf(self, md_content: str, pdf_path: str):
        """Converts a string of Markdown content to a PDF file with a fallback."""
        if not PDF_SUPPORT:
            print("Warning: PDF libraries not installed. Skipping PDF generation.")
            return

        try:
            doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch, leftMargin=0.7*inch, rightMargin=0.7*inch)
            styles = getSampleStyleSheet()
            
            styles.add(ParagraphStyle(name='H1', parent=styles['h1'], fontSize=18, spaceAfter=12))
            styles.add(ParagraphStyle(name='H2', parent=styles['h2'], fontSize=14, spaceAfter=10))
            styles.add(ParagraphStyle(name='H3', parent=styles['h3'], fontSize=12, spaceAfter=8))
            styles.add(ParagraphStyle(name='Body', parent=styles['Normal'], spaceAfter=6, leading=14))
            code_style = ParagraphStyle(name='Code', parent=styles['Normal'], fontName='Courier', fontSize=8.5, leading=10, leftIndent=10, rightIndent=10)

            story = []
            in_code_block = False
            code_text = []

            for line in md_content.split('\n'):
                stripped_line = line.strip()
                if stripped_line.startswith('```'):
                    if in_code_block:
                        story.append(Preformatted('\n'.join(code_text), code_style))
                        code_text = []
                    in_code_block = not in_code_block
                    continue

                if in_code_block:
                    code_text.append(line)
                    continue

                if line.startswith('# '):
                    story.append(Paragraph(line[2:], styles['H1']))
                elif line.startswith('## '):
                    story.append(Paragraph(line[3:], styles['H2']))
                elif line.startswith('### '):
                    story.append(Paragraph(line[4:], styles['H3']))
                elif stripped_line.startswith('- '):
                    story.append(Paragraph(f'• {stripped_line[2:]}', styles['Body'], leftIndent=10))
                else:
                    story.append(Paragraph(line, styles['Body']))
            
            doc.build(story)
        except Exception as e:
            print(f"CRITICAL WARNING: Failed to generate PDF '{os.path.basename(pdf_path)}'. Writing as .md instead. Error: {e}")
            md_path = pdf_path.replace('.pdf', '.md')
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write("--- PDF GENERATION FAILED ---\n\n" + md_content)

    def _create_items_recursively(self, base_path: str, items: List[Dict[str, Any]]):
        """Recursively create directories and files based on the structure definition."""
        for item in items:
            item_name = item.get("name")
            if not item_name:
                continue
            
            item_path = os.path.join(base_path, item_name)
            item_type = item.get("type")

            if item_type == "dir":
                os.makedirs(item_path, exist_ok=True)
                
                description_content = item.get("description", "")
                if "content" in item and item["content"]:
                    tree_for_info_md = self._generate_tree_from_list(item["content"])
                    description_content += f"\n\n## Estructura\n```\n{item_name}/\n{tree_for_info_md}```"
                
                if description_content:
                    try:
                        self._write_doc_file(os.path.join(item_path, "INFO"), description_content)
                    except Exception as e:
                        print(f"ERROR: Failed to generate documentation for {item_path}. Error: {e}")

                if "content" in item and isinstance(item["content"], list):
                    self._create_items_recursively(item_path, item["content"])

            elif item_type == "file" or item.get('template'):
                content = item.get("content_template", f"# {item_name}\n\nContenido base.")
                with open(item_path, 'w', encoding='utf-8') as f:
                    f.write(content)

    def _create_root_structure_file(self, root_path: str, structure: List[Dict[str, Any]]) -> None:
        """Create the main STRUCTURE file in the chosen format."""
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
        try:
            self._write_doc_file(os.path.join(root_path, "STRUCTURE"), info_content)
        except Exception as e:
            print(f"ERROR: Failed to generate root STRUCTURE file. Error: {e}")

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
        heading_level = level + 2
        heading = "#" * heading_level

        for item in items:
            name = item.get("name")
            description = item.get("description", "Sin descripción.")
            
            if item.get("type") == "dir":
                if level == 0:
                    result += f"\n{heading} 📁 {name}\n\n{description}\n"
                else:
                    result += f"\n{heading} 📁 {name}\n\n**Propósito**: {description}\n"

                if "content" in item and item["content"]:
                    files_in_dir = [f for f in item["content"] if f.get("type") != "dir"]
                    if files_in_dir:
                        result += "\n**Archivos:**\n"
                        for file_item in files_in_dir:
                            result += f"- **{file_item.get('name')}**: {file_item.get('description', 'Archivo de datos.')}\n"
                    
                    sub_dirs = [d for d in item["content"] if d.get("type") == "dir"]
                    if sub_dirs:
                         result += self._generate_detailed_docs_from_list(sub_dirs, level + 1)
                result += "\n---\n"
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
