import numpy as np

# RANGE IN PYTHON - COMPREHENSIVE GUIDE

# 1. BASIC SYNTAX
# range(stop)
# range(start, stop)
# range(start, stop, step)

print("=" * 50)
print("1. RANGE WITH SINGLE ARGUMENT (stop)")
print("=" * 50)
for i in range(5):
    print(i, end=" ")
print("\n")  # Output: 0 1 2 3 4

print("=" * 50)
print("2. RANGE WITH TWO ARGUMENTS (start, stop)")
print("=" * 50)
for i in range(2, 7):
    print(i, end=" ")
print("\n")  # Output: 2 3 4 5 6

print("=" * 50)
print("3. RANGE WITH THREE ARGUMENTS (start, stop, step)")
print("=" * 50)
for i in range(0, 10, 2):
    print(i, end=" ")
print("\n")  # Output: 0 2 4 6 8

print("=" * 50)
print("4. NEGATIVE STEP (REVERSE)")
print("=" * 50)
for i in range(10, 0, -1):
    print(i, end=" ")
print("\n")  # Output: 10 9 8 7 6 5 4 3 2 1

print("=" * 50)
print("5. CONVERTING RANGE TO LIST")
print("=" * 50)
print(list(range(5)))  # Output: [0, 1, 2, 3, 4]

print("=" * 50)
print("6. RANGE WITH FLOAT (NOT ALLOWED - USE NUMPY)")
print("=" * 50)
# range(0.5, 5.5)  # TypeError: 'float' object cannot be interpreted as an integer
print(list(np.arange(0.5, 5.5, 0.5)))  # Output: [0.5, 1. , 1.5, 2. , 2.5, 3. , 3.5, 4. , 4.5, 5. ]

print("=" * 50)
print("7. EMPTY RANGE")
print("=" * 50)
print(list(range(5, 5)))  # Output: []
print(list(range(5, 2)))  # Output: []

print("=" * 50)
print("8. ACCESSING RANGE ELEMENTS (INDEXING)")
print("=" * 50)
r = range(10, 20, 2)
print(f"range object: {r}")
print(f"First element: {r[0]}")  # Output: 10
print(f"Last element: {r[-1]}")  # Output: 18
print(f"Middle element: {r[2]}")  # Output: 14

print("=" * 50)
print("9. MEMORY EFFICIENCY")
print("=" * 50)
r = range(1000000)
print(f"Size of range object: {r.__sizeof__()} bytes")  # Much smaller than list
l = list(range(1000000))
print(f"Size of list object: {l.__sizeof__()} bytes")  # Much larger

print("=" * 50)
print("10. CHECKING MEMBERSHIP")
print("=" * 50)
r = range(1, 10)
print(5 in r)  # Output: True
print(15 in r)  # Output: False
