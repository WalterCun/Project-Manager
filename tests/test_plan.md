# Test Plan for Project Structure Manager CLI

## Overview
This test plan covers comprehensive testing of the Project Structure Manager CLI tool, including all commands, parameters, and edge cases. The tests are organized into unit tests for individual functions and integration tests for end-to-end command execution.

## Test Structure
- **Unit Tests**: Test individual functions and methods in isolation.
- **Integration Tests**: Test full command execution, including CLI parsing, database interactions, and file system operations.
- **Edge Case Tests**: Test error conditions, invalid inputs, and boundary scenarios.

## Commands and Parameters

### 1. create-project
**Parameters:**
- name (required): Project name
- --path (optional): Path to generate structure (default: '.')
- --regenerate (optional): Regenerate existing project
- --restart (optional): Restart with default structure
- --force (optional): Force overwrite

**Test Cases:**
- Create new project with default path
- Create new project with custom path
- Create project with existing name (should show menu or use --force)
- Create project with existing directory (empty vs with files)
- Use --regenerate on existing project
- Use --restart on existing project
- Use --force to skip menu
- Invalid project name (empty, special characters)
- Non-existent path
- Permission denied on path

### 2. list-projects
**Parameters:** None

**Test Cases:**
- List when no projects exist
- List when projects exist
- Check output format

### 3. generate-structure
**Parameters:**
- id (required): Project ID
- path (required): Base path

**Test Cases:**
- Generate structure for existing project
- Generate structure for non-existent project ID
- Generate to existing directory
- Generate to non-existent directory
- Invalid ID (non-integer, negative)

### 4. export-json
**Parameters:**
- id (required): Project ID
- file (required): Output file

**Test Cases:**
- Export existing project
- Export non-existent project
- Export to existing file (overwrite)
- Invalid file path
- Invalid ID

### 5. import-json
**Parameters:**
- name (required): Project name
- file (required): Input JSON file

**Test Cases:**
- Import valid JSON
- Import invalid JSON (malformed, missing fields)
- Import with existing project name
- Non-existent file
- Empty file

### 6. scan-directory
**Parameters:**
- name (required): Project name
- path (required): Directory to scan

**Test Cases:**
- Scan existing directory
- Scan non-existent directory
- Scan empty directory
- Scan with existing project name
- Permission denied

### 7. Template Commands
#### template crear
**Parameters:**
- nombre (required)
- --extension (required)
- --contenido (optional)
- --padre (optional)
- --project (optional)

**Test Cases:**
- Create template with all parameters
- Create template with minimal parameters
- Create with existing name
- Invalid extension
- Invalid parent ID

#### template modificar
**Parameters:**
- id (required)
- --nombre (optional)
- --contenido (optional)
- --extension (optional)
- --padre (optional)
- --project (optional)

**Test Cases:**
- Modify existing template
- Modify non-existent template
- Partial modifications
- Invalid ID

#### template heredar
**Parameters:**
- nombre (required)
- --padre (required)
- --extension (required)
- --project (optional)

**Test Cases:**
- Inherit from existing template
- Inherit from non-existent template
- Invalid parent ID

#### template render
**Parameters:**
- id (required)
- --output (optional)
- params (variable)

**Test Cases:**
- Render existing template
- Render with parameters
- Render without parameters (if required)
- Invalid ID
- Invalid output path

#### template listar
**Parameters:**
- --project (optional)

**Test Cases:**
- List all templates
- List templates for specific project
- No templates

#### template eliminar
**Parameters:**
- id (required)

**Test Cases:**
- Delete existing template
- Delete non-existent template
- Invalid ID

#### template external listar
**Parameters:**
- --extension (optional)

**Test Cases:**
- List all external templates
- List by extension
- No external templates

#### template external crear
**Parameters:**
- name (required)
- extension (required)
- --content (optional)
- --description (optional)
- --version (optional)
- --author (optional)

**Test Cases:**
- Create external template
- Create with existing name
- Invalid extension

#### template external eliminar-ext
**Parameters:**
- name (required)
- extension (required)

**Test Cases:**
- Delete existing external template
- Delete non-existent template

## Test Categories

### Unit Tests
- Test individual functions in src/core/database.py, src/core/structure_generator.py, src/templates/models.py, etc.
- Mock dependencies (database, file system)
- Test business logic in isolation

### Integration Tests
- Test full command execution using subprocess or CLI runner
- Check database state after commands
- Verify file creation and content
- Test command output and exit codes

### Edge Case Tests
- Network errors (if applicable)
- Database corruption
- File system full
- Permission errors
- Invalid file formats
- Large inputs
- Concurrent access

## Test Data and Fixtures
- Sample project structures
- Sample templates (JSON, DOCX, etc.)
- Temporary directories
- Mock database states
- Invalid files for error testing

## Tools and Frameworks
- **pytest**: Main testing framework
- **pytest-mock**: For mocking
- **pytest-cov**: For coverage
- **tmp_path**: For temporary files
- **subprocess**: For CLI testing
- **sqlite3**: For database testing

## Execution
- Run unit tests: `pytest tests/test_core.py`
- Run integration tests: `pytest tests/test_cli.py`
- Run all: `pytest`
- Coverage: `pytest --cov=src`

## Maintenance
- Update tests when new features are added
- Ensure tests are independent
- Use descriptive test names
- Document expected behavior in comments