"""
A comprehensive guide to understanding Python Packages, Modules, and Libraries/Frameworks.

Package:
    A package is a way of organizing related modules into a directory hierarchy. It contains
    a special __init__.py file and can have multiple modules and sub-packages. Packages help
    organize code into logical groups and prevent naming conflicts.
    
    Example structure:
        mypackage/
            __init__.py
            module1.py
            module2.py
            subpackage/
                __init__.py
                module3.py

Module:
    A module is a single Python file (.py) containing Python code. It can define functions,
    classes, and variables that can be imported and used elsewhere. A module is the simplest
    unit of code organization.
    
    Example:
        mymodule.py  # This is a module

Library/Framework:
    A library (or framework) is a collection of packages and modules that provides pre-built
    functionality for specific tasks. Libraries are reusable collections of code, while
    frameworks provide a structured foundation for building applications with predefined patterns.

Key Differences:
    
    | Aspect      | Module          | Package              | Library/Framework     |
    |-------------|-----------------|----------------------|-----------------------|
    | Structure   | Single .py file | Directory with mods  | Collection of packages|
    | Purpose     | Basic reuse     | Organize modules     | Complete solution     |
    | Scope       | Small scale     | Medium scale         | Large scale           |
    | __init__.py | Not needed      | Required             | Multiple files        |
    | Example     | math.py         | django.db            | NumPy, Django, Flask  |
    
Relationship:
    Module (smallest) → Package (medium) → Library/Framework (largest)
    
    A package IS made of modules.
    A library/framework IS made of packages and modules.
"""