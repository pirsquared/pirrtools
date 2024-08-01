"""setup.py.

This setup.py file is included to support editable installations using pip's `-e`
option. The primary project configuration is specified in the pyproject.toml file. This
setup.py is only used for development installations and ensures compatibility with tools
and workflows that rely on setup.py.
"""

from setuptools import setup, find_packages

setup(
    name="pirrtools",
    version="0.2.11",  # Update this version number before releasing a new version
    description="Collection of tools I use in my projects",
    author="Sean Smith",
    author_email="pirsquared.pirr@gmail.com",
    url="https://github.com/pirsquared/pirrtools",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "feather-format",
        "ipython",
        "Pygments",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "build",
            "twine",
            "black",
            "pre-commit",
            "pylint",
        ],
    },
)
