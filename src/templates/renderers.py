import os
from abc import ABC, abstractmethod
from typing import Dict, Any
from .models import TemplateManager

class FileRenderer(ABC):
    """Abstract base class for file renderers."""

    @abstractmethod
    def render(self, content: str, output_path: str) -> None:
        """Render content to a file."""
        pass

    @abstractmethod
    def get_extension(self) -> str:
        """Return the file extension this renderer handles."""
        pass

class DocxRenderer(FileRenderer):
    """Renderer for .docx files using python-docx."""

    def get_extension(self) -> str:
        return 'docx'

    def render(self, content: str, output_path: str) -> None:
        from docx import Document
        doc = Document()
        doc.add_paragraph(content)
        doc.save(output_path)

class XlsxRenderer(FileRenderer):
    """Renderer for .xlsx files using openpyxl."""

    def get_extension(self) -> str:
        return 'xlsx'

    def render(self, content: str, output_path: str) -> None:
        from openpyxl import Workbook
        from openpyxl.styles import Font, Alignment, PatternFill
        import json

        wb = Workbook()
        ws = wb.active
        ws.title = "Documento Generado"

        # Try to parse content as structured data
        try:
            # If content contains JSON-like structure, parse it
            if '{' in content and '}' in content:
                # Simple JSON detection
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1 and end > start:
                    json_str = content[start:end]
                    data = json.loads(json_str)
                    self._render_structured_data(ws, data)
                else:
                    self._render_simple_content(ws, content)
            else:
                self._render_simple_content(ws, content)
        except:
            self._render_simple_content(ws, content)

        wb.save(output_path)

    def _render_simple_content(self, ws, content: str) -> None:
        """Render simple text content."""
        from openpyxl.styles import Font, Alignment

        # Split content into lines
        lines = content.split('\n')

        # Title
        if lines:
            ws['A1'] = lines[0]
            ws['A1'].font = Font(size=16, bold=True)
            ws['A1'].alignment = Alignment(horizontal='center')

        # Content
        for i, line in enumerate(lines[1:], 2):
            if line.strip():
                ws[f'A{i}'] = line
                if line.startswith('#'):
                    ws[f'A{i}'].font = Font(bold=True)
                elif line.startswith('##'):
                    ws[f'A{i}'].font = Font(size=14, bold=True)

        # Auto-adjust column width
        ws.column_dimensions['A'].width = 50

    def _render_structured_data(self, ws, data: Dict[str, Any]) -> None:
        """Render structured data with headers and tables."""
        from openpyxl.styles import Font, Alignment, PatternFill

        row = 1

        # Title
        if 'titulo' in data:
            ws[f'A{row}'] = data['titulo']
            ws[f'A{row}'].font = Font(size=16, bold=True)
            ws[f'A{row}'].alignment = Alignment(horizontal='center')
            ws.merge_cells(f'A{row}:E{row}')
            row += 2

        # Company and date
        if 'empresa' in data:
            ws[f'A{row}'] = f"Empresa: {data['empresa']}"
            ws[f'A{row}'].font = Font(italic=True)
            row += 1

        if 'fecha' in data and 'hora' in data:
            ws[f'A{row}'] = f"Fecha: {data['fecha']} | Hora: {data['hora']}"
            ws[f'A{row}'].font = Font(italic=True)
            row += 2

        # Table of contents
        if any(key.startswith('seccion') for key in data.keys()):
            ws[f'A{row}'] = "Tabla de Contenido"
            ws[f'A{row}'].font = Font(bold=True, underline='single')
            row += 1

            for key, value in data.items():
                if key.startswith('seccion'):
                    ws[f'A{row}'] = f"- {value}"
                    row += 1
            row += 1

        # Main content sections
        sections = ['introduccion', 'objetivo', 'contenido', 'conclusiones']
        for section in sections:
            if section in data:
                ws[f'A{row}'] = section.replace('_', ' ').title()
                ws[f'A{row}'].font = Font(size=14, bold=True)
                ws[f'A{row}'].fill = PatternFill(start_color="E6E6FA", end_color="E6E6FA", fill_type="solid")
                row += 1

                # Handle different content types
                content_value = data[section]
                if isinstance(content_value, str):
                    # Split long text into multiple cells
                    content_lines = content_value.split('\n')
                    for line in content_lines:
                        if line.strip():
                            ws[f'A{row}'] = line
                            row += 1
                elif isinstance(content_value, list):
                    # Render as simple list
                    for item in content_value:
                        ws[f'A{row}'] = f"• {item}"
                        row += 1
                elif isinstance(content_value, dict):
                    # Render as table
                    if content_value:  # Only if not empty
                        # Headers
                        col = 1
                        for header in content_value.keys():
                            ws.cell(row=row, column=col, value=header)
                            ws.cell(row=row, column=col).font = Font(bold=True)
                            ws.cell(row=row, column=col).fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
                            col += 1
                        row += 1

                        # Data rows
                        max_rows = max(len(v) if isinstance(v, list) else 1 for v in content_value.values())
                        for i in range(max_rows):
                            col = 1
                            for header, values in content_value.items():
                                if isinstance(values, list) and i < len(values):
                                    ws.cell(row=row, column=col, value=values[i])
                                elif not isinstance(values, list):
                                    ws.cell(row=row, column=col, value=values)
                                col += 1
                            row += 1
                row += 1

        # Footer
        ws[f'A{row}'] = "Generado automáticamente por Project Manager"
        ws[f'A{row}'].font = Font(size=10, italic=True)
        ws[f'A{row}'].alignment = Alignment(horizontal='center')
        ws.merge_cells(f'A{row}:E{row}')

        # Auto-adjust column widths
        for col in ['A', 'B', 'C', 'D', 'E']:
            ws.column_dimensions[col].width = 20

class HtmlRenderer(FileRenderer):
    """Renderer for .html files."""

    def get_extension(self) -> str:
        return 'html'

    def render(self, content: str, output_path: str) -> None:
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Generated Document</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        p {{ line-height: 1.6; }}
    </style>
</head>
<body>
    <p>{content}</p>
</body>
</html>
        """
        with open(output_path, 'w') as f:
            f.write(html_content)

class MdRenderer(FileRenderer):
    """Renderer for .md files."""

    def get_extension(self) -> str:
        return 'md'

    def render(self, content: str, output_path: str) -> None:
        with open(output_path, 'w') as f:
            f.write(content)

class TxtRenderer(FileRenderer):
    """Renderer for .txt files."""

    def get_extension(self) -> str:
        return 'txt'

    def render(self, content: str, output_path: str) -> None:
        with open(output_path, 'w') as f:
            f.write(content)

class RendererFactory:
    """Factory to get the appropriate renderer."""

    _renderers = {
        'docx': DocxRenderer(),
        'xlsx': XlsxRenderer(),
        'html': HtmlRenderer(),
        'md': MdRenderer(),
        'txt': TxtRenderer(),
    }

    @classmethod
    def get_renderer(cls, extension: str) -> FileRenderer:
        """Get renderer for the given extension."""
        if extension not in cls._renderers:
            raise ValueError(f"Unsupported extension: {extension}")
        return cls._renderers[extension]

    @classmethod
    def add_renderer(cls, extension: str, renderer: FileRenderer) -> None:
        """Add a new renderer for a custom extension."""
        cls._renderers[extension] = renderer