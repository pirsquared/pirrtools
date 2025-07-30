#!/usr/bin/env python3
"""
CLI entry point for pirrtools tutorial.

This module provides a command-line interface to launch the interactive
to_rich tutorial directly from the command line after installation.
"""

import sys
from pathlib import Path


def main():
    """Launch the interactive pirrtools to_rich tutorial."""
    try:
        import pirrtools

        # Try multiple locations for the tutorial script
        package_dir = Path(pirrtools.__file__).parent
        possible_paths = [
            # In installed package (distributed with MANIFEST.in)
            package_dir.parent / "examples" / "tutor.py",
            # In development environment
            package_dir.parent / "examples" / "tutor.py",
            # Alternative: if examples were packaged as package data
            package_dir / "examples" / "tutor.py",
        ]

        tutorial_path = None
        for path in possible_paths:
            if path.exists():
                tutorial_path = path
                break

        if tutorial_path is None:
            print("❌ Tutorial script not found!")
            print("The tutorial should be located at examples/tutor.py")
            print("\nTo run the tutorial manually:")
            print(
                "1. Clone the repository: "
                "git clone https://github.com/pirsquared/pirrtools"
            )
            print("2. Navigate to examples: cd pirrtools/examples")
            print("3. Run: python tutor.py")
            print(
                "\nAlternatively, you can find the tutorial in the examples directory"
            )
            print("of the pirrtools package.")
            return 1

        print("🚀 Launching pirrtools to_rich interactive tutorial...")
        print(f"📁 Tutorial location: {tutorial_path}")
        print("=" * 50)

        # Execute the tutorial script
        import subprocess

        result = subprocess.run(
            [sys.executable, str(tutorial_path)], cwd=tutorial_path.parent
        )
        return result.returncode

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure pirrtools is properly installed.")
        return 1
    except Exception as e:
        print(f"❌ Error launching tutorial: {e}")
        print("\nTo run the tutorial manually:")
        print("1. Navigate to the examples directory")
        print("2. Run: python tutor.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())
