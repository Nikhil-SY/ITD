# Python Dictionaries - Complete Guide with Examples

# ============================================
# 1. DICTIONARY BASICS
# ============================================

# Creating dictionaries
student = {"name": "John", "age": 20, "grade": "A"}
print("Dictionary:", student)
# Output: Dictionary: {'name': 'John', 'age': 20, 'grade': 'A'}

# Empty dictionary
empty_dict = {}
print("Empty dict:", empty_dict)
# Output: Empty dict: {}

# Using dict() constructor
dict_construct = dict(name="Alice", age=25)
print("Using dict():", dict_construct)
# Output: Using dict(): {'name': 'Alice', 'age': 25}

# ============================================
# 2. ACCESSING DICTIONARY ELEMENTS
# ============================================

print("\n--- ACCESSING ELEMENTS ---")
print("Name:", student["name"])  # Direct access
# Output: Name: John

print("Age:", student.get("age"))  # Using get()
# Output: Age: 20

print("City:", student.get("city", "Not Found"))  # With default value
# Output: City: Not Found

# ============================================
# 3. DICTIONARY METHODS
# ============================================

print("\n--- DICTIONARY METHODS ---")

# keys() - Returns all keys
print("Keys:", student.keys())
# Output: Keys: dict_keys(['name', 'age', 'grade'])

# values() - Returns all values
print("Values:", student.values())
# Output: Values: dict_values(['John', 20, 'A'])

# items() - Returns key-value pairs
print("Items:", student.items())
# Output: Items: dict_items([('name', 'John'), ('age', 20), ('grade', 'A')])

# update() - Add/Update elements
student.update({"age": 21, "city": "NYC"})
print("After update:", student)
# Output: After update: {'name': 'John', 'age': 21, 'grade': 'A', 'city': 'NYC'}

# pop() - Remove and return value
age = student.pop("age")
print(f"Popped age: {age}, Remaining:", student)
# Output: Popped age: 21, Remaining: {...}

# popitem() - Remove last item
student.update({"age": 21})
last = student.popitem()
print(f"Popped item: {last}")
# Output: Popped item: ('city', 'NYC')

# clear() - Remove all elements
copy_student = student.copy()
copy_student.clear()
print("After clear:", copy_student)
# Output: After clear: {}

# setdefault() - Get with default
print("GPA:", student.setdefault("gpa", 3.8))
print("After setdefault:", student)
# Output: GPA: 3.8

# ============================================
# 4. DICTIONARY OPERATIONS
# ============================================

print("\n--- DICTIONARY OPERATIONS ---")

# Check if key exists
print("'name' in student:", "name" in student)
# Output: 'name' in student: True

# Iterate over dictionary
print("Iterating:")
for key in student:
    print(f"  {key}: {student[key]}")

# Iterate with items()
for key, value in student.items():
    print(f"  {key} = {value}")

# Length
print("Length:", len(student))
# Output: Length: 4

# ============================================
# 5. NESTED DICTIONARIES
# ============================================

print("\n--- NESTED DICTIONARIES ---")

company = {
    "name": "TechCorp",
    "employees": {
        "emp1": {"name": "John", "salary": 50000},
        "emp2": {"name": "Jane", "salary": 60000}
    }
}

print("Employee 1 name:", company["employees"]["emp1"]["name"])
# Output: Employee 1 name: John

# ============================================
# 6. DICTIONARY COMPREHENSION
# ============================================

print("\n--- DICTIONARY COMPREHENSION ---")

squares = {x: x**2 for x in range(1, 6)}
print("Squares:", squares)
# Output: Squares: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# ============================================
# INTERVIEW QUESTIONS & ANSWERS
# ============================================

"""
Q1: What is the difference between dict.pop() and dict.popitem()?
A: pop() removes a specific key and returns its value. 
   popitem() removes the last added key-value pair (arbitrary in Python <3.7).

Q2: Are dictionaries ordered?
A: Yes, in Python 3.7+, dictionaries maintain insertion order.

Q3: Can dictionary keys be mutable?
A: No, keys must be immutable (strings, numbers, tuples). Values can be mutable.

Q4: What's the difference between .get() and [] access?
A: get() returns None if key doesn't exist (with optional default).
   [] raises KeyError if key doesn't exist.

Q5: How to merge two dictionaries?
A: dict1.update(dict2) or {**dict1, **dict2} (Python 3.5+)

Q6: What is dict.copy()?
A: Creates a shallow copy of the dictionary.

Q7: How to check if a key exists?
A: Use 'key' in dict or dict.get(key) is not None

Q8: Can dictionaries have duplicate keys?
A: No, the last value overwrites previous ones with the same key.
"""

# ============================================
# 7. CONVERTING DATATYPES TO DICTIONARY
# ============================================

print("\n--- CONVERTING TO DICTIONARY ---")

# From list of tuples
list_of_tuples = [("name", "John"), ("age", 25), ("city", "NYC")]
dict_from_tuples = dict(list_of_tuples)
print("From list of tuples:", dict_from_tuples)
# Output: From list of tuples: {'name': 'John', 'age': 25, 'city': 'NYC'}

# From two separate lists using zip()
keys = ["name", "age", "city"]
values = ["Alice", 30, "Boston"]
dict_from_zip = dict(zip(keys, values))
print("From zip():", dict_from_zip)
# Output: From zip(): {'name': 'Alice', 'age': 30, 'city': 'Boston'}

# From list of lists
list_of_lists = [["id", 1], ["status", "active"]]
dict_from_lists = dict(list_of_lists)
print("From list of lists:", dict_from_lists)
# Output: From list of lists: {'id': 1, 'status': 'active'}

# ============================================
# 8. ZIP METHOD EXPLAINED
# ============================================

print("\n--- ZIP METHOD ---")

# Basic zip - pairs elements from multiple iterables
list1 = [1, 2, 3]
list2 = ["a", "b", "c"]
zipped = list(zip(list1, list2))
print("Zipped lists:", zipped)
# Output: Zipped lists: [(1, 'a'), (2, 'b'), (3, 'c')]

# Zip with unequal lengths (stops at shortest)
list3 = [10, 20, 30, 40]
list4 = ["x", "y"]
zipped_unequal = list(zip(list3, list4))
print("Zip unequal lengths:", zipped_unequal)
# Output: Zip unequal lengths: [(10, 'x'), (20, 'y')]

# Zip with multiple iterables
list5 = [1, 2, 3]
list6 = ["a", "b", "c"]
list7 = [10, 20, 30]
zipped_multi = list(zip(list5, list6, list7))
print("Zip multiple lists:", zipped_multi)
# Output: Zip multiple lists: [(1, 'a', 10), (2, 'b', 20), (3, 'c', 30)]

# Unzipping using zip
pairs = [(1, "a"), (2, "b"), (3, "c")]
numbers, letters = zip(*pairs)
print("Unzipped numbers:", numbers)
print("Unzipped letters:", letters)
# Output: Unzipped numbers: (1, 2, 3)
# Output: Unzipped letters: ('a', 'b', 'c')

# Practical example: Create dictionary from two lists
students_names = ["John", "Jane", "Jack"]
students_scores = [85, 90, 88]
scores_dict = dict(zip(students_names, students_scores))
print("Student scores:", scores_dict)
# Output: Student scores: {'John': 85, 'Jane': 90, 'Jack': 88}