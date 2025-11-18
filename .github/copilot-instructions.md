# Copilot Instructions for Claude Agent Project

## Project Overview
This is the Claude Agent project - an AI-powered development assistant built with Python and modern web technologies.

## Development Environment
- **Python Version**: 3.12 (via conda environment 'claude')
- **Package Manager**: pip (within conda environment)
- **IDE**: VS Code with GitHub Copilot

## Code Style Guidelines
- Follow PEP 8 Python style guidelines
- Use type hints for function parameters and return values
- Write descriptive variable and function names
- Include docstrings for all public functions and classes
- Keep functions small and focused on single responsibilities

## Project Structure
- `src/`: Main source code
- `tests/`: Unit and integration tests
- `docs/`: Documentation
- `scripts/`: Utility scripts

## Key Dependencies
- Core Python libraries as needed
- Testing framework (pytest recommended)
- Documentation tools (Sphinx recommended)

## Development Workflow
1. Always activate the 'claude' conda environment before working
2. Create feature branches for new work
3. Write tests before implementing features
4. Ensure all tests pass before committing
5. Follow conventional commit message format

## AI Assistant Guidelines
- Prefer functional programming patterns where appropriate
- Suggest modern Python features (f-strings, dataclasses, etc.)
- Recommend best practices for error handling and logging
- Help maintain clean, readable, and maintainable code
- Suggest appropriate design patterns when relevant

## Security Considerations
- Never commit sensitive information (API keys, passwords, etc.)
- Use environment variables for configuration
- Validate all user inputs
- Follow principle of least privilege

## Testing
- Write unit tests for all new functions
- Include integration tests for API endpoints
- Aim for high test coverage (>80%)
- Use descriptive test names that explain the expected behavior