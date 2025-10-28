import subprocess
import os
import json
from pathlib import Path

class TestCLICommands:
    def run_command(self, cmd, cwd=None):
        """Run a CLI command and return the result."""
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode, result.stdout, result.stderr

    def test_create_project_new(self, temp_dir):
        """Test creating a new project."""
        cmd = f"python -m src.cli.commands create-project TestProject --path {temp_dir}"
        returncode, stdout, stderr = self.run_command(cmd)
        assert returncode == 0
        assert "TestProject" in stdout or "created" in stdout.lower()

        # Check if the directory was created
        project_path = Path(temp_dir) / "TestProject"
        assert project_path.exists()

    def test_create_project_duplicate(self, temp_dir):
        """Test creating a project with a duplicate name."""
        # Create the first project
        cmd1 = f"python -m src.cli.commands create-project TestProject --path {temp_dir}"
        self.run_command(cmd1)

        # Try to create again without --force (should cancel in non-interactive)
        cmd2 = f"python -m src.cli.commands create-project TestProject --path {temp_dir}"
        returncode, stdout, stderr = self.run_command(cmd2)
        assert returncode == 0  # Should not error, but cancel
        assert "cancelled" in stdout.lower() or "already exists" in stdout.lower()

        # Try with --force
        cmd3 = f"python -m src.cli.commands create-project TestProject --path {temp_dir} --force"
        returncode, stdout, stderr = self.run_command(cmd3)
        assert returncode == 0
        assert "regenerated" in stdout.lower()

    def test_list_projects(self):
        """Test listing projects."""
        cmd = "python -m src.cli.commands list-projects"
        returncode, stdout, stderr = self.run_command(cmd)
        assert returncode == 0
        # Should list projects or say no projects

    def test_generate_structure(self, temp_dir):
        """Test generating structure for existing project."""
        # First create a project
        cmd1 = f"python -m src.cli.commands create-project TestProject --path {temp_dir}"
        self.run_command(cmd1)

        # Get project ID (assuming it's 1 for simplicity, or parse from output)
        # For now, assume ID 1
        cmd2 = f"python -m src.cli.commands generate-structure 1 {temp_dir}/generated"
        returncode, stdout, stderr = self.run_command(cmd2)
        assert returncode == 0

    def test_export_json(self, temp_dir):
        """Test exporting project to JSON."""
        # Create a project
        cmd1 = f"python -m src.cli.commands create-project TestProject --path {temp_dir}"
        self.run_command(cmd1)

        # Export
        export_file = f"{temp_dir}/export.json"
        cmd2 = f"python -m src.cli.commands export-json 1 {export_file}"
        returncode, stdout, stderr = self.run_command(cmd2)
        assert returncode == 0
        assert os.path.exists(export_file)

        # Check content
        with open(export_file) as f:
            data = json.load(f)
            assert "00_ADMINISTRATIVO" in data

    def test_import_json(self, temp_dir):
        """Test importing project from JSON."""
        # Create export file
        export_file = f"{temp_dir}/export.json"
        sample_structure = {"folder": {"file.txt": "content"}}
        with open(export_file, 'w') as f:
            json.dump(sample_structure, f)

        # Import
        cmd = f"python -m src.cli.commands import-json ImportedProject {export_file}"
        returncode, stdout, stderr = self.run_command(cmd)
        assert returncode == 0
        assert "imported" in stdout.lower()

    def test_scan_directory(self, temp_dir):
        """Test scanning a directory."""
        # Create a test directory structure
        test_scan_dir = f"{temp_dir}/scan_test"
        os.makedirs(f"{test_scan_dir}/subfolder")
        with open(f"{test_scan_dir}/file.txt", 'w') as f:
            f.write("test")

        cmd = f"python -m src.cli.commands scan-directory ScannedProject {test_scan_dir}"
        returncode, stdout, stderr = self.run_command(cmd)
        assert returncode == 0
        assert "scanned" in stdout.lower()

    def test_template_commands(self):
        """Test template creation and listing."""
        # Create template
        cmd1 = "python -m src.cli.commands template crear TestTemplate --extension txt --contenido 'Hello {{name}}'"
        returncode, stdout, stderr = self.run_command(cmd1)
        assert returncode == 0

        # List templates
        cmd2 = "python -m src.cli.commands template listar"
        returncode, stdout, stderr = self.run_command(cmd2)
        assert returncode == 0
        assert "TestTemplate" in stdout

        # Render template
        cmd3 = "python -m src.cli.commands template render 1 name World"
        returncode, stdout, stderr = self.run_command(cmd3)
        assert returncode == 0
        assert "Hello World" in stdout

    def test_invalid_commands(self):
        """Test invalid command parameters."""
        # Invalid project name
        cmd1 = "python -m src.cli.commands create-project ''"
        returncode, stdout, stderr = self.run_command(cmd1)
        assert returncode != 0

        # Invalid ID
        cmd2 = "python -m src.cli.commands generate-structure invalid_id /tmp"
        returncode, stdout, stderr = self.run_command(cmd2)
        assert returncode != 0

    def test_path_conflicts(self, temp_dir):
        """Test path conflict handling."""
        # Create directory with files
        conflict_dir = f"{temp_dir}/conflict"
        os.makedirs(conflict_dir)
        with open(f"{conflict_dir}/existing.txt", 'w') as f:
            f.write("existing")

        # Try to create project without --force
        cmd1 = f"python -m src.cli.commands create-project ConflictProject --path {temp_dir}"
        returncode, stdout, stderr = self.run_command(cmd1)
        assert returncode == 0
        assert "cancelled" in stdout.lower() or "overwrite" in stdout.lower()

        # With --force
        cmd2 = f"python -m src.cli.commands create-project ConflictProject --path {temp_dir} --force"
        returncode, stdout, stderr = self.run_command(cmd2)
        assert returncode == 0
        assert "created" in stdout.lower()