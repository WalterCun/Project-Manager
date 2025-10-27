# Project Structure Manager

A CLI tool for generating standardized business project folder structures. This tool helps create organized directory layouts for business projects, with support for database management, structure generation, and export functionality.

## Features

- **Create Projects**: Define and save custom project structures to a SQLite database.
- **Generate Structures**: Automatically create folder hierarchies based on saved projects.
- **List Projects**: View all saved projects with their details.
- **Export Structures**: Export project structures to JSON files for sharing or backup.
- **Default Structure**: Includes a comprehensive default structure for business projects, covering administrative, strategic, legal, operational, and other key areas.
- **Dynamic Templates**: Create, manage, and render dynamic templates with inheritance support for multiple file formats (DOCX, XLSX, HTML, MD, TXT).
- **Template Inheritance**: Templates can inherit from parent templates, allowing for reusable and customizable content.
- **Multi-Format Rendering**: Generate files in various formats with dynamic placeholder replacement.

## Installation

### Prerequisites

- Python 3.12 or higher
- Required dependencies: `openpyxl`, `pyinstaller`, `python-docx`, `sqlalchemy`

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd base-de-proyecto
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Run the CLI:
   ```bash
   project-manager --help
   ```

## Usage

The tool is accessed via the `project-manager` command (or `python __main__.py` directly).

### Available Commands

#### Create a New Project
```bash
project-manager create-project "My Project Name"
```
Creates a new project with the default structure and saves it to the database.

#### List All Projects
```bash
project-manager list-projects
```
Displays all saved projects with their IDs, names, and last updated timestamps.

#### Generate Folder Structure
```bash
project-manager generate-structure <project-id> <output-path>
```
Generates the folder structure for the specified project ID at the given output path.

Example:
```bash
project-manager generate-structure 1 ./my-business-project
```

#### Export Structure to JSON
```bash
project-manager export-json <project-id> <output-file>
```
Exports the project structure to a JSON file.

Example:
```bash
project-manager export-json 1 project-structure.json
```

#### Import Structure from JSON
```bash
project-manager import-json <project-name> <input-file>
```
Imports a project structure from a JSON file and saves it to the database.

Example:
```bash
project-manager import-json "My Imported Project" project-structure.json
```

#### Scan Directory and Save
```bash
project-manager scan-directory <project-name> <directory-path>
```
Scans an existing directory structure and saves it to the database.

Example:
```bash
project-manager scan-directory "Scanned Project" ./existing-project
```

### Template Management

The tool now supports dynamic templates with inheritance and multi-format rendering.

#### Create a Template
```bash
project-manager template crear "Contract Template" --extension docx --contenido "This is a contract for {{client}} from {{company}}."
```
Creates a new template with placeholders.

#### Create a Template with Inheritance
```bash
project-manager template heredar "Specific Contract" --padre 1 --extension docx
```
Creates a child template inheriting from template ID 1.

#### Render a Template
```bash
project-manager template render 1 --output ./contract.docx client "John Doe" company "Acme Corp"
```
Renders the template with provided parameters and generates the file.

#### List Templates
```bash
project-manager template listar
```
Lists all templates.

#### Modify a Template
```bash
project-manager template modificar 1 --contenido "Updated content with {{new_placeholder}}."
```
Updates the content of template ID 1.

#### Delete a Template
```bash
project-manager template eliminar 1
```
Deletes template ID 1.

### Default Project Structure

The tool includes a comprehensive default structure organized into the following main categories:

- **00_ADMINISTRATIVO**: General project information, legal data, contracts, intellectual property, official correspondence.
- **01_ESTRATÉGICO**: Vision, mission, business model, market analysis, strategic roadmap, objectives, financial projections.
- **02_LEGAL_Y_CONSTITUCIÓN**: RUC, permits, insurance, partner agreements, client terms, supplier contracts.
- **03_OPERACIONES**: Manuals, processes, protocols, supplier control, quality standards, operational calendars.
- **04_COMERCIAL_Y_VENTAS**: Sales manuals, scripts, objection responses, pricing policies, promotions, cost calculators.
- **05_MARKETING_Y_CONTENIDO**: Marketing plans, editorial calendars, brand guidelines, content banks, strategies.
- **06_CLIENTES_Y_USUARIOS**: CRM, communication templates, client contracts, feedback forms, loyalty programs.
- **07_FINANZAS_Y_CONTABILIDAD**: Initial balance, annual budgets, expense control, cash flow, financial reports.
- **08_RECURSOS_HUMANOS_Y_EQUIPO**: Organizational chart, roles, job descriptions, KPIs, culture manuals.
- **09_CAPACITACIÓN_Y_DOCUMENTACIÓN_INTERNA**: Induction manuals, operational guides, technical training, videos.
- **10_ANALÍTICA_Y_REPORTES**: Dashboards, periodic reports, lessons learned, performance indicators.

## Project Structure

```
base-de-proyecto/
├── __main__.py              # CLI entry point
├── pyproject.toml           # Project configuration and dependencies
├── project_structure.db     # SQLite database for projects and templates (created on first run)
├── README.md                # This file
├── tests/
│   └── templates/
│       └── test_models.py   # Unit tests for template functionality
├── src/
│   ├── cli/
│   │   ├── __init__.py
│   │   └── commands.py      # CLI command implementations
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py      # Database management (SQLAlchemy models and operations)
│   │   └── structure_generator.py  # Structure generation logic
│   └── templates/
│       ├── __init__.py
│       ├── models.py        # Template management and inheritance logic
│       ├── renderers.py     # File format renderers (DOCX, XLSX, HTML, MD, TXT)
│       └── cli.py           # Template-specific CLI commands
```

## Development

### Running Locally

1. Ensure Python 3.12+ is installed.
2. Activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install in development mode:
   ```bash
   pip install -e .
   ```
4. Run the CLI:
   ```bash
   python __main__.py create-project "Test Project"
   ```

### Database

The tool uses SQLite (`project_structure.db`) for persistence. The database is created automatically on first run. It includes tables for projects, templates, and change history.

- **Projects Table**: Stores project structures and metadata.
- **Templates Table**: Stores dynamic templates with inheritance support.
- **Changes Table**: Logs all modifications for audit purposes.

### Adding New Features

1. **CLI Commands**: Add new commands in `src/cli/commands.py` by defining functions and adding them to the argument parser in the `main()` function.
2. **Core Logic**: Extend `src/core/structure_generator.py` for new structure generation features.
3. **Database Models**: Modify `src/core/database.py` to add new tables or fields as needed.

### Testing

Run tests (if implemented):
```bash
python -m pytest
```

### Building Executable

To create a standalone executable using PyInstaller:
```bash
pyinstaller --onefile __main__.py
```

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/new-feature`.
3. Commit changes: `git commit -am 'Add new feature'`.
4. Push to the branch: `git push origin feature/new-feature`.
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For issues or questions, please open an issue on the GitHub repository.