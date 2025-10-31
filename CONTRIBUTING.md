# 🤝 Contributing to Blender MCP Server

Thank you for your interest in contributing to the Blender MCP Server! This document provides guidelines and information for contributors.

## 🎯 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Pull Requests](#submitting-pull-requests)

## 📋 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Standards

- **Be respectful and inclusive** in your language and actions
- **Be collaborative** and help others learn
- **Focus on constructive feedback** and solutions
- **Respect differing viewpoints and experiences**
- **Show empathy towards other community members**

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+**
- **Blender 3.6+** with Python API access
- **Git** for version control
- **VS Code** or similar IDE (recommended)

### Quick Setup

1. **Fork the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/blender-mcp-server.git
   cd blender-mcp-server
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

## 🛠️ Development Setup

### Project Structure

```
blender-mcp-server/
├── src/blender_mcp_server/     # Main source code
│   ├── server.py              # FastMCP implementation
│   ├── simple_server.py       # Self-contained version
│   └── __init__.py
├── tests/                      # Test suite
├── docs/                       # Documentation
├── examples/                   # Usage examples
├── .github/                    # GitHub workflows
└── tools/                      # Development tools
```

### Code Quality Tools

We use several tools to maintain code quality:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Code formatting
black src/ tests/ examples/
isort src/ tests/ examples/

# Linting
ruff check src/ tests/ examples/
mypy src/blender_mcp_server/

# Security scanning
bandit -r src/
```

## 🔧 Making Changes

### Branch Naming Convention

Use descriptive branch names:

- `feature/add-new-tool` - Adding new functionality
- `fix/connection-timeout` - Bug fixes
- `docs/update-api-reference` - Documentation updates
- `refactor/error-handling` - Code refactoring

### Commit Message Format

Follow conventional commits:

```
type(scope): description

Longer explanation if needed

Fixes #123
```

**Types:**
- `feat` - New features
- `fix` - Bug fixes
- `docs` - Documentation changes
- `style` - Code style changes
- `refactor` - Code refactoring
- `test` - Adding or updating tests
- `chore` - Maintenance tasks

**Examples:**
```
feat(scene): add scene duplication functionality
fix(object): resolve transformation parameter validation
docs(api): update tool parameter documentation
```

### Adding New Tools

1. **Design the tool:**
   - Define the tool's purpose and parameters
   - Consider security implications
   - Plan for error handling

2. **Implement the tool:**
   ```python
   @server.list_tools()
   async def handle_list_tools():
       return [
           Tool(
               name="my_new_tool",
               description="Description of the tool",
               inputSchema={
                   "type": "object",
                   "properties": {
                       "param1": {
                           "type": "string",
                           "description": "Parameter description"
                       }
                   },
                   "required": ["param1"]
               }
           )
       ]

   @server.call_tool()
   async def handle_call_tool(name, arguments):
       if name == "my_new_tool":
           try:
               # Implementation here
               result = await execute_blender_operation(arguments)
               return [TextContent(type="text", text=f"Success: {result}")]
           except Exception as e:
               raise MCPError(f"Operation failed: {str(e)}")
   ```

3. **Add comprehensive tests:**
   ```python
   def test_my_new_tool(self):
       """Test the new tool functionality."""
       # Test successful execution
       # Test parameter validation
       # Test error cases
   ```

4. **Update documentation:**
   - Add tool to API reference
   - Include usage examples
   - Update README if needed

### Code Style Guidelines

- **Follow PEP 8** style guidelines
- **Use type hints** for all functions and parameters
- **Write docstrings** for all public functions
- **Keep functions focused** - single responsibility principle
- **Handle errors gracefully** - provide meaningful error messages

## 🧪 Testing

### Test Categories

1. **Unit Tests** - Test individual functions and methods
2. **Integration Tests** - Test tool interactions with Blender
3. **API Tests** - Test MCP protocol compliance
4. **Security Tests** - Test safety features and validations

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/blender_mcp_server

# Run specific test categories
pytest tests/test_blender_mcp_server.py::TestSceneManagement

# Run in verbose mode
pytest -v

# Run with markers
pytest -m "not slow"
```

