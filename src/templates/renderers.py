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
        wb = Workbook()
        ws = wb.active
        ws['A1'] = content
        wb.save(output_path)

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