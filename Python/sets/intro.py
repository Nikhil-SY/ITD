# Sets: Unordered collections of unique elements
'''

Sets Module - Comprehensive Docstring
OVERVIEW:
=========
Python sets are unordered collections of unique elements that are mutable but do not support indexing.
They automatically eliminate duplicate values and are optimized for membership testing with O(1) average time complexity.
KEY CHARACTERISTICS:
====================
- Unordered: Elements have no guaranteed order or index position
- Unique: Duplicate elements are automatically removed upon creation or addition
- Mutable: Sets can be modified after creation through various methods
- No Indexing: Cannot access elements using index notation (e.g., set[0] is invalid)
- Hashable Elements: Can only contain immutable types (int, str, tuple, frozenset, etc.)
CREATION METHODS:
=================
1. Literal Syntax:
    - {1, 2, 3}: Direct set creation with elements
    - Note: {} creates an empty dict, not an empty set
2. set() Constructor:
    - set(): Creates an empty set
    - set([1, 2, 2, 3]): Creates a set from an iterable, automatically removing duplicates
    - set("abc"): Creates a set from a string: {'a', 'b', 'c'}
3. Set Comprehension:
    - {x for x in range(5)}: Creates a set using comprehension syntax
    - {x for x in range(10) if x % 2 == 0}: With conditional filtering
SET OPERATIONS (Mathematical Set Theory):
==========================================
1. Union (|):
    - Syntax: set_a | set_b or set_a.union(set_b)
    - Returns: All elements from both sets (combined)
    - Example: {1, 2, 3} | {3, 4, 5} = {1, 2, 3, 4, 5}
2. Intersection (&):
    - Syntax: set_a & set_b or set_a.intersection(set_b)
    - Returns: Only common elements present in both sets
    - Example: {1, 2, 3} & {3, 4, 5} = {3}
3. Difference (-):
    - Syntax: set_a - set_b or set_a.difference(set_b)
    - Returns: Elements in set_a that are NOT in set_b
    - Example: {1, 2, 3} - {3, 4, 5} = {1, 2}
4. Symmetric Difference (^):
    - Syntax: set_a ^ set_b or set_a.symmetric_difference(set_b)
    - Returns: Elements in either set but NOT in both (XOR operation)
    - Example: {1, 2, 3} ^ {3, 4, 5} = {1, 2, 4, 5}
MUTATING VS. NON-MUTATING OPERATIONS:
======================================
Each set operation has two variants:
1. Non-Mutating (Operator or Method):
    - union(): Returns new set, original unchanged
    - intersection(): Returns new set, original unchanged
    - difference(): Returns new set, original unchanged
    - symmetric_difference(): Returns new set, original unchanged
2. Mutating (In-place _update variants):
    - update(): Modifies original set with union of all elements
      Syntax: set_a.update(set_b)
      Effect: set_a now contains all elements from both sets
    - intersection_update(): Modifies original set to keep only common elements
      Syntax: set_a.intersection_update(set_b)
      Effect: set_a now contains only elements also in set_b
    - difference_update(): Modifies original set by removing elements found in other set
      Syntax: set_a.difference_update(set_b)
      Effect: set_a now removes all elements that appear in set_b
    - symmetric_difference_update(): Modifies original set to keep only unique elements
      Syntax: set_a.symmetric_difference_update(set_b)
      Effect: set_a keeps only elements that are in one set or the other, but not both
ADDING AND REMOVING ELEMENTS:
==============================
1. add(element):
    - Adds a single element to the set
    - If element already exists, set remains unchanged (no duplicates)
    - Raises TypeError if element is unhashable
    - Example: s.add(4)
2. update(iterable) [Mutating Operation]:
    - Adds multiple elements from an iterable (list, tuple, set, string, etc.)
    - Elements are added individually from the iterable
    - Similar to calling add() multiple times in a loop
    - Example: s.update([5, 6, 7]) or s.update("abc")
    - Note: update() is the non-symmetric variant of union(); union() returns a new set
3. remove(element):
    - Removes specified element from the set
    - Raises KeyError if element does not exist (strict behavior)
    - Use when you are certain the element exists
    - Example: s.remove(3)
4. discard(element):
    - Removes specified element from the set if it exists
    - Does NOT raise an error if element is absent (lenient behavior)
    - Silently does nothing if element not found
    - Use when unsure if element exists
    - Example: s.discard(10)
5. pop():
    - Removes and returns an arbitrary element from the set
    - Sets are unordered, so which element is removed is unpredictable
    - Raises KeyError if the set is empty
    - Example: removed_element = s.pop()
CRITICAL DIFFERENCE: remove() vs discard()
===========================================
remove():
  - Behavior: Strict - raises KeyError if element not found
  - Use Case: When you expect the element to exist; want to catch errors
  - Safety: Fails loudly, helping catch bugs
discard():
  - Behavior: Lenient - does nothing if element not found
  - Use Case: When unsure if element exists; want safe removal
  - Safety: Fails silently, preventing exceptions
SUBSET AND SUPERSET METHODS:
=============================
1. issubset(other):
    - Returns True if all elements of the set are in the other set
    - Syntax: set_a.issubset(set_b) or set_a <= set_b
    - Example: {1, 2}.issubset({1, 2, 3}) = True
2. issuperset(other):
    - Returns True if the set contains all elements of the other set
    - Syntax: set_a.issuperset(set_b) or set_a >= set_b
    - Example: {1, 2, 3}.issuperset({1, 2}) = True
3. isdisjoint(other):
    - Returns True if the two sets have NO common elements
    - Syntax: set_a.isdisjoint(set_b)
    - Example: {1, 2}.isdisjoint({3, 4}) = True
MEMBERSHIP TESTING:
===================
- Operator: in or not in
- Time Complexity: O(1) average case (much faster than lists which are O(n))
- Usage: element in my_set
- Advantage: Sets are optimized for membership testing, making them ideal for checking existence
ITERATION:
==========
- Each iteration may yield elements in different orders
- Useful for applying operations to all elements in a set
- Example: for item in my_set: print(item)
PRACTICAL USE CASES:
====================
1. Removing Duplicates:
    - Convert list to set: unique_items = list(set(original_list))
    - Automatically eliminates duplicate values
    - Note: Order may not be preserved
2. Fast Membership Testing:
    - Check if element exists: if element in my_set (O(1) vs O(n) for lists)
3. Mathematical Set Operations:
    - Union, intersection, difference for data analysis
    - Finding common elements between datasets
4. Data Deduplication and Cleaning:
    - Remove redundant entries from collections
    - Ensure uniqueness constraints
5. Tracking Unique Values:
    - Monitor distinct items seen in a stream
    - Count unique elements efficiently
IMMUTABILITY NOTE:
==================
While sets themselves are mutable (elements can be added/removed), they cannot contain mutable objects.
Use frozenset for an immutable set variant that can be stored in sets or used as dictionary keys.
'''


