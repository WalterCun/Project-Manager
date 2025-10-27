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
                    self._render_excel_template(wb, data)
                else:
                    self._render_simple_content(wb.active, content)
            else:
                self._render_simple_content(wb.active, content)
        except Exception as e:
            print(f"Warning: Failed to render Excel template: {e}")
            self._render_simple_content(wb.active, content)

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

    def _render_excel_template(self, wb, data: Dict[str, Any]) -> None:
        """Render a multi-sheet Excel template."""
        from openpyxl.styles import Font, Alignment, PatternFill

        # Handle multi-sheet templates
        if 'sheets' in data:
            self._render_multi_sheet_excel(wb, data)
        else:
            # Fallback to single sheet
            self._render_structured_data(wb.active, data)

    def _render_multi_sheet_excel(self, wb, data: Dict[str, Any]) -> None:
        """Render multi-sheet Excel template."""
        from openpyxl.styles import Font, Alignment, PatternFill

        sheets = data.get('sheets', {})
        global_styles = data.get('global_styles', {})

        # Remove default sheet if multiple sheets are defined
        if len(sheets) > 1:
            wb.remove(wb.active)

        for sheet_name, sheet_config in sheets.items():
            ws = wb.create_sheet(title=sheet_name)

            # Apply sheet description as comment if available
            if 'description' in sheet_config:
                ws.cell(1, 1).comment = sheet_config['description']

            # Render cells
            if 'cells' in sheet_config:
                self._render_cells(ws, sheet_config['cells'], global_styles)

            # Render tables
            if 'tables' in sheet_config:
                self._render_tables(ws, sheet_config['tables'], global_styles)

            # Render charts (placeholder for future implementation)
            if 'charts' in sheet_config:
                self._render_charts_placeholder(ws, sheet_config['charts'])

    def _render_cells(self, ws, cells: Dict[str, Any], global_styles: Dict[str, Any]) -> None:
        """Render individual cells with styles."""
        from openpyxl.styles import Font, Alignment, PatternFill

        for cell_ref, cell_config in cells.items():
            if 'value' in cell_config:
                ws[cell_ref] = cell_config['value']
            elif 'formula' in cell_config:
                ws[cell_ref] = cell_config['formula']

            # Apply styles
            if 'style' in cell_config:
                style = cell_config['style']
                cell = ws[cell_ref]

                if 'bold' in style and style['bold']:
                    cell.font = Font(bold=True)
                if 'font_size' in style:
                    if not cell.font:
                        cell.font = Font()
                    cell.font = Font(size=style['font_size'], bold=cell.font.bold if cell.font else False)
                if 'font_color' in style:
                    if not cell.font:
                        cell.font = Font()
                    cell.font = Font(color=style['font_color'], size=cell.font.size if cell.font else 11)
                if 'fill' in style:
                    fill_config = style['fill']
                    if fill_config.get('pattern') == 'solid' and 'color' in fill_config:
                        cell.fill = PatternFill(start_color=fill_config['color'], end_color=fill_config['color'], fill_type="solid")
                if 'alignment' in style:
                    align_config = style['alignment']
                    cell.alignment = Alignment(horizontal=align_config.get('horizontal', 'left'))

    def _render_tables(self, ws, tables: Dict[str, Any], global_styles: Dict[str, Any]) -> None:
        """Render table structures."""
        from openpyxl.styles import Font, PatternFill

        for table_name, table_config in tables.items():
            range_str = table_config.get('range', '')
            if not range_str:
                continue

            # Parse range (e.g., "B7:D9")
            try:
                start_col, start_row = self._parse_cell_ref(range_str.split(':')[0])
                end_col, end_row = self._parse_cell_ref(range_str.split(':')[1])

                # Apply table styling
                style = table_config.get('style', {})

                # Style headers
                if table_config.get('headers', False):
                    for col in range(start_col, end_col + 1):
                        cell = ws.cell(start_row, col)
                        if style.get('header_fill'):
                            cell.fill = PatternFill(start_color=style['header_fill'], end_color=style['header_fill'], fill_type="solid")
                        if style.get('header_font_color'):
                            cell.font = Font(color=style['header_font_color'], bold=True)

                # Apply borders if specified
                if style.get('border'):
                    for row in range(start_row, end_row + 1):
                        for col in range(start_col, end_col + 1):
                            cell = ws.cell(row, col)
                            # Add border styling here when needed

            except Exception as e:
                print(f"Warning: Failed to render table {table_name}: {e}")

    def _render_charts_placeholder(self, ws, charts: Dict[str, Any]) -> None:
        """Add placeholder text for charts (future implementation)."""
        for chart_name, chart_config in charts.items():
            position = chart_config.get('position', 'A1')
            ws[position] = f"[Chart: {chart_name}] - {chart_config.get('type', 'unknown')}"

    def _parse_cell_ref(self, cell_ref: str) -> tuple:
        """Parse cell reference like 'B7' to (col, row)."""
        import re
        match = re.match(r'([A-Z]+)(\d+)', cell_ref)
        if match:
            col_str, row_str = match.groups()
            col = 0
            for i, char in enumerate(col_str):
                col += (ord(char) - ord('A') + 1) * (26 ** (len(col_str) - i - 1))
            return (col, int(row_str))
        return (1, 1)

    def _render_structured_data(self, ws, data: Dict[str, Any]) -> None:
        """Render structured data with headers and tables (fallback method)."""
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

        # Main content sections
        sections = ['introduccion', 'objetivo', 'contenido', 'conclusiones']
        for section in sections:
            if section in data:
                ws[f'A{row}'] = section.replace('_', ' ').title()
                ws[f'A{row}'].font = Font(size=14, bold=True)
                ws[f'A{row}'].fill = PatternFill(start_color="E6E6FA", end_color="E6E6FA", fill_type="solid")
                row += 1

                content_value = data[section]
                if isinstance(content_value, str):
                    content_lines = content_value.split('\n')
                    for line in content_lines:
                        if line.strip():
                            ws[f'A{row}'] = line
                            row += 1
                elif isinstance(content_value, dict) and content_value:
                    # Render as table
                    col = 1
                    for header in content_value.keys():
                        ws.cell(row=row, column=col, value=header)
                        ws.cell(row=row, column=col).font = Font(bold=True)
                        ws.cell(row=row, column=col).fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
                        col += 1
                    row += 1

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