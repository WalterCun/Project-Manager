import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.database import DatabaseManager
from .models import TemplateManager, TemplateNotFoundError, InvalidPlaceholderError
from .renderers import RendererFactory

def create_template(args: argparse.Namespace) -> None:
    db_manager = DatabaseManager()
    tm = TemplateManager(db_manager)
    template_id = tm.save_template(args.nombre, args.contenido, args.extension, args.padre, args.project)
    print(f"Template '{args.nombre}' created with ID: {template_id}")

def modify_template(args: argparse.Namespace) -> None:
    db_manager = DatabaseManager()
    tm = TemplateManager(db_manager)
    tm.update_template(args.id, nombre=args.nombre, contenido=args.contenido, extension=args.extension, padre_id=args.padre, project_id=args.project)
    print(f"Template {args.id} updated.")

def inherit_template(args: argparse.Namespace) -> None:
    db_manager = DatabaseManager()
    tm = TemplateManager(db_manager)
    # Load parent content
    parent = tm.load_template(args.padre)
    template_id = tm.save_template(args.nombre, parent['contenido'], args.extension, args.padre, args.project)
    print(f"Template '{args.nombre}' inherited from ID {args.padre} with new ID: {template_id}")

def render_template(args: argparse.Namespace) -> None:
    db_manager = DatabaseManager()
    tm = TemplateManager(db_manager)
    try:
        template = tm.load_template(args.id)
        params = dict(zip(args.params[::2], args.params[1::2]))
        rendered_content = tm.render_template(template, params)

        # Generate file
        output_path = args.output or f"{args.id}.{template['extension']}"
        renderer = RendererFactory.get_renderer(template['extension'])
        renderer.render(rendered_content, output_path)

        print(f"Template rendered and saved to: {output_path}")
    except (TemplateNotFoundError, InvalidPlaceholderError) as e:
        print(f"Error: {e}")

def list_templates(args: argparse.Namespace) -> None:
    db_manager = DatabaseManager()
    tm = TemplateManager(db_manager)
    templates = tm.list_templates(args.project)
    if not templates:
        print("No templates found.")
    else:
        for t in templates:
            print(f"ID: {t['id']}, Name: {t['nombre']}, Extension: {t['extension']}, Updated: {t['updated_at']}")

def delete_template(args: argparse.Namespace) -> None:
    db_manager = DatabaseManager()
    tm = TemplateManager(db_manager)
    tm.delete_template(args.id)
    print(f"Template {args.id} deleted.")

def setup_template_parser(subparsers: argparse._SubParsersAction) -> None:
    """Set up template subcommands."""
    template_parser = subparsers.add_parser('template', help='Manage templates')
    template_subparsers = template_parser.add_subparsers(dest='template_command', help='Template commands')

    # Create template
    create_parser = template_subparsers.add_parser('crear', help='Create a new template')
    create_parser.add_argument('nombre', help='Template name')
    create_parser.add_argument('--extension', required=True, help='File extension (e.g., docx, xlsx)')
    create_parser.add_argument('--contenido', default='', help='Template content with placeholders')
    create_parser.add_argument('--padre', type=int, help='Parent template ID for inheritance')
    create_parser.add_argument('--project', type=int, help='Associated project ID')
    create_parser.set_defaults(func=create_template)

    # Modify template
    modify_parser = template_subparsers.add_parser('modificar', help='Modify an existing template')
    modify_parser.add_argument('id', type=int, help='Template ID')
    modify_parser.add_argument('--nombre', help='New name')
    modify_parser.add_argument('--contenido', help='New content')
    modify_parser.add_argument('--extension', help='New extension')
    modify_parser.add_argument('--padre', type=int, help='New parent ID')
    modify_parser.add_argument('--project', type=int, help='New project ID')
    modify_parser.set_defaults(func=modify_template)

    # Inherit template
    inherit_parser = template_subparsers.add_parser('heredar', help='Create a template inheriting from another')
    inherit_parser.add_argument('nombre', help='New template name')
    inherit_parser.add_argument('--padre', type=int, required=True, help='Parent template ID')
    inherit_parser.add_argument('--extension', required=True, help='File extension')
    inherit_parser.add_argument('--project', type=int, help='Associated project ID')
    inherit_parser.set_defaults(func=inherit_template)

    # Render template
    render_parser = template_subparsers.add_parser('render', help='Render and generate file from template')
    render_parser.add_argument('id', type=int, help='Template ID')
    render_parser.add_argument('--output', help='Output file path')
    render_parser.add_argument('params', nargs='*', help='Key-value pairs for placeholders (e.g., nombre Juan empresa Acme)')
    render_parser.set_defaults(func=render_template)

    # List templates
    list_parser = template_subparsers.add_parser('listar', help='List all templates')
    list_parser.add_argument('--project', type=int, help='Filter by project ID')
    list_parser.set_defaults(func=list_templates)

    # Delete template
    delete_parser = template_subparsers.add_parser('eliminar', help='Delete a template')
    delete_parser.add_argument('id', type=int, help='Template ID')
    delete_parser.set_defaults(func=delete_template)