# 1. Simple Number Pyramid
print("1. Number Pyramid")
n = 5
for i in range(1, n + 1):
    print(' ' * (n - i) + ' '.join(str(j) for j in range(1, i + 1)))

# Output:
#     1
#    1 2
#   1 2 3
#  1 2 3 4
# 1 2 3 4 5


# 2. Star Pyramid
print("\n2. Star Pyramid")
n = 5
for i in range(1, n + 1):
    print(' ' * (n - i) + '*' * (2 * i - 1))

# Output:
#     *
#    ***
#   *****
#  *******
# *********


# 3. Inverted Pyramid
print("\n3. Inverted Pyramid")
n = 5
for i in range(n, 0, -1):
    print(' ' * (n - i) + '*' * (2 * i - 1))

# Output:
# *********
#  *******
#   *****
#    ***
#     *


# 4. Diamond Pattern
print("\n4. Diamond Pattern")
n = 5
for i in range(1, n + 1):
    print(' ' * (n - i) + '*' * (2 * i - 1))
for i in range(n - 1, 0, -1):
    print(' ' * (n - i) + '*' * (2 * i - 1))

# Output:
#     *
#    ***
#   *****
#  *******
# *********
#  *******
#   *****
#    ***
#     *


# 5. Floyd's Triangle
print("\n5. Floyd's Triangle")
n = 5
num = 1
for i in range(1, n + 1):
    for j in range(i):
        print(num, end=' ')
        num += 1
    print()

# Output:
# 1
# 2 3
# 4 5 6
# 7 8 9 10
# 11 12 13 14 15


# 6. Alphabet Pyramid
print("\n6. Alphabet Pyramid")
n = 5
for i in range(n):
    for j in range(i + 1):
        print(chr(65 + j), end=' ')
    print()

# Output:
# A
# A B
# A B C
# A B C D
# A B C D E


# 7. Pascal's Triangle
print("\n7. Pascal's Triangle")
n = 6
for i in range(n):
    val = 1
    for j in range(i + 1):
        print(val, end=' ')
        val = val * (i - j) // (j + 1)
    print()

# Output:
# 1
# 1 1
# 1 2 1
# 1 3 3 1
# 1 4 6 4 1
# 1 5 10 10 5 1


# 8. Hollow Square
print("\n8. Hollow Square")
n = 5
for i in range(n):
    for j in range(n):
        if i == 0 or i == n - 1 or j == 0 or j == n - 1:
            print('*', end=' ')
        else:
            print(' ', end=' ')
    print()

# Output:
# * * * * *
# *       *
# *       *
# *       *
# * * * * *