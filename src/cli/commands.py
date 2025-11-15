import argparse
import json
import os
from ..core.structure_generator import StructureGenerator
from ..core.database import DatabaseManager
from ..templates.cli import setup_template_parser

def create_project(args: argparse.Namespace) -> None:
    db_manager = DatabaseManager()
    # Pass the format argument to the generator
    generator = StructureGenerator(db_manager, doc_format=args.format)

    # Determine action based on arguments
    action = None
    if hasattr(args, 'regenerate') and args.regenerate:
        action = 'regenerate'
    elif hasattr(args, 'restart') and args.restart:
        action = 'restart'

    # Get structure name if provided
    structure_name = getattr(args, 'structure', None)

    # Check if the project already exists
    if generator.check_duplicate_name(args.name):
        existing_project = db_manager.get_project_by_name(args.name)
 
        # If non-interactive mode with a specific action
        if action:
            if action == 'regenerate':
                print(f"Regenerating project '{args.name}'...")
                try:
                    path = generator.regenerate_structure(args.name, args.path)
                    print(f"Project '{args.name}' regenerated at: {path}")
                    return
                except Exception as e:
                    print(f"Error regenerating project: {e}")
                    return
            elif action == 'restart':
                print(f"Restarting project '{args.name}' with default structure...")
                try:
                    path = generator.restart_structure(args.name, args.path)
                    print(f"Project '{args.name}' restarted at: {path}")
                    return
                except Exception as e:
                    print(f"Error restarting project: {e}")
                    return
 
        # If --force is specified, skip interactive menu and regenerate
        if hasattr(args, 'force') and args.force:
            print(f"Regenerating project '{args.name}' with --force...")
            try:
                path = generator.regenerate_structure(args.name, args.path)
                print(f"Project '{args.name}' regenerated at: {path}")
                return
            except Exception as e:
                print(f"Error regenerating project: {e}")
                return
 
        # Interactive mode
        print(f"Project '{args.name}' already exists in the database.")
        if existing_project and existing_project['path']:
            print(f"Current path: {existing_project['path']}")
 
        print("\nWhat would you like to do?")
        print("1. Regenerate existing structure (keep current structure, recreate files)")
        print("2. Restart with default structure (replace with new default structure)")
        print("3. Cancel")
 
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
 
            if choice == '1':
                print(f"Regenerating project '{args.name}'...")
                try:
                    path = generator.regenerate_structure(args.name, args.path)
                    print(f"Project '{args.name}' regenerated at: {path}")
                except Exception as e:
                    print(f"Error regenerating project: {e}")
            elif choice == '2':
                print(f"Restarting project '{args.name}' with default structure...")
                try:
                    path = generator.restart_structure(args.name, args.path)
                    print(f"Project '{args.name}' restarted at: {path}")
                except Exception as e:
                    print(f"Error restarting project: {e}")
            else:
                print("Operation cancelled.")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled (non-interactive environment detected).")
        return

    # Check for path conflicts for new projects
    conflict = generator.check_path_conflict(args.name, args.path)
    if conflict == "path_exists_with_files":
        print(f"Warning: Directory '{os.path.join(args.path, args.name)}' already exists and contains files.")
        print("This may overwrite existing files.")
 
        if not hasattr(args, 'force') or not args.force:
            print("Use --force to override this check in non-interactive mode.")
            print("Operation cancelled.")
            return
 
        print("Continuing with --force flag...")
    elif conflict == "path_exists_empty":
        print(f"Directory '{os.path.join(args.path, args.name)}' already exists but is empty. Proceeding without --force.")

    # Create new project
    try:
        path = generator.create_structure_and_save(args.name, args.path, structure_name=structure_name)
        print(f"Project '{args.name}' created and structure generated at: {path}")
    except Exception as e:
        print(f"Error creating project: {e}")

def list_projects(args: argparse.Namespace) -> None:
    db_manager = DatabaseManager()
    projects = db_manager.list_projects()
    if not projects:
        print("No projects found.")
    else:
        for proj in projects:
            print(f"ID: {proj['id']}, Name: {proj['name']}, Updated: {proj['updated_at']}")

