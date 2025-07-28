=========
Changelog
=========

All notable changes to pirrtools will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
============

Added
-----
- Comprehensive Sphinx documentation with tutorials and API reference
- Interactive tutorial script (``examples/tutor.py``) for learning to_rich features
- Professional documentation structure with installation guide and examples
- Enhanced docstrings following Google/NumPy style conventions across all modules

Changed
-------
- Organized all example files into ``examples/`` directory for better structure
- Improved code documentation quality and consistency throughout codebase
- Enhanced error handling and parameter validation in core functions

[0.2.14] - 2024-XX-XX
======================

Added
-----
- Enhanced ``to_rich`` method with full-width background color support
- New styling parameters for professional table appearance
- Support for alternating row colors and custom theming
- Integration with existing pandas Styler objects

Changed
-------
- Improved background padding for styled tables
- Optimized Rich table rendering for better performance
- Enhanced gradient color mapping and text styling options

Fixed
-----
- Background color rendering issues with varied text lengths
- Style inheritance problems in complex table configurations

[0.2.13] - Previous Release
============================

- Core ``to_rich`` functionality
- Basic pandas accessor methods
- AttrPath file system navigation
- Caching system for pandas objects

[0.2.12] - Previous Release  
============================

- Initial pandas caching functionality
- Basic AttrDict implementation
- Core utility functions

Earlier Versions
================

See git history for details on earlier releases.

Migration Guide
===============

From 0.2.13 to 0.2.14
----------------------

**New Features Available:**
- Enhanced background styling options
- Professional table theming
- Improved gradient rendering

**Breaking Changes:**
None. All existing code remains compatible.

**Recommended Updates:**
- Update example code to use new styling parameters
- Consider migrating to enhanced background options for better appearance

Development Notes
=================

**Version Numbering:**
- Major version (X.0.0): Breaking changes or major feature additions
- Minor version (0.X.0): New features, backward compatible
- Patch version (0.0.X): Bug fixes, documentation updates

**Release Schedule:**
- Patches: As needed for critical bugs
- Minor releases: Monthly or when significant features are ready
- Major releases: Annually or for breaking changes

**Deprecation Policy:**
- Features marked deprecated in version X.Y.Z will be removed in version (X+1).0.0
- At least 6 months notice will be given for breaking changes
- Migration guides will be provided for major changes