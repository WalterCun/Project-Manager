import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.database import DatabaseManager
from .models import TemplateManager, TemplateNotFoundError, InvalidPlaceholderError

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

        # Print rendered content for immediate feedback/testing
        print(rendered_content)

        # Optionally write to a file if output path specified
        output_path = args.output or f"{args.id}.{template['extension']}"
        try:
            # Write as text by default for DB templates
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(rendered_content)
            print(f"Template rendered and saved to: {output_path}")
        except OSError as file_err:
            print(f"Warning: Could not write output file: {file_err}")
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

def list_external_templates(args: argparse.Namespace) -> None:
    """List all external templates."""
    from ..core.external_templates import ExternalTemplateLoader
    loader = ExternalTemplateLoader()

    extension = getattr(args, 'extension', None)
    templates = loader.list_templates(extension)

    if not templates:
        print("No external templates found.")
    else:
        print(f"Found {len(templates)} external templates:")
        for template in templates:
            print(f"  - {template['name']} ({template['extension']})")
            if template['description']:
                print(f"    Description: {template['description']}")

def create_external_template(args: argparse.Namespace) -> None:
    """Create a new external template."""
    from ..core.external_templates import ExternalTemplateLoader

    template_data = {
        "name": args.name,
        "extension": args.extension,
        "description": getattr(args, 'description', ''),
        "content": getattr(args, 'content', ''),
        "version": getattr(args, 'version', '1.0'),
        "author": getattr(args, 'author', 'User')
    }

    loader = ExternalTemplateLoader()
    success = loader.save_template(template_data, args.extension)

    if success:
        print(f"External template '{args.name}' ({args.extension}) created successfully.")
    else:
        print(f"Failed to create template '{args.name}'.")

def delete_external_template(args: argparse.Namespace) -> None:
    """Delete an external template."""
    from ..core.external_templates import ExternalTemplateLoader

    loader = ExternalTemplateLoader()
    success = loader.delete_template(args.name, args.extension)

    if success:
        print(f"External template '{args.name}' ({args.extension}) deleted successfully.")
    else:
        print(f"Template '{args.name}' not found or could not be deleted.")

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

    # External templates
    external_parser = template_subparsers.add_parser('external', help='Manage external templates')
    external_subparsers = external_parser.add_subparsers(dest='external_command', help='External template commands')

    # List external templates
    list_ext_parser = external_subparsers.add_parser('listar', help='List external templates')
    list_ext_parser.add_argument('--extension', help='Filter by extension (html, xlsx, docx, md)')
    list_ext_parser.set_defaults(func=list_external_templates)

    # Create external template
    create_ext_parser = external_subparsers.add_parser('crear', help='Create external template')
    create_ext_parser.add_argument('name', help='Template name')
    create_ext_parser.add_argument('extension', help='File extension (html, xlsx, docx, md)')
    create_ext_parser.add_argument('--content', default='', help='Template content')
    create_ext_parser.add_argument('--description', default='', help='Template description')
    create_ext_parser.add_argument('--version', default='1.0', help='Template version')
    create_ext_parser.add_argument('--author', default='User', help='Template author')
    create_ext_parser.set_defaults(func=create_external_template)

    # Delete external template
    delete_ext_parser = external_subparsers.add_parser('eliminar-ext', help='Delete external template')
    delete_ext_parser.add_argument('name', help='Template name')
    delete_ext_parser.add_argument('extension', help='File extension')
    delete_ext_parser.set_defaults(func=delete_external_template)