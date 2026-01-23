"""
SECTIONS COVERED:
1. Basic For Loop Syntax - Introduction to for loop structure
2. For Loop with range() - Iterating using range() function with different parameters
3. For Loop with Strings - Character-by-character iteration
4. For Loop with enumerate() - Getting both index and value simultaneously
5. For Loop with Dictionaries - Iterating through keys, values, and key-value pairs
6. Nested For Loops - Loops within loops for multi-dimensional iteration
7. Break and Continue - Control flow statements to exit or skip iterations
8. For-Else Loop - Else block execution when loop completes without break
9. List Comprehension - Pythonic alternative to traditional for loops
10. Practical Examples - Real-world use cases of for loops
11. Interview Questions and Answers - Common Q&A for technical interviews
ENUMERATE FUNCTION DETAILS:
===========================
enumerate() is a built-in function that provides both the index and value when 
iterating over a sequence. It's particularly useful when you need to track the 
position of each element.
Syntax: enumerate(iterable, start=0)
- iterable: The sequence to iterate over
- start: Starting index (default is 0)
Returns: An enumerate object that yields (index, value) tuples
Use Cases:
- When you need element position and value together
- Avoiding manual counter variables in loops
- Adding line numbers to file processing
- Creating indexed data structures during iteration
Performance: enumerate() is more efficient than using range(len()) because it 
doesn't create an intermediate list of indices.
Key Features:
- Works with any iterable (lists, tuples, strings, dictionaries, sets, etc.)
- Can customize starting index with the 'start' parameter
- Returns tuples that can be unpacked for cleaner code
- Eliminates the need for manual counter variables
FOR LOOP IN PYTHON - COMPLETE GUIDE
====================================
A for loop is used to iterate over a sequence (list, tuple, string, dict, set, range)
and execute a block of code for each item.
"""

# ============================================================================
# 1. BASIC FOR LOOP SYNTAX
# ============================================================================

print("=" * 50)
print("1. BASIC FOR LOOP")
print("=" * 50)

# Syntax: for variable in sequence:
#            code block

# Example 1: Loop through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Output:
# apple
# banana
# cherry

print("\n")

# ============================================================================
# 2. FOR LOOP WITH RANGE()
# ============================================================================

print("=" * 50)
print("2. FOR LOOP WITH RANGE()")
print("=" * 50)

# range(start, stop, step)
for i in range(5):  # 0 to 4
    print(f"Number: {i}")

print("\n")

# Range with start and stop
for i in range(1, 6):  # 1 to 5
    print(f"Count: {i}")

print("\n")

# Range with step
for i in range(0, 10, 2):  # 0, 2, 4, 6, 8
    print(f"Even: {i}")

print("\n")

# ============================================================================
# 3. FOR LOOP WITH STRINGS
# ============================================================================

print("=" * 50)
print("3. FOR LOOP WITH STRINGS")
print("=" * 50)

word = "Python"
for char in word:
    print(char)

# Output:
# P
# y
# t
# h
# o
# n

print("\n")

# ============================================================================
# 4. FOR LOOP WITH ENUMERATE()
# ============================================================================

print("=" * 50)
print("4. FOR LOOP WITH ENUMERATE()")
print("=" * 50)

# Get both index and value
colors = ["red", "green", "blue"]
for index, color in enumerate(colors):
    print(f"Index {index}: {color}")

# Output:
# Index 0: red
# Index 1: green
# Index 2: blue

print("\n")

# ============================================================================
# 5. FOR LOOP WITH DICTIONARIES
# ============================================================================

print("=" * 50)
print("5. FOR LOOP WITH DICTIONARIES")
print("=" * 50)

student = {"name": "John", "age": 20, "grade": "A"}

# Loop through keys
for key in student:
    print(f"{key}: {student[key]}")

print("\n")

# Loop through key-value pairs
for key, value in student.items():
    print(f"{key} = {value}")

print("\n")

# ============================================================================
# 6. NESTED FOR LOOPS
# ============================================================================

print("=" * 50)
print("6. NESTED FOR LOOPS")
print("=" * 50)

for i in range(1, 4):
    for j in range(1, 4):
        print(f"({i}, {j})", end=" ")
    print()

# Output:
# (1, 1) (1, 2) (1, 3)
# (2, 1) (2, 2) (2, 3)
# (3, 1) (3, 2) (3, 3)

print("\n")

# ============================================================================
# 7. BREAK AND CONTINUE
# ============================================================================

print("=" * 50)
print("7. BREAK AND CONTINUE")
print("=" * 50)

# BREAK - exits the loop
print("Break Example:")
for i in range(5):
    if i == 3:
        break
    print(i)

# Output: 0, 1, 2

print("\n")

# CONTINUE - skips current iteration
print("Continue Example:")
for i in range(5):
    if i == 2:
        continue
    print(i)

# Output: 0, 1, 3, 4

print("\n")

# ============================================================================
# 8. FOR-ELSE LOOP
# ============================================================================

print("=" * 50)
print("8. FOR-ELSE LOOP")
print("=" * 50)

# Else block executes when loop completes without break
for i in range(3):
    print(i)
else:
    print("Loop completed successfully!")

# Output:
# 0
# 1
# 2
# Loop completed successfully!

print("\n")

# Else doesn't execute if break is used
for i in range(5):
    if i == 2:
        break
    print(i)
else:
    print("This won't print")

# Output: 0, 1

print("\n")

# ============================================================================
# 9. LIST COMPREHENSION (Alternative to for loop)
# ============================================================================

print("=" * 50)
print("9. LIST COMPREHENSION")
print("=" * 50)

# Traditional for loop
squares = []
for x in range(5):
    squares.append(x ** 2)
