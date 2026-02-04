import math
from math import sqrt, pi
import math as m
from math import *
from datetime import datetime, timedelta
import random
import os
import sys
from collections import Counter, defaultdict
import json
import importlib
import math as m

# ============================================================================
# PYTHON MODULES - COMPLETE GUIDE WITH EXAMPLES AND INTERVIEW Q&A
# ============================================================================

"""
A MODULE is a file containing Python code (variables, functions, classes).
Modules help organize code, promote reusability, and avoid naming conflicts.
"""

# ============================================================================
# 1. CREATING AND IMPORTING MODULES
# ============================================================================

# Example 1: Importing entire module
print("Example 1: Import entire module")
print(f"Square root of 16: {math.sqrt(16)}")  # Output: 4.0
print(f"Pi value: {math.pi}")  # Output: 3.14159...
print()

# Example 2: Import specific function from module
print("Example 2: Import specific items")
print(f"Sqrt of 25: {sqrt(25)}")  # Output: 5.0
print()

# Example 3: Import with alias
print("Example 3: Import with alias")
print(f"Factorial of 5: {m.factorial(5)}")  # Output: 120
print()

# Example 4: Import all from module (not recommended)
print("Example 4: Import all (*)")
print(f"Ceiling of 4.3: {ceil(4.3)}")  # Output: 5
print()

# ============================================================================
# 2. BUILT-IN MODULES
# ============================================================================

# Example 5: datetime module
print("Example 5: datetime module")
current_time = datetime.now()
print(f"Current time: {current_time}")  # Output: 2024-01-15 10:30:45.123456
tomorrow = current_time + timedelta(days=1)#timedelta(days=1) represents a duration of one day
print(f"Tomorrow: {tomorrow}")
print()

# Example 6: random module
print("Example 6: random module")
print(f"Random integer (1-10): {random.randint(1, 10)}")  # Output: varies
print(f"Random choice: {random.choice(['apple', 'banana', 'cherry'])}")  # Output: varies
print()

# Example 7: os module
print("Example 7: os module")
print(f"Current directory: {os.getcwd()}") # Output: current working directory
print(f"OS name: {os.name}")  # Output: nt (Windows) or posix (Linux/Mac)
print()

# Example 8: sys module
print("Example 8: sys module")
print(f"Python version: {sys.version}") # Output: Python version info
print(f"Python path: {sys.path[:2]}")  # First 2 paths
print()

# Example 9: collections module
print("Example 9: collections module")
data = [1, 1, 1, 2, 2, 3]
print(f"Counter: {Counter(data)}")  # Output: Counter({1: 3, 2: 2, 3: 1})
print()

# Example 10: json module
print("Example 10: json module")
data_dict = {"name": "John", "age": 30}
json_str = json.dumps(data_dict)
print(f"JSON string: {json_str}")  # Output: {"name": "John", "age": 30}
parsed = json.loads(json_str)
print(f"Parsed back: {parsed}")
print()

# ============================================================================
# 3. CHECKING WHAT'S IN A MODULE
# ============================================================================

print("Example 11: Exploring module contents")
print(f"All attributes in math: {dir(math)[:5]}...")  # Shows first 5
print(f"Help on sqrt: {help(math.sqrt)}")
print()

# ============================================================================
# 4. MODULE VARIABLES AND ATTRIBUTES
# ============================================================================

print("Example 12: Module attributes")
print(f"math.__name__: {math.__name__}")  # Output: math
print(f"math.__file__: {math.__file__}")  # Shows file location
print()

# ============================================================================
# 5. CREATING YOUR OWN CUSTOM MODULES
# ============================================================================

"""
To create a custom module:
1. Create a Python file (e.g., my_module.py)
2. Write functions/classes in it
3. Import it in another file

Example custom module file: my_math.py
---
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

PI = 3.14159
---

Then import: import my_math
Usage: my_math.add(5, 3)  # Output: 8
"""

# ============================================================================
# 6. __name__ VARIABLE - IMPORTANT CONCEPT
# ============================================================================

print("Example 13: __name__ variable")
print(f"Current script name: {__name__}")  # Output: __main__ (when run directly)
print()

"""
When you run a file directly: __name__ = "__main__"
When you import it: __name__ = "module_name"

This allows code to run only when file is executed directly:
if __name__ == "__main__":
    # This runs only when file is run, not when imported
    print("Running directly")
"""

# ============================================================================
# 7. PACKAGE VS MODULE
# ============================================================================

"""
MODULE: A single .py file
PACKAGE: A directory with __init__.py file containing multiple modules

Structure:
mypackage/
    __init__.py
    module1.py
    module2.py
    subpackage/
        __init__.py
        module3.py

Import: from mypackage.module1 import function_name
"""

# ============================================================================
# INTERVIEW QUESTIONS & ANSWERS
# ============================================================================

