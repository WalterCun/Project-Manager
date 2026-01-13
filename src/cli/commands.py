import argparse
import os
from ..core.structure_generator import StructureGenerator
# from ..core.database import DatabaseManager  # Comentado para desactivar DB
# from ..templates.cli import setup_template_parser # Comentado para desactivar DB

def create_project(args: argparse.Namespace) -> None:
    """
    Handles the core logic of creating a project structure.
    This version is simplified to work without a database.
    """
    # --- DB-related logic is fully disabled ---
    # The generator is instantiated without a database manager.
    generator = StructureGenerator(db_manager=None, doc_format=args.format)

    # Path conflict check (this is independent of the database)
    target_path = os.path.join(args.path, args.name)
    if os.path.exists(target_path) and os.listdir(target_path):
        if not args.force:
            print(f"Warning: Directory '{target_path}' already exists and is not empty.")
            print("Use --force to proceed and potentially overwrite files.")
            return
        else:
            print(f"Warning: Directory '{target_path}' is not empty. Proceeding with --force.")

    # Create the project structure using the non-DB method
    try:
        print(f"Creating project '{args.name}' (no-db mode)...")
        path = generator.create_structure(args.name, args.path)
        print(f"Project '{args.name}' created successfully at: {path}")
    except Exception as e:
        print(f"Error creating project: {e}")


# --- All DB-dependent functions are commented out ---

# def list_projects(args: argparse.Namespace) -> None:
#     db_manager = DatabaseManager()
#     projects = db_manager.list_projects()
#     if not projects:
#         print("No projects found.")
#     else:
#         for proj in projects:
#             print(f"ID: {proj['id']}, Name: {proj['name']}, Updated: {proj['updated_at']}")

# def generate_structure(args: argparse.Namespace) -> None:
#     db_manager = DatabaseManager()
#     generator = StructureGenerator(db_manager, doc_format=args.format)
#     project = db_manager.get_project(args.id)
#     if not project:
#         print(f"Project with ID {args.id} not found.")
#         return
#     path = generator.create_structure(project['name'], args.path, project['structure'])
#     print(f"Structure generated at: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Project Structure Manager CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands', required=True)

    # Create the project command (only command available in no-db mode)
    create_parser = subparsers.add_parser('create-project', help='Create a new project')
    create_parser.add_argument('name', help='Name of the project')
    create_parser.add_argument('--path', default='.', help='Path to generate the project structure')
    create_parser.add_argument('--format', choices=['md', 'pdf', 'img'], default='pdf', help='Format for documentation files (default: pdf)')
    create_parser.add_argument('--force', action='store_true', help='Force overwrite if target directory is not empty')
    create_parser.set_defaults(func=create_project)

    # --- DB-dependent commands are commented out from the parser ---
    # list_parser = subparsers.add_parser('list-projects', help='List all projects')
    # list_parser.set_defaults(func=list_projects)

    # gen_parser = subparsers.add_parser('generate-structure', help='Generate folder structure for a project')
    # gen_parser.add_argument('id', type=int, help='Project ID')
    # gen_parser.add_argument('path', help='Base path to generate structure')
    # gen_parser.add_argument('--format', choices=['md', 'pdf', 'img'], default='pdf', help='Format for documentation files (default: pdf)')
    # gen_parser.set_defaults(func=generate_structure)
    
    # setup_template_parser(subparsers)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        try:
            args.func(args)
            return 0
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return 1
    else:
        parser.print_help()
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
