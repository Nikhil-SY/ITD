import csv
import json
import os

# ============================================
# FILE OPERATIONS IN PYTHON - COMPLETE GUIDE
# ============================================

# 1. OPENING AND READING FILES
# ============================

# Method 1: Basic file reading
file = open('sample.txt', 'r')
content = file.read()  # Read entire file
file.close()

# Method 2: Using context manager (RECOMMENDED)
with open('sample.txt', 'r') as file:
    content = file.read()
# File automatically closes

# Method 3: Read line by line
with open('sample.txt', 'r') as file:
    for line in file:
        print(line.strip())

# Method 4: Read all lines into a list
with open('sample.txt', 'r') as file:
    lines = file.readlines()

# ============================================
# 2. WRITING TO FILES
# ============================================

# Write mode (overwrites)
with open('output.txt', 'w') as file:
    file.write('Hello, World!\n')
    file.write('Python File Operations\n')

# Append mode (adds to existing)
with open('output.txt', 'a') as file:
    file.write('Appended line\n')

# Write multiple lines
lines = ['Line 1\n', 'Line 2\n', 'Line 3\n']
with open('output.txt', 'w') as file:
    file.writelines(lines)

# ============================================
# 3. FILE MODES
# ============================================

"""
'r'  - Read (default)
'w'  - Write (creates/overwrites)
'a'  - Append (adds to end)
'x'  - Create (fails if exists)
'b'  - Binary mode
't'  - Text mode (default)
'+'  - Read and Write
"""

# ============================================
# 4. WORKING WITH CSV FILES
# ============================================


# Reading CSV
with open('data.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)

# Writing CSV
with open('data.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Name', 'Age', 'City'])
    csv_writer.writerow(['John', '25', 'NYC'])

# ============================================
# 5. WORKING WITH JSON FILES
# ============================================


# Reading JSON
with open('data.json', 'r') as file:
    data = json.load(file)
    print(data)

# Writing JSON
data = {'name': 'John', 'age': 25, 'city': 'NYC'}
with open('data.json', 'w') as file:
    json.dump(data, file, indent=2)

# ============================================
# 6. FILE OPERATIONS - PRACTICAL EXAMPLE
# ============================================

# Create and write to file
with open('students.txt', 'w') as file:
    file.write('Name,Age,Grade\n')
    file.write('Alice,20,A\n')
    file.write('Bob,19,B\n')
    file.write('Charlie,21,A\n')

# Read and process
with open('students.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        print(line.strip()) #output each line

# ============================================
# 7. FILE METHODS
# ============================================

with open('sample.txt', 'r') as file:
    # read(size) - Read up to size characters
    content = file.read(50)
    
    # readline() - Read one line
    line = file.readline()
    
    # readlines() - Read all lines as list
    all_lines = file.readlines()
    
    # seek(position) - Move cursor
    file.seek(0)
    
    # tell() - Current position
    position = file.tell()

# ============================================
# 8. CHECKING FILE EXISTENCE & PROPERTIES
# ============================================


# Check if file exists
if os.path.exists('sample.txt'):
    print('File exists')

# Get file size
size = os.path.getsize('sample.txt')

# Get absolute path
path = os.path.abspath('sample.txt')

# ============================================
# 9. DELETING FILES
# ============================================


# Delete a file
if os.path.exists('temp.txt'):
    os.remove('temp.txt')

# ============================================
# INTERVIEW Q&A
# ============================================

"""
Q1: What's the difference between read(), readline(), and readlines()?
A: 
- read(): Returns entire file as single string
- readline(): Returns one line as string
- readlines(): Returns list of all lines

Q2: Why use 'with' statement for files?
A: Automatically closes file, prevents resource leaks, cleaner code

Q3: What happens if we open file in 'w' mode?
A: File is created if not exists, overwritten if exists

Q4: Difference between 'w' and 'a' modes?
A: 'w' overwrites entire file, 'a' appends to end

Q5: How to read large files efficiently?
A: Read in chunks using a loop or chunk_size parameter

Q6: What are file modes?
A: 'r'=read, 'w'=write, 'a'=append, 'x'=create, 'b'=binary, 't'=text

Q7: How to handle file not found error?
A: Use try-except block with FileNotFoundError

Q8: Can we read binary files like images?
A: Yes, use 'rb' mode and handle as bytes

Q9: How to get current file position?
A: Use file.tell() method

Q10: What's the difference between 'newline' parameter?
A: Controls how newlines are handled (important for CSV files)
"""

# ============================================
# ERROR HANDLING EXAMPLE
# ============================================

try:
    with open('nonexistent.txt', 'r') as file:
        content = file.read()
except FileNotFoundError:
    print('File not found!')
except IOError:
    print('Error reading file!')

    # Create sample files for demonstration
    with open('sample.txt', 'w') as f:
        f.write('Line 1: Introduction to file operations\n')
        f.write('Line 2: Python makes file handling easy\n')
        f.write('Line 3: Using context managers is best practice\n')

    # Read and print the created file
    print("=== Reading sample.txt ===")
    with open('sample.txt', 'r') as f:
        print(f.read())

    # Create and read CSV
    with open('data.csv', 'w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['Name', 'Age', 'City'])
        csv_writer.writerow(['Alice', '25', 'NYC'])
        csv_writer.writerow(['Bob', '30', 'LA'])

    print("=== Reading data.csv ===")
    with open('data.csv', 'r') as f:
        for row in csv.reader(f):
            print(row)

    # Create and read JSON
    data = {'name': 'John', 'age': 28, 'city': 'Chicago'}
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=2)

    print("\n=== Reading data.json ===")
    with open('data.json', 'r') as f:
        loaded_data = json.load(f)
        print(loaded_data)
        # Search for lines matching a pattern
        print("\n=== Searching for pattern in file ===")
        with open('sample.txt', 'r') as f:
            lines = f.readlines()
            pattern = 'file'
            
            print(f"Lines containing '{pattern}':")
            for line in lines:
                print(line) #output each line
                if pattern.lower() in line.lower(): #case-insensitive search
                    print(f"  Found: {line.strip()}") #output: Found: Line 3: Using context managers is best practice