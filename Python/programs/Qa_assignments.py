# Addition of two numbers using lambda function
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))
addition = lambda a,b: a+b
print(addition(1,3))

# Even or Odd
a = int(input("Enter the number: "))
output = "Even" if a % 2 == 0 else 'Odd'
print(output)


 #Find the largest among three numbers   
a,b,c = map(int, input("Enter 3 numbers: ").split())
print(a,b,c)

if a>=b and a>=c:
    print(f'{a} is largest')
elif b>=a and b>=c:
    print(f'{b} is largest')
else:
    print(f'{c} is largest')

#taking multiple inputs using list comprehension
# numbers = [int(x) for x in input("Enter numbers: ").split()[:3]]
# print(numbers)

# Print numbers from 1 to N
N = int(input("Enter the number: "))

for i in range(1, N+1):
    print(i, end=" ")


# Sum of first N natural numbers
n = int(input("Enter the number: "))

sum = n * (n+1)//2
print(sum)


#different ways to find sum of first N natural numbers
n = int(input("Enter the number: "))

# Method 1: Using a loop
sum_loop = 0
for i in range(1, n+1):
    sum_loop += i
print("Sum using loop:", sum_loop)

# Method 2: Using the formula (already implemented above)
print("Sum using formula:", n * (n+1)//2)

# Method 3: Using recursion
def sum_recursive(n):
    if n == 0:
        return 0
    return n + sum_recursive(n-1)
print("Sum using recursion:", sum_recursive(n))


# Count vowels in a string
name = input("Enter a string: ")
vowel_count = 0

for i in name:
    if i in "aeiou":
        vowel_count += 1
print(vowel_count)


# Check Pallindrome
name = input("Enter the name: ")

if name == name[::-1]:
    print("Pallindrome")
else:
    print("Not a pallindrome")


# Find the largest number in a list
list1 = [int(x) for x in input("Enter the numbers: ").split()]
max = list1[0]

for i in list1:
    if i>max:
        max = i
print(f'Maximum number is {max}')



# Remove duplicates from a list by keeping the order
list1 = [int(x) for x in input("Enter the numbers: ").split()]

new_list = []
new_set = set()

for i in list1:
    if i not in new_set:
        new_list.append(i)
        new_set.add(i)
print(new_list)


# Print a right angle triangle pattern
n = int(input("Enter the number: "))
for i in range(1,n+1):
    print('*' * i)