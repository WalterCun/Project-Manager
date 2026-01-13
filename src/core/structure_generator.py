from typing import Dict, Any, Optional, List
import json
import os

# --- Dependency Imports with Graceful Fallbacks ---
try:
    import markdown
    from markdown_pdf import PdfConverter
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    import imgkit
    IMG_SUPPORT = True
except ImportError:
    IMG_SUPPORT = False

class DatabaseManager:
    pass

class StructureGenerator:
    def __init__(self, db_manager: Optional['DatabaseManager'] = None, doc_format: str = 'pdf'):
        if doc_format == 'pdf' and not PDF_SUPPORT:
            raise ImportError("PDF format selected, but 'markdown-pdf' is not installed. Please run 'pip install markdown-pdf'.")
        if doc_format == 'img' and not IMG_SUPPORT:
            raise ImportError("Image format selected, but 'imgkit' is not installed. Please run 'pip install imgkit' and ensure wkhtmltoimage is in your system's PATH.")
        
        self.db_manager = db_manager
        self.doc_format = doc_format
        self.default_structure = self._get_default_structure()

        if self.db_manager:
            from .enhanced_template_manager import EnhancedTemplateManager
            from ..templates.models import TemplateManager
            self.template_manager = TemplateManager(self.db_manager)
            self.enhanced_template_manager = EnhancedTemplateManager(self.db_manager)

    def _get_default_structure(self) -> List[Dict[str, Any]]:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        structure_path = os.path.join(base_dir, 'templates', 'structures', 'default_business_structure.json')
        try:
            with open(structure_path, 'r', encoding='utf-8') as f:
                return json.load(f).get('structure', [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error: Could not load default structure from {structure_path}. Error: {e}")
            return []

    def create_structure(self, project_name: str, base_path: str, structure: Optional[List[Dict[str, Any]]] = None) -> str:
        if not project_name or not project_name.strip(): raise ValueError("Project name cannot be empty")
        if any(sep in project_name for sep in ['/', '\\']): raise ValueError("Project name cannot contain path separators")
        if not base_path or not base_path.strip(): raise ValueError("Base path cannot be empty")

        structure_to_use = structure if structure is not None else self.default_structure
        root_path = os.path.join(base_path, project_name)
        
        try:
            os.makedirs(root_path, exist_ok=True)
            self._create_items_recursively(root_path, structure_to_use)
            self._create_root_structure_file(root_path, structure_to_use)
            return root_path
        except OSError as e:
            raise RuntimeError(f"Failed to create structure: {e}")

    def _write_doc_file(self, file_path_without_ext: str, content: str):
        if self.doc_format == 'pdf':
            self._convert_md_to_pdf(content, file_path_without_ext + '.pdf')
        elif self.doc_format == 'img':
            self._convert_md_to_image(content, file_path_without_ext + '.png')
        else:
            with open(file_path_without_ext + '.md', 'w', encoding='utf-8') as f: f.write(content)

    def _convert_md_to_pdf(self, md_content: str, pdf_path: str):
        if not PDF_SUPPORT: return
        try:
            converter = PdfConverter(output_file=pdf_path)
            converter.convert_string(md_content)
        except Exception as e:
            print(f"CRITICAL WARNING: Failed to generate PDF '{os.path.basename(pdf_path)}'. Writing as .md instead. Error: {e}")
            with open(pdf_path.replace('.pdf', '.md'), 'w', encoding='utf-8') as f:
                f.write("--- PDF GENERATION FAILED ---\n\n" + md_content)

    def _convert_md_to_image(self, md_content: str, img_path: str):
        if not IMG_SUPPORT: return
        
        # --- Explicitly define the path to the wkhtmltoimage executable ---
        # This is the most common installation path on Windows.
        # If your path is different, you can change this variable.
        wkhtmltoimage_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'

        if not os.path.exists(wkhtmltoimage_path):
            print(f"ERROR: wkhtmltoimage not found at the specified path: {wkhtmltoimage_path}")
            print("Please install wkhtmltopdf (https://wkhtmltopdf.org/downloads.html) to the default location or update the path in structure_generator.py")
            # Fallback to writing MD
            with open(img_path.replace('.png', '.md'), 'w', encoding='utf-8') as f:
                f.write("--- IMAGE GENERATION FAILED: wkhtmltoimage not found ---\n\n" + md_content)
            return

        config = imgkit.config(wkhtmltoimage=wkhtmltoimage_path)
        
        html_content = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])
        
        css = """
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #fff; width: 960px; margin: auto; }
            h1, h2, h3 { color: #2c3e50; border-bottom: 1px solid #eaecef; padding-bottom: .3em; }
            h1 { font-size: 2em; }
            h2 { font-size: 1.5em; }
            h3 { font-size: 1.2em; }
            pre { background-color: #f6f8fa; padding: 16px; overflow: auto; font-size: 85%; line-height: 1.45; border-radius: 6px; }
            code { font-family: 'Courier New', Courier, monospace; }
            ul { padding-left: 20px; }
        </style>
        """
        full_html = f"<html><head><meta charset='UTF-8'>{css}</head><body>{html_content}</body></html>"
        
        try:
            imgkit.from_string(full_html, img_path, options={'width': 1000}, config=config)
        except Exception as e:
            print(f"CRITICAL WARNING: Failed to generate Image '{os.path.basename(img_path)}'. Writing as .md instead. Error: {e}")
            with open(img_path.replace('.png', '.md'), 'w', encoding='utf-8') as f:
                f.write("--- IMAGE GENERATION FAILED ---\n\n" + md_content)

    def _create_items_recursively(self, base_path: str, items: List[Dict[str, Any]]):
        for item in items:
            item_name = item.get("name")
            if not item_name: continue
            item_path = os.path.join(base_path, item_name)
            item_type = item.get("type")
            if item_type == "dir":
                os.makedirs(item_path, exist_ok=True)
                description_content = item.get("description", "")
                if "content" in item and item["content"]:
                    tree_for_info = self._generate_tree_from_list(item["content"])
                    description_content += f"\n\n## Estructura\n```\n📁 {item_name}/\n{tree_for_info}```"
                if description_content:
                    try: self._write_doc_file(os.path.join(item_path, "INFO"), description_content)
                    except Exception as e: print(f"ERROR: Failed to generate doc for {item_path}. Error: {e}")
                if "content" in item and isinstance(item["content"], list):
                    self._create_items_recursively(item_path, item["content"])
            elif item_type == "file" or item.get('template'):
                content = item.get("content_template", f"# {item_name}\n\nContenido base.")
                with open(item_path, 'w', encoding='utf-8') as f: f.write(content)

    def _create_root_structure_file(self, root_path: str, structure: List[Dict[str, Any]]):
        tree = self._generate_tree_from_list(structure)
        details = self._generate_detailed_docs_from_list(structure)
        folders, files = self._count_items_from_list(structure)
        content = f"""# Estructura del Proyecto: {os.path.basename(root_path)}

## Árbol de Carpetas Completo
```
📁 {os.path.basename(root_path)}/
{tree}
```

## Estructura Detallada del Proyecto
{details}

## Estadísticas de la Estructura
- **Total de carpetas**: {folders}
- **Total de archivos**: {files}

---
*Estructura generada automáticamente por Project Structure Manager*
"""
        try: self._write_doc_file(os.path.join(root_path, "STRUCTURE"), content)
        except Exception as e: print(f"ERROR: Failed to generate root STRUCTURE file. Error: {e}")

    def _generate_tree_from_list(self, items: List[Dict[str, Any]], prefix: str = "") -> str:
        result = ""
        for i, item in enumerate(items):
            is_last = (i == len(items) - 1)
            connector = "└── " if is_last else "├── "
            name = item.get("name", "Unnamed")
            icon = "📁" if item.get("type") == "dir" else "📄"
            result += f"{prefix}{connector}{icon} {name}"
            if item.get("type") == "dir":
                result += "/\n"
                new_prefix = prefix + ("    " if is_last else "│   ")
                if "content" in item and item["content"]:
                    result += self._generate_tree_from_list(item["content"], new_prefix)
            else: result += "\n"
        return result

    def _generate_detailed_docs_from_list(self, items: List[Dict[str, Any]], level: int = 0) -> str:
        result = ""
        heading = "#" * (level + 2)
        for item in items:
            name, desc = item.get("name"), item.get("description", "Sin descripción.")
            if item.get("type") == "dir":
                result += f"\n{heading} 📁 {name}\n\n" + (f"{desc}\n" if level == 0 else f"**Propósito**: {desc}\n")
                if "content" in item and item["content"]:
                    files = [f for f in item["content"] if f.get("type") != "dir"]
                    if files:
                        result += "\n**Archivos:**\n"
                        for f in files: result += f"- 📄 **{f.get('name')}**: {f.get('description', 'Archivo de datos.')}\n"
                    sub_dirs = [d for d in item["content"] if d.get("type") == "dir"]
                    if sub_dirs: result += self._generate_detailed_docs_from_list(sub_dirs, level + 1)
                result += "\n---\n"
        return result

    def _count_items_from_list(self, items: List[Dict[str, Any]]) -> tuple[int, int]:
        folders, files = 0, 0
        for item in items:
            if item.get("type") == "dir":
                folders += 1
                sub_folders, sub_files = self._count_items_from_list(item.get("content", []))
                folders += sub_folders
                files += sub_files
            else: files += 1
        return folders, files
    
    def _ensure_db(self):
        if not self.db_manager: raise ConnectionError("Database connection is not available for this operation.")

    def _convert_dict_to_list_structure(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        new_list = []
        for key, value in data.items():
            dir_item = {"type": "dir", "name": key, "description": f"Carpeta para {key}", "content": []}
            if isinstance(value, dict):
                dir_item["content"] = self._convert_dict_to_list_structure(value)
            elif isinstance(value, list):
                dir_item["content"] = [{"type": "file", "name": f, "description": f"Archivo {f}", "content_template": f"# {f}"} for f in value]
            new_list.append(dir_item)
        return new_list

    def regenerate_structure(self, project_name: str, base_path: str) -> str:
        self._ensure_db()
        existing_project = self.db_manager.get_project_by_name(project_name)
        if not existing_project: raise RuntimeError(f"Project '{project_name}' not found in database.")
        structure_from_db = existing_project.get('structure')
        structure_to_use = self._convert_dict_to_list_structure(structure_from_db) if isinstance(structure_from_db, dict) else structure_from_db
        if not isinstance(structure_to_use, list): raise TypeError("Project structure in database is in an unknown or corrupt format.")
        root_path = self.create_structure(project_name, base_path, structure=structure_to_use)
        self.db_manager.update_project(existing_project['id'], structure=structure_to_use, path=root_path)
        return root_path

    def restart_structure(self, project_name: str, base_path: str) -> str:
        self._ensure_db()
        root_path = self.create_structure(project_name, base_path, self.default_structure)
        existing_project = self.db_manager.get_project_by_name(project_name)
        if existing_project:
            self.db_manager.update_project(existing_project['id'], structure=self.default_structure, path=root_path)
        else:
            self.save_to_db(project_name, self.default_structure, root_path)
        return root_path

    def create_structure_and_save(self, project_name: str, base_path: str, structure_name: Optional[str] = None) -> str:
        self._ensure_db()
        structure_to_use = self.default_structure
        if structure_name and structure_name != "Default Business Structure":
            if not hasattr(self, 'enhanced_template_manager'): raise ConnectionError("DB connection required for custom templates.")
            template_data = self.enhanced_template_manager.get_structure_template(structure_name)
            if not template_data: raise ValueError(f"Custom template '{structure_name}' not found.")
            structure_to_use = template_data.get('structure')
            if not isinstance(structure_to_use, list): raise TypeError(f"Template '{structure_name}' has invalid format.")
        root_path = self.create_structure(project_name, base_path, structure_to_use)
        self.save_to_db(project_name, structure_to_use, root_path)
        return root_path
    
    def save_to_db(self, project_name: str, structure: List[Dict[str, Any]], path: Optional[str] = None) -> int:
        self._ensure_db()
        return self.db_manager.save_project(project_name, structure, path)
