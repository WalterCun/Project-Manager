import pytest
import tempfile
import shutil
import os
from src.core.database import DatabaseManager
from src.core.structure_generator import StructureGenerator
from src.templates.models import TemplateManager

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)

@pytest.fixture
def test_db():
    """Create a temporary database for testing."""
    db_path = tempfile.mktemp(suffix='.db')
    db_manager = DatabaseManager(db_path)
    yield db_manager
    os.remove(db_path)

@pytest.fixture
def sample_structure():
    """Sample project structure for testing."""
    return {
        "folder1": {
            "subfolder": {},
            "file1.txt": "content1"
        },
        "folder2": {
            "file2.txt": "content2"
        }
    }

@pytest.fixture
def generator(test_db):
    """Structure generator with test database."""
    return StructureGenerator(test_db)

@pytest.fixture
def template_manager(test_db):
    """Template manager with test database."""
    return TemplateManager(test_db)

@pytest.fixture
def sample_template():
    """Sample template for testing."""
    return {
        "nombre": "Test Template",
        "contenido": "Hello {{name}}",
        "extension": "txt"
    }