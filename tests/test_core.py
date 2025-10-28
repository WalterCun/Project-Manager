import pytest
import os
import json
from unittest.mock import patch, MagicMock
from src.core.database import DatabaseManager
from src.core.structure_generator import StructureGenerator
from src.templates.models import TemplateManager

class TestDatabaseManager:
    def test_save_project(self, test_db, sample_structure):
        project_id = test_db.save_project("Test Project", sample_structure)
        assert project_id > 0

        project = test_db.get_project(project_id)
        assert project['name'] == "Test Project"
        assert project['structure'] == sample_structure

    def test_get_project_by_name(self, test_db, sample_structure):
        test_db.save_project("Test Project", sample_structure)
        project = test_db.get_project_by_name("Test Project")
        assert project['name'] == "Test Project"

        non_existent = test_db.get_project_by_name("Non Existent")
        assert non_existent is None

    def test_check_duplicate_name(self, test_db, sample_structure):
        assert not test_db.check_duplicate_name("Test Project")
        test_db.save_project("Test Project", sample_structure)
        assert test_db.check_duplicate_name("Test Project")

    def test_check_path_conflict(self, test_db, sample_structure):
        # Test no conflict
        conflict = test_db.check_project_path_conflict("Test Project", ".")
        assert conflict is None

        # Test with existing project
        test_db.save_project("Test Project", sample_structure, ".")
        conflict = test_db.check_project_path_conflict("Test Project", ".")
        assert conflict == "same_path"

    def test_list_projects(self, test_db, sample_structure):
        projects = test_db.list_projects()
        assert len(projects) == 0

        test_db.save_project("Project1", sample_structure)
        test_db.save_project("Project2", sample_structure)
        projects = test_db.list_projects()
        assert len(projects) == 2

class TestStructureGenerator:
    def test_create_structure(self, generator, temp_dir, sample_structure):
        path = generator.create_structure("Test Project", temp_dir, sample_structure)
        expected_path = os.path.join(temp_dir, "Test Project")
        assert path == expected_path
        assert os.path.exists(expected_path)

        # Check if folders are created
        assert os.path.exists(os.path.join(expected_path, "folder1"))
        assert os.path.exists(os.path.join(expected_path, "folder1", "subfolder"))

    def test_check_duplicate_name(self, generator, sample_structure):
        assert not generator.check_duplicate_name("Test Project")
        generator.save_to_db("Test Project", sample_structure)
        assert generator.check_duplicate_name("Test Project")

    def test_regenerate_structure(self, generator, temp_dir, sample_structure):
        # First create
        generator.save_to_db("Test Project", sample_structure)
        path = generator.regenerate_structure("Test Project", temp_dir)
        assert os.path.exists(path)

    def test_restart_structure(self, generator, temp_dir, sample_structure):
        # First create
        generator.save_to_db("Test Project", sample_structure)
        path = generator.restart_structure("Test Project", temp_dir)
        assert os.path.exists(path)

class TestTemplateManager:
    def test_save_template(self, template_manager, sample_template):
        template_id = template_manager.save_template(
            sample_template['nombre'],
            sample_template['contenido'],
            sample_template['extension']
        )
        assert template_id > 0

    def test_load_template(self, template_manager, sample_template):
        template_id = template_manager.save_template(
            sample_template['nombre'],
            sample_template['contenido'],
            sample_template['extension']
        )
        loaded = template_manager.load_template(template_id)
        assert loaded['nombre'] == sample_template['nombre']

    def test_render_template(self, template_manager, sample_template):
        template_id = template_manager.save_template(
            sample_template['nombre'],
            sample_template['contenido'],
            sample_template['extension']
        )
        rendered = template_manager.render_template(
            template_manager.load_template(template_id),
            {'name': 'World'}
        )
        assert rendered == "Hello World"

    def test_list_templates(self, template_manager, sample_template):
        templates = template_manager.list_templates()
        assert len(templates) == 0

        template_manager.save_template(
            sample_template['nombre'],
            sample_template['contenido'],
            sample_template['extension']
        )
        templates = template_manager.list_templates()
        assert len(templates) == 1