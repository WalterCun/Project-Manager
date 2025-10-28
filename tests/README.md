# Tests

This directory contains comprehensive tests for the Project Structure Manager CLI.

## Structure

- `test_plan.md`: Detailed test plan with all commands and parameters
- `__init__.py`: Package initialization
- `conftest.py`: Pytest fixtures for testing
- `test_core.py`: Unit tests for core modules (database, structure_generator, templates)
- `test_cli.py`: Integration tests for CLI commands
- `test_edge_cases.py`: Tests for error handling and edge cases
- `test_data/`: Sample data files for testing (JSON structures, etc.)

## Running Tests

### Prerequisites
Install pytest and other testing dependencies:
```
pip install pytest pytest-mock
```

### Run All Tests
```
pytest
```

### Run Specific Test Files
```
pytest tests/test_core.py
pytest tests/test_cli.py
pytest tests/test_edge_cases.py
```

### Run with Coverage
```
pip install pytest-cov
pytest --cov=src --cov-report=html
```

### Run Specific Tests
```
pytest tests/test_cli.py::TestCLICommands::test_create_project_new -v
```

## Test Categories

### Unit Tests (test_core.py)
- Test individual functions in isolation
- Mock external dependencies
- Focus on business logic

### Integration Tests (test_cli.py)
- Test full command execution
- Verify file system changes
- Check database state

### Edge Case Tests (test_edge_cases.py)
- Error conditions
- Invalid inputs
- System limits

## Fixtures

- `temp_dir`: Temporary directory for file operations
- `test_db`: Temporary SQLite database
- `sample_structure`: Sample project structure
- `generator`: StructureGenerator instance
- `template_manager`: TemplateManager instance

## Adding New Tests

1. Add unit tests to `test_core.py` for new functions
2. Add integration tests to `test_cli.py` for new commands
3. Add edge cases to `test_edge_cases.py`
4. Update `test_plan.md` with new test cases
5. Ensure tests are independent and use fixtures

## Best Practices

- Use descriptive test names
- Test one thing per test function
- Use assertions for expected behavior
- Mock external dependencies
- Clean up after tests
- Document complex test logic