# ============================================
# 1. IF CONDITIONAL STATEMENTS
# ============================================

# Basic if statement
age = 18
if age >= 18:
    print("You are an adult")

# if-else statement
score = 45
if score >= 50:
    print("Pass")
else:
    print("Fail")

# if-elif-else statement
marks = 85
if marks >= 90:
    print("Grade: A")
elif marks >= 80:
    print("Grade: B")
elif marks >= 70:
    print("Grade: C")
else:
    print("Grade: F")

# Nested if statements
username = "admin"
password = "1234"
if username == "admin":
    if password == "1234":
        print("Login successful")
    else:
        print("Wrong password")
else:
    print("User not found")

# Multiple conditions with and/or
age = 25
income = 50000
if age >= 18 and income >= 30000:
    print("Eligible for loan")

# Not operator
is_student = False
if not is_student:
    print("You need to pay full price")


# ============================================
# 2. TERNARY OPERATOR (Conditional Expression)
# ============================================

# Basic ternary syntax: value_if_true if condition else value_if_false
age = 20
status = "Adult" if age >= 18 else "Minor"
print(f"Status: {status}")

# Ternary with variables
num = 10
result = "Even" if num % 2 == 0 else "Odd"
print(f"Number is: {result}")

# Nested ternary operator
score = 75
grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "F"
print(f"Grade: {grade}")

# Ternary in list/dictionary
numbers = [1, 2, 3, 4, 5]
result = ["even" if x % 2 == 0 else "odd" for x in numbers]
print(f"List classification: {result}")


# ============================================
# 3. INTERVIEW QUESTIONS & ANSWERS
# ============================================

"""
Q1: What's the difference between = and == ?
A: = is assignment, == is comparison
   x = 5 (assigns 5 to x)
   x == 5 (checks if x equals 5, returns True/False)

Q2: Can you use multiple conditions in if statement?
A: Yes, using 'and', 'or', 'not' operators
   if x > 5 and y < 10:
   if x == 5 or y == 5:

Q3: What is a ternary operator?
A: One-line conditional expression for simple if-else
   value = "yes" if condition else "no"

Q4: What's the difference between if-elif-else and nested if?
A: if-elif checks multiple conditions mutually exclusively
   nested if allows checking conditions within conditions
   
Q5: Can ternary operators be nested?
A: Yes, but readability decreases with nesting
   value = "a" if x > 5 else "b" if x > 2 else "c"
"""

# Practice Examples
print("\n=== PRACTICE EXAMPLES ===")
# Example 1: Check even/odd using ternary
num = 7
print(f"{num} is {'even' if num % 2 == 0 else 'odd'}")

# Example 2: Discount calculation
purchase = 500
discount = 20 if purchase > 1000 else 10 if purchase > 500 else 0
print(f"Discount: {discount}%")

# Example 3: Temperature check
temp = 25
message = "Hot" if temp > 30 else "Warm" if temp > 20 else "Cold"
print(f"Weather: {message}")