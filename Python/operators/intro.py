# Arithmetic Operators
a = 10
b = 3

print("Arithmetic Operators:")
print("Addition:", a + b)          # Output: 13
print("Subtraction:", a - b)       # Output: 7
print("Multiplication:", a * b)    # Output: 30
print("Division:", a / b)          # Output: 3.3333...
print("Floor Division:", a // b)   # Output: 3
print("Modulus:", a % b)           # Output: 1
print("Exponentiation:", a ** b)   # Output: 1000

# Comparison Operators
print("\nComparison Operators:")
print("Equal:", a == b)            # Output: False
print("Not Equal:", a != b)        # Output: True
print("Greater than:", a > b)      # Output: True
print("Less than:", a < b)         # Output: False
print("Greater than or Equal:", a >= b)  # Output: True
print("Less than or Equal:", a <= b)     # Output: False

# Logical Operators
print("\nLogical Operators:")
x = True
y = False
print("AND:", x and y)             # Output: False
print("OR:", x or y)               # Output: True
print("NOT:", not x)                # Output: False

# Bitwise Operators
print("\nBitwise Operators:")
print("Bitwise AND:", a & b)       # Output: 2
print("Bitwise OR:", a | b)        # Output: 11
print("Bitwise XOR:", a ^ b)       # Output: 9
print("Bitwise NOT:", ~a)          # Output: -11
print("Left Shift:", a << 1)       # Output: 20
print("Right Shift:", a >> 1)      # Output: 5

# Assignment Operators
print("\nAssignment Operators:")
c = 5
print("Initial value of c:", c)    # Output: 5
c += 2
print("After c += 2:", c)          # Output: 7
c *= 3
print("After c *= 3:", c)          # Output: 21

# Identity Operators
print("\nIdentity Operators:")
list1 = [1, 2, 3]
list2 = list1
list3 = list1[:]
print("list1 is list2:", list1 is list2)  # Output: True
print("list1 is list3:", list1 is list3)  # Output: False

# Membership Operators
print("\nMembership Operators:")
print("1 in list1:", 1 in list1)    # Output: True
print("4 not in list1:", 4 not in list1)  # Output: True