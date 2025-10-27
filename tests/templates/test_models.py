import unittest
from unittest.mock import Mock
from src.core.database import DatabaseManager
from src.templates.models import TemplateManager, TemplateNotFoundError, InvalidPlaceholderError

class TestTemplateManager(unittest.TestCase):
    def setUp(self):
        self.db_manager = Mock(spec=DatabaseManager)
        self.tm = TemplateManager(self.db_manager)

    def test_load_template_without_parent(self):
        self.db_manager.get_template.return_value = {
            'id': 1, 'nombre': 'Test', 'contenido': 'Hello {{name}}', 'padre_id': None, 'extension': 'txt'
        }
        template = self.tm.load_template(1)
        self.assertEqual(template['nombre'], 'Test')
        self.assertEqual(template['contenido'], 'Hello {{name}}')

    def test_load_template_with_parent(self):
        self.db_manager.get_template.side_effect = [
            {'id': 2, 'nombre': 'Parent', 'contenido': 'Base {{name}}', 'padre_id': None, 'extension': 'txt'},
            {'id': 1, 'nombre': 'Child', 'contenido': 'Child content', 'padre_id': 2, 'extension': 'txt'}
        ]
        template = self.tm.load_template(1)
        self.assertEqual(template['nombre'], 'Child')
        self.assertEqual(template['contenido'], 'Child content')

    def test_render_template_success(self):
        template = {'contenido': 'Hello {{name}}, welcome to {{company}}'}
        params = {'name': 'John', 'company': 'Acme'}
        result = self.tm.render_template(template, params)
        self.assertEqual(result, 'Hello John, welcome to Acme')

    def test_render_template_missing_placeholder(self):
        template = {'contenido': 'Hello {{name}}'}
        params = {}
        with self.assertRaises(InvalidPlaceholderError):
            self.tm.render_template(template, params)

if __name__ == '__main__':
    unittest.main()