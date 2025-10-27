import argparse
import json
import os
from typing import Dict, Any
from ..core.structure_generator import StructureGenerator
from ..core.database import DatabaseManager

def create_project(args: argparse.Namespace) -> None:
    db_manager = DatabaseManager()
    generator = StructureGenerator(db_manager)
    project_id = generator.save_to_db(args.name, generator.default_structure)
    path = generator.create_structure(args.name, args.path, generator.default_structure)
    print(f"Project '{args.name}' created with ID: {project_id} and structure generated at: {path}")

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
    generator = StructureGenerator(db_manager)
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
    with open(args.file, 'w') as f:
        json.dump(project['structure'], f, indent=4)
    print(f"Structure exported to {args.file}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Project Structure Manager CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create project
    create_parser = subparsers.add_parser('create-project', help='Create a new project')
    create_parser.add_argument('name', help='Name of the project')
    create_parser.add_argument('--path', default='.', help='Path to generate the project structure (default: current directory)')
    create_parser.set_defaults(func=create_project)

    # List projects
    list_parser = subparsers.add_parser('list-projects', help='List all projects')
    list_parser.set_defaults(func=list_projects)

    # Generate structure
    gen_parser = subparsers.add_parser('generate-structure', help='Generate folder structure for a project')
    gen_parser.add_argument('id', type=int, help='Project ID')
    gen_parser.add_argument('path', help='Base path to generate structure')
    gen_parser.set_defaults(func=generate_structure)

    # Export JSON
    export_parser = subparsers.add_parser('export-json', help='Export project structure to JSON')
    export_parser.add_argument('id', type=int, help='Project ID')
    export_parser.add_argument('file', help='Output JSON file')
    export_parser.set_defaults(func=export_json)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()