"""
Module: Python Sets - Comprehensive Guide
This module demonstrates Python sets, which are unordered collections of unique elements.
Sets are mutable, do not support indexing, and automatically eliminate duplicate values.
Key Characteristics:
- Unordered: Elements have no guaranteed order
- Unique: Duplicates are automatically removed
- Mutable: Can be modified after creation
- No Indexing: Cannot access elements by index
Functions/Operations Covered:
1. Creating Sets:
    - Literal syntax: {1, 2, 3}
    - set() constructor from iterables
    - Empty set creation: set() (not {})
2. Set Operations:
    - Union (|): Combines all elements from both sets
    - Intersection (&): Returns only common elements
    - Difference (-): Returns elements in first set but not in second
    - Symmetric Difference (^): Returns elements in either set but not in both
3. Adding/Removing Elements:
    - add(element): Adds a single element
    - update(iterable): Adds multiple elements from an iterable
    - remove(element): Removes element; raises KeyError if not found
    - discard(element): Removes element if present; no error if absent
    DIFFERENCE between remove() and discard():
    - remove() raises KeyError if element doesn't exist
    - discard() silently does nothing if element doesn't exist
    - pop(): Removes and returns arbitrary element; raises KeyError if set is empty
4. Set Methods:
    - issubset(other): Checks if all elements of set are in other set
    - issuperset(other): Checks if set contains all elements of other set
    - isdisjoint(other): Checks if two sets have no common elements
5. Membership Testing:
    - in operator: O(1) average time complexity for checking membership
    - More efficient than lists for membership testing
6. Iteration:
    - Sets are iterable but order is not guaranteed
    - Useful for loop operations over all elements
7. Set Comprehension:
    - Concise syntax for creating sets from iterables
    - Supports conditional filtering with if clauses
8. Practical Use Cases:
    - Removing duplicates from lists/sequences
    - Performing mathematical set operations
    - Fast membership testing
    - Deduplication and data cleaning
"""
# Key characteristics: Mutable, unordered, no duplicates, no indexing

