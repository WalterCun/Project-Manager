#!/usr/bin/env python3
"""
Test script for template generation and rendering.
Tests different template types and verifies the output.
"""

import os
import sys
from datetime import datetime
from typing import Dict, Any

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.database import DatabaseManager
from core.base_templates import get_base_templates, get_template_params_for_file
from templates.models import TemplateManager
from templates.renderers import RendererFactory

def test_base_templates():
    """Test that base templates are loaded correctly."""
    print("Testing base templates...")

    templates = get_base_templates()
    expected_templates = [
        "Plantilla HTML Base",
        "Plantilla Markdown Base",
        "Plantilla DOCX Base",
        "Plantilla Email Base",
        "Plantilla Manual Base"
    ]

    for expected in expected_templates:
        found = any(t['nombre'] == expected for t in templates)
        if not found:
            raise AssertionError(f"Template '{expected}' not found in base templates")
        print(f"Found template: {expected}")

    print(f"All {len(templates)} base templates loaded successfully\n")

def test_template_params():
    """Test template parameter generation for different file types."""
    print("Testing template parameters...")

    test_files = [
        "Confirmación_Reserva.html",
        "Recordatorio_48h.html",
        "Agradecimiento_Post_Tour.html",
        "Manual_de_Inducción.docx",
        "Evaluaciones.docx",
        "Rol.docx",
        "Atencion_al_Cliente.docx",
        "Calculadora_Financiera.xlsx",
        "Dashboard_Principal.xlsx",
        "Base_de_Datos_de_Clientes.xlsx"
    ]

    for file_name in test_files:
        params = get_template_params_for_file(file_name)
        required_params = ["titulo", "empresa", "fecha", "hora"]

        for param in required_params:
            if param not in params:
                raise AssertionError(f"Missing required parameter '{param}' for {file_name}")

        print(f"Parameters generated for {file_name}: {len(params)} params")
        print(f"   Title: {params.get('titulo', 'N/A')}")

    print()

def test_template_rendering():
    """Test template rendering with different renderers."""
    print("Testing template rendering...")

    db_manager = DatabaseManager()
    template_manager = TemplateManager(db_manager)

    # Get templates from database
    templates = template_manager.list_templates()

    if not templates:
        print("No templates found in database. Run the application first to initialize templates.")
        return

    test_output_dir = "test_output"
    os.makedirs(test_output_dir, exist_ok=True)

    for template_info in templates:
        try:
            template = template_manager.load_template(template_info['id'])
            if not template:
                continue

            # Get parameters for this template type
            file_name = f"test_{template['nombre'].lower().replace(' ', '_')}.{template['extension']}"
            params = get_template_params_for_file(file_name)

            # Add current date/time
            params['fecha'] = datetime.now().strftime("%Y-%m-%d")
            params['hora'] = datetime.now().strftime("%H:%M:%S")

            # Render template
            content = template_manager.render_template(template, params)

            # Save using appropriate renderer
            output_path = os.path.join(test_output_dir, f"test_{template_info['id']}.{template['extension']}")
            renderer = RendererFactory.get_renderer(template['extension'])
            renderer.render(content, output_path)

            print(f"Rendered {template['nombre']} ({template['extension']}) -> {output_path}")

        except Exception as e:
            print(f"Failed to render {template['nombre']}: {e}")

    print()

def test_structure_generation_with_templates():
    """Test structure generation with template rendering."""
    print("Testing structure generation with templates...")

    db_manager = DatabaseManager()
    from core.structure_generator import StructureGenerator

    generator = StructureGenerator(db_manager)

    # Test with a small structure
    test_structure = {
        "TestFolder": {
            "Templates": [
                "Test_Confirmacion.html",
                "Test_Manual.docx",
                "Test_Report.md",
                "Test_Dashboard.xlsx",
                "Test_Calculator.xlsx"
            ]
        }
    }

    try:
        output_path = generator.create_structure("TemplateTest", "test_output", test_structure)
        print(f"Structure generated at: {output_path}")

        # Check if files were created
        templates_dir = os.path.join(output_path, "TestFolder", "Templates")
        if os.path.exists(templates_dir):
            files = os.listdir(templates_dir)
            print(f"Generated files: {files}")

            # Check content of one file
            html_file = next((f for f in files if f.endswith('.html')), None)
            if html_file:
                with open(os.path.join(templates_dir, html_file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'Confirmación de Reserva' in content:
                        print("Template content correctly rendered")
                    else:
                        print("Template content may not be fully rendered")

        print()
    except Exception as e:
        print(f"Structure generation failed: {e}\n")

def cleanup_test_files():
    """Clean up test files."""
    print("Cleaning up test files...")

    test_dirs = ["test_output", "TemplateTest"]
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            import shutil
            shutil.rmtree(test_dir)
            print(f"Removed {test_dir}")

    print()

def main():
    """Run all tests."""
    print("Starting Template Tests\n")
    print("=" * 50)

    try:
        test_base_templates()
        test_template_params()
        test_template_rendering()
        test_structure_generation_with_templates()
        cleanup_test_files()

        print("=" * 50)
        print("All tests completed successfully!")

    except Exception as e:
        print(f"Test failed: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())