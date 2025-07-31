============
Contributing
============

We welcome contributions to pirrtools! This guide covers how to set up your development environment and contribute to the project.

Getting Started
===============

**Fork and Clone**

1. Fork the repository on GitHub
2. Clone your fork locally:

.. code-block:: bash

   git clone https://github.com/yourusername/pirrtools.git
   cd pirrtools

**Development Setup**

Install in development mode:

.. code-block:: bash

   pip install -e .[dev]

This installs pirrtools in editable mode with all development dependencies.

**Docker Development** (Optional)

Use the provided Docker environment:

.. code-block:: bash

   docker-compose up -d
   docker-compose exec pirrtools-dev bash

Development Workflow
====================

**Code Style**

We use Black for code formatting:

.. code-block:: bash

   black pirrtools tests

**Linting**

Run pylint to check code quality:

.. code-block:: bash

   pylint pirrtools

**Pre-commit Hooks**

Set up pre-commit hooks to automatically format code:

.. code-block:: bash

   pre-commit install
   pre-commit run --all-files

**Testing**

Run tests with pytest:

.. code-block:: bash

   # Run all tests
   pytest
   
   # Run with coverage
   pytest --cov=pirrtools
   
   # Run specific test
   pytest tests/test_pandas.py::test_simple_dataframe

**Building Documentation**

Build Sphinx documentation:

.. code-block:: bash

   cd docs
   make html

Types of Contributions
======================

**Bug Reports**

When reporting bugs, please include:

- Operating system and Python version
- Complete error traceback
- Minimal example to reproduce the issue
- Expected vs actual behavior

**Feature Requests**

For new features:

- Describe the use case
- Provide examples of how it would work
- Consider implementation complexity
- Check if it fits the project scope

**Code Contributions**

- Fix bugs or implement features
- Add tests for new functionality
- Update documentation
- Follow existing code patterns

**Documentation**

- Fix typos or improve clarity
- Add missing docstrings
- Create new examples
- Improve existing tutorials

Code Guidelines
===============

**Style**

- Follow PEP 8 conventions
- Use Black for code formatting (88 character line length)
- Use Google/NumPy style docstrings
- Add type hints where helpful

**Testing**

- Write tests for new functionality
- Use pytest fixtures for test setup
- Test both success and failure cases
- Maintain or improve code coverage

**Documentation**

- Add docstrings to all public functions and classes
- Update relevant documentation files
- Include examples in docstrings
- Keep documentation current with code changes

**Git Commits**

- Use clear, descriptive commit messages
- Keep commits focused on single changes
- Reference issues when applicable
- Follow conventional commit format when possible

Pull Request Process
====================

**Before Submitting**

1. Ensure tests pass: ``pytest``
2. Format code: ``black pirrtools tests``
3. Run linting: ``pylint pirrtools``
4. Update documentation if needed
5. Add entry to changelog if significant

**Submitting**

1. Create a branch for your changes:

.. code-block:: bash

   git checkout -b feature/your-feature-name

2. Make your changes and commit:

.. code-block:: bash

   git add .
   git commit -m "Add feature: description of changes"

3. Push to your fork:

.. code-block:: bash

   git push origin feature/your-feature-name

4. Create a pull request on GitHub

**Pull Request Template**

Include in your PR:

- Clear description of changes
- Motivation and context
- Type of change (bug fix, feature, etc.)
- Testing performed
- Screenshots if applicable

Project Structure
=================

Understanding the codebase:

.. code-block::

   pirrtools/
   ├── __init__.py          # Main package with utilities
   ├── pandas.py            # Enhanced pandas functionality
   ├── list_chunks.py       # List chunking utilities
   ├── load.py              # Module loading helpers
   ├── sequences.py         # Sequence manipulation
   └── structures/          # Data structures
       ├── __init__.py
       ├── attrdict.py      # Dictionary with attribute access
       └── attrpath.py      # File system navigation
   
   tests/                   # Test suite
   ├── test_pandas.py       # Pandas functionality tests
   ├── test_list_chunks.py  # List chunking tests
   └── test_sequences.py    # Sequence tests
   
   examples/                # Usage examples
   ├── tutor.py            # Interactive tutorial
   ├── to_rich_examples.py # Comprehensive examples
   └── ...                 # Other example files
   
   docs/                   # Sphinx documentation
   ├── conf.py            # Sphinx configuration
   ├── index.rst          # Main documentation page
   └── ...                # Other documentation files

Areas for Contribution
======================

**High Priority**

- Bug fixes in existing functionality
- Performance improvements
- Better error messages and handling
- Additional test coverage

**Medium Priority**

- New styling options for ``to_rich`` method
- Additional pandas accessor methods
- New utility functions
- Documentation improvements

**Low Priority**

- Code cleanup and refactoring
- New examples and tutorials
- IDE integrations
- Performance benchmarks

Development Tips
================

**Local Testing**

Test your changes thoroughly:

.. code-block:: bash

   # Run full test suite
   pytest
   
   # Test specific functionality
   python -c "
   import pandas as pd
   import pirrtools
   df = pd.DataFrame({'A': [1,2,3]})
   print(df.pirr.to_rich())
   "

**Debugging**

Use the examples directory for testing:

.. code-block:: bash

   cd examples
   python tutor.py  # Test to_rich functionality
   python to_rich_examples.py  # Test comprehensive features

**Documentation Testing**

Build and check documentation:

.. code-block:: bash

   cd docs
   make html
   open _build/html/index.html  # Check rendered docs

Release Process
===============

(For maintainers)

1. Update version in ``pyproject.toml``
2. Update ``CHANGELOG.md``
3. Create git tag: ``git tag v0.x.x``
4. Push tag: ``git push origin v0.x.x``
5. GitHub Actions will automatically publish to PyPI

Questions?
==========

- Open an issue for questions about contributing
- Review existing issues and PRs for context
- Check the documentation for implementation details
- Ask questions in pull request discussions

Thank you for contributing to pirrtools! 🎉