"""
# ============================================================================
# TYPES OF MODULES IN PYTHON
# ============================================================================

print("=" * 70)
print("TYPES OF MODULES IN PYTHON")
print("=" * 70)
print()

# TYPE 1: BUILT-IN MODULES
print("TYPE 1: BUILT-IN MODULES")
print("-" * 70)
print("Definition: Modules that come pre-installed with Python")
print("Examples: math, random, datetime, os, sys, json, collections")
print()
print("Examples:")
print(f"  math.sqrt(16) = {math.sqrt(16)}")
print(f"  random.randint(1, 100) = {random.randint(1, 100)}")
print(f"  datetime.now() = {datetime.now()}")
print()

# TYPE 2: THIRD-PARTY MODULES
print("TYPE 2: THIRD-PARTY MODULES")
print("-" * 70)
print("Definition: Modules created by developers, installed via pip")
print("Examples: numpy, pandas, requests, flask, django, matplotlib")
print()
print("Installation: pip install module_name")
print("Usage: import numpy as np")
print("  Note: Not imported here as they may not be installed")
print()

# TYPE 3: CUSTOM/USER-DEFINED MODULES
print("TYPE 3: CUSTOM/USER-DEFINED MODULES")
print("-" * 70)
print("Definition: Modules you create yourself in .py files")
print()
print("Example structure:")
print("  my_calculator.py:")
print("    def add(a, b):")
print("        return a + b")
print("    def multiply(a, b):")
print("        return a * b")
print()
print("  main.py:")
print("    import my_calculator")
print("    result = my_calculator.add(5, 3)  # Output: 8")
print()

# TYPE 4: PACKAGES
print("TYPE 4: PACKAGES")
print("-" * 70)
print("Definition: Directory containing modules and __init__.py file")
print()
print("Directory structure:")
print("  myapp/")
print("    __init__.py")
print("    math_ops.py")
print("    string_ops.py")
print("    utils/")
print("      __init__.py")
print("      helpers.py")
print()
print("Usage:")
print("  from myapp.math_ops import add")
print("  from myapp.utils.helpers import format_text")
print()

# TYPE 5: NAMESPACE PACKAGES
print("TYPE 5: NAMESPACE PACKAGES")
print("-" * 70)
print("Definition: Packages without __init__.py (Python 3.3+)")
print("Allow splitting package across multiple directories")
print()
print("Directory structure:")
print("  path1/myapp/module1.py")
print("  path2/myapp/module2.py")
print()
print("Usage: from myapp import module1, module2")
print()

# COMPARISON TABLE
print("=" * 70)
print("COMPARISON TABLE")
print("=" * 70)
print()
print("Type              | Source        | Installation | Example")
print("-" * 70)
print("Built-in          | Python        | Pre-installed| math, os, sys")
print("Third-party       | External dev  | pip install  | numpy, pandas")
print("Custom            | You           | Manual       | my_module.py")
print("Package           | You/External  | Manual/pip   | myapp/")
print("Namespace Package | You/External  | Manual       | path1/myapp/")
print()
Q1: What is a module in Python?
A1: A module is a file containing Python code (functions, classes, variables).
    It helps organize code and promote reusability.
    Example: import math; print(math.sqrt(16))  # Output: 4.0

Q2: Difference between module and package?
A2: Module is a .py file, Package is a directory with __init__.py
    Module: math.py
    Package: mypackage/__init__.py + mypackage/module1.py

Q3: What does 'import *' do? Is it recommended?
A3: It imports all public names from module.
    Not recommended as it can cause naming conflicts.
    Example: from math import *
    Use specific imports instead: from math import sqrt

Q4: How does Python find modules?
A4: Python searches in sys.path (directories list)
    Order: current directory, PYTHONPATH, installation-dependent paths
    Example: import sys; print(sys.path)

Q5: What's the difference between 'import X' and 'from X import Y'?
A5: import X: imports entire module, access as X.Y
    from X import Y: imports specific item, access directly as Y
    Example:
    import math; math.sqrt(4)  # Output: 2.0
    from math import sqrt; sqrt(4)  # Output: 2.0

Q6: Can you reload a module?
A6: Yes, using importlib.reload()
    importlib.reload(module_name)

Q7: What is __init__.py?
A7: Makes Python treat directory as package (required in Python < 3.3)
    Can contain initialization code for package

Q8: What's the __name__ == "__main__" check?
A8: Allows code to run only when file is executed directly, not when imported
    if __name__ == "__main__": print("Running directly")

Q9: How to check what's in a module?
A9: Use dir() and help()
    dir(math) - lists all attributes
    help(math.sqrt) - shows documentation

Q10: What's aliasing?
A10: Giving another name to imported module
     print(m.sqrt(4))  # Output: 2.0
"""

# ============================================================================
# QUICK REFERENCE TABLE
# ============================================================================

"""
IMPORT METHOD          | USAGE                    | ADVANTAGE
-----------------------|--------------------------|---------------------------
import math            | math.sqrt(4)             | Clear namespace
from math import sqrt  | sqrt(4)                  | Shorter syntax
import math as m       | m.sqrt(4)                | Shorter name
from math import *     | sqrt(4)                  | No prefix needed

COMMON BUILT-IN MODULES:
- math: Mathematical functions
- random: Random number generation
- datetime: Date and time
- os: Operating system operations
- sys: System-specific parameters
- json: JSON encoding/decoding
- collections: Special data structures
- itertools: Iterator tools
- functools: Higher-order functions
- re: Regular expressions
"""

print("\n✓ Module guide complete! Refer comments for detailed learning.")