# 1. Creating Sets
print("=== Creating Sets ===")
# === Creating Sets ===
my_set = {1, 2, 3, 4, 5}
print(f"Set: {my_set}")
# Set: {1, 2, 3, 4, 5}

# Empty set (not {}, which creates a dict)
empty_set = set()
print(f"Empty set: {empty_set}")
# Empty set: set()

# From a list (removes duplicates)
from_list = set([1, 2, 2, 3, 3, 3])
print(f"From list [1, 2, 2, 3, 3, 3]: {from_list}")
# From list [1, 2, 2, 3, 3, 3]: {1, 2, 3}

# 2. Set Operations
print("\n=== Set Operations ===")
# === Set Operations ===
set_a = {1, 2, 3, 4}
set_b = {3, 4, 5, 6}

# Union
print(f"Union {set_a} | {set_b}: {set_a | set_b}")
# Union {1, 2, 3, 4} | {3, 4, 5, 6}: {1, 2, 3, 4, 5, 6}

# Intersection
print(f"Intersection {set_a} & {set_b}: {set_a & set_b}")
# Intersection {1, 2, 3, 4} & {3, 4, 5, 6}: {3, 4}

# Difference
print(f"Difference {set_a} - {set_b}: {set_a - set_b}")
# Difference {1, 2, 3, 4} - {3, 4, 5, 6}: {1, 2}

# Symmetric Difference
print(f"Symmetric Diff {set_a} ^ {set_b}: {set_a ^ set_b}")
# Symmetric Diff {1, 2, 3, 4} ^ {3, 4, 5, 6}: {1, 2, 5, 6}

# 3. Adding/Removing Elements
print("\n=== Adding/Removing Elements ===")
# === Adding/Removing Elements ===
s = {1, 2, 3}
s.add(4)
print(f"After add(4): {s}")
# After add(4): {1, 2, 3, 4}

s.update([5, 6])
print(f"After update([5, 6]): {s}")
# After update([5, 6]): {1, 2, 3, 4, 5, 6}, it adds elements one by one as for iterable, it is like using add multiple times

s.remove(3)
print(f"After remove(3): {s}")
# After remove(3): {1, 2, 4, 5, 6}

s.discard(10)  # No error if element doesn't exist
print(f"After discard(10): {s}")
# After discard(10): {1, 2, 4, 5, 6}

popped = s.pop()
print(f"Popped {popped}, set now: {s}")
# Popped 1, set now: {2, 4, 5, 6}

# 4. Set Methods
print("\n=== Set Methods ===")
# === Set Methods ===
set_x = {1, 2, 3}
set_y = {2, 3, 4}

print(f"set_x.issubset(set_y): {set_x.issubset(set_y)}")
# set_x.issubset(set_y): False

print(f"set_x.issuperset(set_y): {set_x.issuperset(set_y)}")
# set_x.issuperset(set_y): False

print(f"set_x.isdisjoint(set_y): {set_x.isdisjoint(set_y)}")
# set_x.isdisjoint(set_y): False

# 5. Membership Testing
print("\n=== Membership Testing ===")
# === Membership Testing ===
s = {1, 2, 3, 4, 5}
print(f"3 in {s}: {3 in s}")
# 3 in {1, 2, 3, 4, 5}: True

print(f"10 in {s}: {10 in s}")
# 10 in {1, 2, 3, 4, 5}: False

# 6. Iteration
print("\n=== Iteration ===")
# === Iteration ===
s = {'a', 'b', 'c'}
for item in s:
    print(f"  {item}")
#   a
#   b
#   c

# 7. Set Comprehension
print("\n=== Set Comprehension ===")
# === Set Comprehension ===
squares = {x**2 for x in range(5)}
print(f"Squares of 0-4: {squares}")
# Squares of 0-4: {0, 1, 4, 9, 16}

evens = {x for x in range(10) if x % 2 == 0}
print(f"Even numbers 0-9: {evens}")
# Even numbers 0-9: {0, 2, 4, 6, 8}

# 8. Practical Example: Remove Duplicates
print("\n=== Practical Use Case ===")
# === Practical Use Case ===
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique = list(set(numbers))
print(f"Original list: {numbers}")
# Original list: [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]

print(f"After removing duplicates: {unique}")
# After removing duplicates: [1, 2, 3, 4]

odd = {1, 3, 5, 7, 9}
prime = {2, 3, 5, 7}
odd.intersection_update(prime)   # Modifying odd to keep only primes
print(f"Odd numbers after intersection_update with primes: {odd}") # Output: {3, 5, 7}