def generate_structure(args: argparse.Namespace) -> None:
    db_manager = DatabaseManager()
    generator = StructureGenerator(db_manager, doc_format=args.format)
    project = generator.load_from_db(args.id)
    if not project:
        print(f"Project with ID {args.id} not found.")
        return
    path = generator.create_structure(project['name'], args.path, project['structure'])
    print(f"Structure generated at: {path}")

def export_json(args: argparse.Namespace) -> None:
    db_manager = DatabaseManager()
    generator = StructureGenerator(db_manager)
    project = generator.load_from_db(args.id)
    if not project:
        print(f"Project with ID {args.id} not found.")
        return
    with open(args.file, 'w', encoding='utf-8') as f:
        json.dump(project['structure'], f, indent=4)
    print(f"Structure exported to {args.file}")

def import_json(args: argparse.Namespace) -> None:
    db_manager = DatabaseManager()
    generator = StructureGenerator(db_manager)
    if generator.check_duplicate_name(args.name):
        print(f"Project with name '{args.name}' already exists.")
        return
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            structure = json.load(f)
        project_id = generator.save_to_db(args.name, structure)
        print(f"Structure imported as project '{args.name}' with ID: {project_id}")
    except FileNotFoundError:
        print(f"File {args.file} not found.")
    except json.JSONDecodeError:
        print(f"Invalid JSON in {args.file}.")

def scan_directory(args: argparse.Namespace) -> None:
    db_manager = DatabaseManager()
    generator = StructureGenerator(db_manager)
    if generator.check_duplicate_name(args.name):
        print(f"Project with name '{args.name}' already exists.")
        return
    try:
        project_id = generator.save_scanned_structure(args.name, args.path)
        print(f"Directory scanned and saved as project '{args.name}' with ID: {project_id}")
    except RuntimeError as e:
        print(f"Error: {e}")

def main() -> int:
    parser = argparse.ArgumentParser(description="Project Structure Manager CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create the project
    create_parser = subparsers.add_parser('create-project', help='Create a new project')
    create_parser.add_argument('name', help='Name of the project')
    create_parser.add_argument('--path', default='.', help='Path to generate the project structure (default: current directory)')
    create_parser.add_argument('--structure', help='Name of structure template to use (from templates/structures/)')
    create_parser.add_argument('--format', choices=['md', 'pdf'], default='pdf', help='Format for documentation files (INFO, STRUCTURE). Default: pdf')
    create_parser.add_argument('--regenerate', action='store_true', help='Regenerate existing project structure (non-interactive)')
    create_parser.add_argument('--restart', action='store_true', help='Restart project with default structure (non-interactive)')
    create_parser.add_argument('--force', action='store_true', help='Force overwrite existing directories (non-interactive)')
    create_parser.set_defaults(func=create_project)

    # List projects
    list_parser = subparsers.add_parser('list-projects', help='List all projects')
    list_parser.set_defaults(func=list_projects)

    # Generate structure
    gen_parser = subparsers.add_parser('generate-structure', help='Generate folder structure for a project')
    gen_parser.add_argument('id', type=int, help='Project ID')
    gen_parser.add_argument('path', help='Base path to generate structure')
    gen_parser.add_argument('--format', choices=['md', 'pdf'], default='pdf', help='Format for documentation files. Default: pdf')
    gen_parser.set_defaults(func=generate_structure)

    # Export JSON
    export_parser = subparsers.add_parser('export-json', help='Export project structure to JSON')
    export_parser.add_argument('id', type=int, help='Project ID')
    export_parser.add_argument('file', help='Output JSON file')
    export_parser.set_defaults(func=export_json)

    # Import JSON
    import_parser = subparsers.add_parser('import-json', help='Import project structure from JSON file')
    import_parser.add_argument('name', help='Name of the project')
    import_parser.add_argument('file', help='Input JSON file')
    import_parser.set_defaults(func=import_json)

    # Scan directory
    scan_parser = subparsers.add_parser('scan-directory', help='Scan a directory and save structure to database')
    scan_parser.add_argument('name', help='Name of the project')
    scan_parser.add_argument('path', help='Path to the directory to scan')
    scan_parser.set_defaults(func=scan_directory)

    # Setup template commands
    setup_template_parser(subparsers)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        try:
            args.func(args)
            return 0
        except Exception as e:
            if str(e):
                print(f"Error: {e}")
            return 1
    else:
        parser.print_help()
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
