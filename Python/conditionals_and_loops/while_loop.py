# ===== BASIC WHILE LOOP =====
# Syntax: while condition:
#             statement(s)

# Example 1: Simple counter
print("=== Example 1: Simple Counter ===")
i = 1
while i <= 5:
    print(i)
    i += 1
# Output: 1 2 3 4 5

# Example 2: While with else
print("\n=== Example 2: While with Else ===")
count = 0
while count < 3:
    print(f"Count: {count}")
    count += 1
else:
    print("Loop completed!")
# Output: Count: 0, Count: 1, Count: 2, Loop completed!

# Example 3: Break statement
print("\n=== Example 3: Break ===")
i = 0
while i < 10:
    if i == 5:
        break
    print(i)
    i += 1
# Output: 0 1 2 3 4

# Example 4: Continue statement
print("\n=== Example 4: Continue ===")
i = 0
while i < 5:
    i += 1
    if i == 3:
        continue
    print(i)
# Output: 1 2 4 5

# ===== INTERVIEW PROGRAMS =====

# Interview Q1: Sum of n natural numbers
print("\n=== Interview Q1: Sum of n Natural Numbers ===")
n = 5
sum_n = 0
i = 1
while i <= n:
    sum_n += i
    i += 1
print(f"Sum of {n} natural numbers: {sum_n}")
# Output: 15

# Interview Q2: Factorial
print("\n=== Interview Q2: Factorial ===")
num = 5
factorial = 1
i = 1
while i <= num:
    factorial *= i
    i += 1
print(f"Factorial of {num}: {factorial}")
# Output: 120

# Interview Q3: Reverse a number
print("\n=== Interview Q3: Reverse a Number ===")
num = 12345
reversed_num = 0
while num > 0:
    digit = num % 10
    reversed_num = reversed_num * 10 + digit
    num //= 10
print(f"Reversed number: {reversed_num}")
# Output: 54321

# Interview Q4: Check Armstrong number
print("\n=== Interview Q4: Armstrong Number ===")
num = 153
original = num
sum_cubes = 0
while num > 0:
    digit = num % 10
    sum_cubes += digit ** 3
    num //= 10
print(f"{original} is Armstrong: {original == sum_cubes}")
# Output: True

# Interview Q5: Count digits
print("\n=== Interview Q5: Count Digits ===")
num = 9876
count = 0
while num > 0:
    count += 1
    num //= 10
print(f"Number of digits: {count}")
# Output: 4

# Interview Q6: Fibonacci series
print("\n=== Interview Q6: Fibonacci Series ===")
n = 7
a, b = 0, 1
i = 0
while i < n:
    print(a, end=" ")
    a, b = b, a + b
    i += 1
# Output: 0 1 1 2 3 5 8

# Interview Q7: Prime number check
print("\n\n=== Interview Q7: Prime Number Check ===")
num = 17
is_prime = True
i = 2
while i * i <= num:
    if num % i == 0:
        is_prime = False
        break
    i += 1
print(f"{num} is Prime: {is_prime}")
# Output: True

# Interview Q8: Password validation (infinite loop with break)
print("\n=== Interview Q8: Password Validation ===")
correct_password = "python123"
attempts = 0
while True:
    if attempts >= 3:
        print("Too many attempts. Access denied!")
        break
    password = input("Enter password: ") if False else "python123"  # Simulated input
    if password == correct_password:
        print("Access granted!")
        break
    else:
        attempts += 1
        print(f"Wrong password. Attempts left: {3 - attempts}")