print(f"Traditional: {squares}")

# List comprehension
squares = [x ** 2 for x in range(5)]
print(f"List Comprehension: {squares}")

# With condition
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
print(f"Even Squares: {even_squares}")

print("\n")

# ============================================================================
# 10. PRACTICAL EXAMPLES
# ============================================================================

print("=" * 50)
print("10. PRACTICAL EXAMPLES")
print("=" * 50)

# Example 1: Sum of numbers
total = 0
for num in [1, 2, 3, 4, 5]:
    total += num
print(f"Sum: {total}")  # Output: 15

# Example 2: Count occurrences
word = "hello"
count = 0
for char in word:
    if char == 'l':
        count += 1
print(f"'l' appears {count} times")  # Output: 2

# Example 3: Find maximum
numbers = [45, 23, 67, 12, 89, 34]
max_num = numbers[0]
for num in numbers:
    if num > max_num:
        max_num = num
print(f"Maximum: {max_num}")  # Output: 89

print("\n")

# ============================================================================
# INTERVIEW QUESTIONS AND ANSWERS
# ============================================================================

interview_qa = """
╔════════════════════════════════════════════════════════════════════════════╗
║                 FOR LOOP - INTERVIEW QUESTIONS & ANSWERS                  ║
╚════════════════════════════════════════════════════════════════════════════╝

Q1: What is a for loop and why is it used?
A:  A for loop is used to iterate over a sequence (list, tuple, string, etc.)
    and execute a block of code for each item. It's used to avoid repetitive code.

Q2: What is the difference between for and while loops?
A:  - for loop: Iterates over a sequence (predefined number of iterations)
    - while loop: Iterates based on a condition (indefinite iterations)

Q3: What is enumerate() and when to use it?
A:  enumerate() returns both index and value. Use it when you need the position
    of an item in the sequence.
    Example: for index, value in enumerate(list):

Q4: Explain the difference between break and continue.
A:  - break: Exits the loop immediately
    - continue: Skips the current iteration and continues with the next one

Q5: What is a nested for loop?
A:  A for loop inside another for loop. Used for iterating through 2D structures
    like matrices, or creating combinations.

Q6: What is the for-else statement?
A:  The else block executes when the loop completes normally (without break).
    If break is used, the else block is skipped.

Q7: How is list comprehension better than a for loop?
A:  - More concise and readable
    - Generally faster execution
    - Creates lists in a single line
    Example: [x**2 for x in range(5)]

Q8: Can you loop backwards in Python?
A:  Yes, using:
    - reversed(): for item in reversed(list)
    - negative step: for item in range(10, 0, -1)
    - slice: for item in list[::-1]

Q9: What happens if you modify a list while looping through it?
A:  It's dangerous and can cause unexpected behavior. Always loop through a copy
    or use list comprehension instead.

Q10: Explain the zip() function with for loop.
A:   zip() combines multiple sequences. Example:
     for x, y in zip(list1, list2):
     Iterates through two lists simultaneously.

Q11: What is the pass statement in a for loop?
A:   pass is a placeholder that does nothing. Used when a statement is required
     but you don't want to execute code.
     Example:
     for i in range(5):
         pass

Q12: How do you loop through a dictionary?
A:   - for key in dict: (iterates through keys)
     - for key, value in dict.items(): (iterates through key-value pairs)
     - for value in dict.values(): (iterates through values)

Q13: Can you use else with while loop?
A:   Yes, the else clause works with both for and while loops in Python.

Q14: What's the difference between range(5) and range(0, 5)?
A:   They are identical. range(5) implies starting from 0 by default.

Q15: How to iterate through nested lists?
A:   Use nested for loops:
     for sublist in nested_list:
         for item in sublist:
             print(item)
"""

print(interview_qa)

# ============================================================================
# ADDITIONAL BREAK AND CONTINUE EXAMPLES WITH OUTPUT
# ============================================================================

print("=" * 50)
print("BREAK AND CONTINUE - DETAILED EXAMPLES")
print("=" * 50)

# Example 1: Break - Exit loop when condition is met
print("\nExample 1: Break - Find first number divisible by 7")
for num in range(1, 20):
    if num % 7 == 0:
        print(f"Found: {num}")
        break
    print(num, end=" ")
print("\n(Loop stopped at 7)")# Output: 1 2 3 4 5 6 Found: 7

# Example 2: Continue - Skip even numbers
print("\nExample 2: Continue - Print only odd numbers")
for num in range(1, 11):
    if num % 2 == 0:
        continue
    print(num, end=" ")
print("\n(Skipped all even numbers)") # Output: 1 3 5 7 9

# Example 3: Break with nested loop
print("\nExample 3: Break - Exit nested loop")
for i in range(1, 4):
    for j in range(1, 4):
        if i == 2 and j == 2:
            print("Break!")
            break
        print(f"({i},{j})", end=" ")
    print()

# Example 4: Continue with string iteration
print("\nExample 4: Continue - Skip vowels")
word = "python"
for char in word:
    if char in "aeiou":
        continue
    print(char, end=" ")
print("\n(Skipped all vowels)")

# Example 5: Break to search in list
print("\nExample 5: Break - Search for target item")
shopping_list = ["apple", "banana", "orange", "grape", "mango"]
target = "orange"
for item in shopping_list:
    print(f"Checking: {item}")
    if item == target:
        print(f"Found {target}!")
        break
else:
    print(f"{target} not found")

# Example 6: Continue to filter data
print("\nExample 6: Continue - Process only valid entries")
scores = [45, 0, 78, -5, 92, 0, 88]
for score in scores:
    if score == 0:
        continue
    if score >= 70:
        print(f"Passed: {score}")
    else:
        print(f"Failed: {score}")