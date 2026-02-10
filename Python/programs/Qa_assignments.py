#######################Part 1########################

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


#####################3 part 2########################

#First non-repeating character in a string
s = input("Enter string: ")

for i in range(len(s)):
    count = 0
    for j in range(len(s)):
        if s[i] == s[j]:
            count += 1
    if count == 1:
        print("First non-repeating character:", s[i])
        break

#Frequency of each word in a sentence
sentence = input("Enter sentence: ")
words = sentence.split()

visited = []

for word in words:
    if word not in visited:
        count = 0
        for w in words:
            if word == w:
                count += 1
        print(word, ":", count)
        visited.append(word)

#First and second largest number in a list
n = int(input("Enter number of elements: "))
arr = []

for i in range(n):
    arr.append(int(input()))

largest = arr[0]
second = arr[0]

for num in arr:
    if num > largest:
        second = largest
        largest = num
    elif num > second and num != largest:
        second = num

print("Largest:", largest)
print("Second Largest:", second)

#Check whether a number is prime
num = int(input("Enter number: "))

if num <= 1:
    print("Not Prime")
else:
    flag = True
    for i in range(2, num):
        if num % i == 0:
            flag = False
            break

    if flag:
        print("Prime")
    else:
        print("Not Prime")

#Common elements between two lists (without set)
n1 = int(input("Enter size of list1: "))
list1 = []
for i in range(n1):
    list1.append(int(input()))

n2 = int(input("Enter size of list2: "))
list2 = []
for i in range(n2):
    list2.append(int(input()))

print("Common elements:")
for i in list1:
    for j in list2:
        if i == j:
            print(i)
            break

#Reverse words without reversing characters
sentence = input("Enter sentence: ")
words = sentence.split()

for i in range(len(words)-1, -1, -1):
    print(words[i], end=" ")

#Reverse words AND characters
sentence = input("Enter sentence: ")
words = sentence.split()

for word in words[::-1]:
    rev = ""
    for ch in word:
        rev = ch + rev
    print(rev, end=" ")

#Missing number from 1 to n
n = int(input("Enter n: "))
arr = []

for i in range(n-1):
    arr.append(int(input()))

expected_sum = n * (n + 1) // 2
actual_sum = 0

for i in arr:
    actual_sum += i

print("Missing number:", expected_sum - actual_sum)

#Balanced parentheses
s = input("Enter brackets string: ")
count = 0

for ch in s:
    if ch == "(":
        count += 1
    elif ch == ")":
        count -= 1
    if count < 0:
        break

if count == 0:
    print("Balanced")
else:
    print("Not Balanced")

#Convert list of tuples into dictionary
n = int(input("Enter number of tuples: "))
d = {}

for i in range(n):
    key = input("Key: ")
    value = input("Value: ")
    d[key] = value

print(d)

#Longest word in a sentence
sentence = input("Enter sentence: ")
words = sentence.split()

longest = words[0]

for word in words:
    if len(word) > len(longest):
        longest = word

print("Longest word:", longest)


#Smallest word in a sentence
sentence = input("Enter sentence: ")
words = sentence.split()

smallest = words[0]

for word in words:
    if len(word) < len(smallest):
        smallest = word

print("Smallest word:", smallest)
