Python

Day 19: Python Introduction

1. What is Python?
Python is a high-level, interpreted, general-purpose programming language created by Guido van Rossum in 1991.
 
2. Why Python is Popular?
- Easy to learn
- Simple syntax
- Large community
- Cross-platform
- Used by top companies
 
3. Where is Python Used?
Web Development, Data Science, AI, Automation, DevOps, Cyber Security, Games, IoT
 
4. Features of Python
- High-level
- Interpreted
- Platform-independent
- Open-source
- Large standard library
 
5. History of Python
- Developed by Guido van Rossum
- Named after Monty Python
- First released in 1991
 
6. Python Versions
Python 2 (Discontinued)
Python 3 (Recommended)
 
7. How Python Works
Code → Interpreter → Output
 
8. Python Installation (Windows 11)
Download from python.org
Check "Add Python to PATH"
Verify using: python --version
 
9. IDEs for Python
VS Code, Notepad++, Sublime Text
 
10. Python vs Other Languages
Python is easier to learn compared to Java and C.
 
11. Advantages
Easy, fast development, free, high demand
 
12. Disadvantages
Slower than C/Java, more memory usage
 
 
Python Installation on Windows
Uninstall via Settings
1.	Settings → Apps → Installed apps
2.	Search Python
3.	Click Uninstall
 
Delete the following if exists
Step 1: Open the Folder
1.	Press Win + R
2.	Paste: 
%LocalAppData%\Microsoft\WindowsApps
3.	Press Enter
 
Step 2: Identify Python Files
python.exe
python3.exe
python3.11.exe
pythonw.exe
pip.exe
pip3.exe
pip3.11.exe
 
Step 3: Delete Python Files
1.	Select only the Python-related files
2.	Press Delete
3.	Empty the Recycle Bin
 
Step 4: To Install Python on Windows folow these
https://bhavikjikadara.medium.com/how-to-install-python-on-windows-11-4903cdb5626b

Day 20: Syntax

PYTHON COMMENTS
What is a Comment?
A comment is a line in your code that Python does not execute. It is only for humans to read.
Single-Line Comment:
# This is a comment
Multi-Line Comment:
'''
This is a multi-line comment
'''
Why Comments are Important:
- Makes code easy to understand
- Helps beginners
- Useful for teamwork
Shortcut -> Select lines that you want to commit and press ctrl /
 
PYTHON INDENTATION
What is Indentation?
Indentation means giving space at the start of a line.
Example (Wrong):
if 5 > 2:
print("Hello")
Correct Example:
if 5 > 2:
    print("Hello")
Why Indentation is Important:
- Python uses indentation to group code
- Without it, code will fail
PYTHON IDENTIFIERS
What is an Identifier?
An identifier is the name of a variable, function, or class.
Example:
name = "Bharath"
Rules:
- Must start with a letter or _
- Cannot start with a number
- No spaces allowed
- No keywords allowed
Valid:
age, student_name, _total
Invalid:
2name, my name, class
 
PYTHON FILE NAMING CONVENTION
Python files must end with .py
Good names:
main.py
student_data.py
Bad names:
my file.py
1test.py
Test@123.py
Rules:
- Use lowercase letters
- Use _ instead of spaces
- Keep names simple

Day 21: Datatypes

Comments in Python
A comment is a line of code that Python ignores during execution. It is used to explain code or leave notes for other developers.
Types of Comments
1. Single-line Comments
Use the '#' symbol:


# This is a single-line comment
print("Hello")  # This comment is after a line of code
 
2. Multi-line Comments
There’s no official multi-line comment syntax, but you can use triple quotes (''' or """) as a workaround:


'''
This is a multi-line comment
used for documentation or explanation
'''
print("Python")


Note: Triple quotes are actually strings, so use them only when not assigned to any variable.
When to Use Comments
•	To describe what a complex piece of code is doing.
- To explain why a specific approach or algorithm is used.
- To leave reminders or TODOs.
- To make the code more readable for collaborators or your future self.
- To separate logical sections in your code.
 
Identifiers
Identifiers are the names used to identify variables, functions, classes, modules, etc.
They must follow certain rules:
- Must begin with a letter (A–Z or a–z) or an underscore (_)
- Followed by letters, digits (0–9), or underscores
- Case-sensitive (e.g., `Name` and `name` are different)
- Cannot use Python keywords as identifiers (e.g., `if`, `class`, `for`)
Valid Identifiers:
age, _value, user1

Invalid Identifiers:
1user, user-name, for


Data Types in Python
Python supports various built-in data types to represent different kinds of values. These types help Python know how to store and process the data.
 
Integer Types in Python
An integer is a whole number (no decimal point). In Python, all integer values are of type 'int'.
Examples:
x = 5          # Positive integer
y = -10        # Negative integer
z = 0          # Zero
Type Check
Use type() to check if a value is an integer:
print(type(x))  # <class 'int'>

Integer Characteristics
Python integers have unlimited precision:
big = 999999999999999999999999999999999
print(big)  # Works fine!
 
 
Referece
 
https://docs.python.org/3/library/stdtypes.html



Day 21: Strings