### Writing Tests

```python
import pytest
from blender_mcp_server.server import BlenderMCPServer

class TestMyFeature:
    def test_successful_operation(self):
        """Test successful operation execution."""
        server = BlenderMCPServer()
        # Test implementation
        pass

    def test_parameter_validation(self):
        """Test parameter validation."""
        with pytest.raises(ValidationError):
            # Test invalid parameters
            pass

    def test_error_handling(self):
        """Test error handling."""
        # Test error scenarios
        pass
```

### Test Coverage

Maintain high test coverage:

```bash
# Generate coverage report
pytest --cov=src/blender_mcp_server --cov-report=html

# View coverage report
open htmlcov/index.html
```

## 📚 Documentation

### Types of Documentation

1. **API Documentation** - Tool descriptions and parameters
2. **User Guides** - How to use the server
3. **Developer Documentation** - Architecture and design decisions
4. **Examples** - Code examples and use cases

### Documentation Standards

- **Keep it up to date** - Update docs when making changes
- **Use clear examples** - Include practical usage examples
- **Add diagrams** - Visual aids for complex concepts
- **Cross-reference** - Link related sections

### Building Documentation

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build documentation
mkdocs build

# Serve documentation locally
mkdocs serve
```

## 📤 Submitting Pull Requests

### Before Submitting

1. **Run all tests:**
   ```bash
   pytest
   ```

2. **Check code quality:**
   ```bash
   black src/ tests/
   ruff check src/ tests/
   mypy src/blender_mcp_server/
   ```

3. **Update tests** for any new functionality

4. **Update documentation** as needed

5. **Add entry to CHANGELOG.md**

### Pull Request Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe):

## Testing
- [ ] All tests pass
- [ ] Added/updated tests for changes
- [ ] Manual testing completed

## Documentation
- [ ] Documentation updated
- [ ] Examples updated if applicable

## Security
- [ ] No security implications
- [ ] Security considerations addressed
- [ ] Permission requirements documented

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Changes documented in CHANGELOG.md
- [ ] Related issues linked
```

### Review Process

1. **Automated checks** will run (CI/CD pipeline)
2. **Code review** by maintainers
3. **Testing** on different platforms
4. **Documentation** review
5. **Final approval** and merge

## 🐛 Reporting Issues

### Bug Reports

Use the bug report template:

```markdown
**Describe the bug**
Clear description of the issue.

**To Reproduce**
Steps to reproduce the behavior:
1. Start Blender with MCP addon
2. Run tool X with parameters Y
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. Ubuntu 20.04]
- Blender Version: [e.g. 3.6.0]
- Python Version: [e.g. 3.12.0]
- MCP Server Version: [e.g. 1.0.0]

**Additional context**
Other relevant information.
```

### Feature Requests

Use the feature request template:

```markdown
**Is your feature request related to a problem?**
Clear description of the problem.

**Describe the solution you'd like**
Clear description of what you want to happen.

**Describe alternatives you've considered**
Clear description of alternative solutions.

**Additional context**
Other relevant information or screenshots.
```

## 🎯 Development Priorities

### Current Focus Areas

1. **Tool Expansion** - Adding more Blender API capabilities
2. **Performance** - Optimization for large scenes
3. **Security** - Enhanced safety features
4. **Documentation** - Comprehensive user guides
5. **Testing** - Increased test coverage

### Good First Issues

Look for issues labeled with:
- `good first issue` - Beginner-friendly
- `help wanted` - Community contributions needed
- `documentation` - Documentation improvements

## 📞 Getting Help

- **GitHub Discussions** - Community support and questions
- **GitHub Issues** - Bug reports and feature requests
- **Documentation** - Comprehensive guides and examples
- **Discord/Slack** - Real-time community chat (if available)

## 🙏 Recognition

Contributors will be recognized in:

- **README.md** - List of contributors
- **Releases** - Thank contributors in release notes
- **Hall of Fame** - Special recognition for significant contributions

---

**Thank you for contributing to Blender MCP Server!** 🚀

Your contributions help make 3D creation more accessible through AI-powered automation.