# ========== 1. BASIC FUNCTIONS ==========
def greet(name):
    """Basic function with a parameter"""
    return f"Hello, {name}!"

print(greet("Alice"))
# Output: Hello, Alice!


# ========== 2. MULTIPLE RETURN VALUES ==========
def get_user_info():
    """Function returning multiple values"""
    name = "John"
    age = 30
    email = "john@example.com"
    return name, age, email

name, age, email = get_user_info()
print(f"Name: {name}, Age: {age}, Email: {email}")
# Output: Name: John, Age: 30, Email: john@example.com


# ========== 3. *ARGS (Variable Arguments) ==========
def sum_numbers(*args):
    """*args allows variable number of positional arguments"""
    total = 0
    print("Arguments received:", args) #output: Arguments received: (1, 2, 3, 4, 5)
    print("Type of args:", type(args)) #output: Type of args: <class 'tuple'>
    for num in args:
        total += num
    return total

print(sum_numbers(1, 2, 3, 4, 5))
# Output: 15

print(sum_numbers(10, 20))
# Output: 30


# ========== 4. **KWARGS (Keyword Arguments) ==========
def print_info(**kwargs):
    """**kwargs allows variable number of keyword arguments"""
    print("Keyword arguments received:", kwargs) #output: Keyword arguments received: {'name': 'Bob', 'age': 25, 'city': 'NYC'}
    print("Type of kwargs:", type(kwargs)) #output: Type of kwargs: <class 'dict'>
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Bob", age=25, city="NYC")
# Output:
# name: Bob
# age: 25
# city: NYC


# ========== 5. COMBINING *ARGS AND **KWARGS ==========
def full_function(name, *args, **kwargs):
    """Combining positional, *args, and **kwargs"""
    print(f"Name: {name}")
    print(f"Additional args: {args}")
    print(f"Keyword args: {kwargs}")

full_function("Alice", 1, 2, 3, age=30, city="LA")
# Output:
# Name: Alice
# Additional args: (1, 2, 3)
# Keyword args: {'age': 30, 'city': 'LA'}


# ========== 6. RECURSION ==========
def factorial(n):
    """Factorial using recursion"""
    if n <= 1:  # Base case
        return 1
    return n * factorial(n - 1)  # Recursive case

print(factorial(5))
# Output: 120 (5 * 4 * 3 * 2 * 1)


# ========== 7. RECURSION WITH MULTIPLE CALLS ==========
def fibonacci(n):
    """Fibonacci sequence using recursion"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(6))
# Output: 8 (0, 1, 1, 2, 3, 5, 8)


# ========== 8. RECURSION WITH MEMOIZATION (Optimization) ==========
# What is memoization? It is an optimization technique used primarily to speed up recursive algorithms by storing the results of expensive function calls and reusing them when the same inputs occur again.
def fibonacci_memo(n, memo=None):
    """Optimized fibonacci with memoization"""
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]

print(fibonacci_memo(10))
# Output: 55


# ========== 9. DEFAULT PARAMETERS ==========
def introduce(name, age=25, city="Unknown"):
    """Function with default parameters"""
    return f"{name} is {age} years old and lives in {city}"

print(introduce("Charlie"))
# Output: Charlie is 25 years old and lives in Unknown

print(introduce("David", 30, "Boston"))
# Output: David is 30 years old and lives in Boston


# ========== 10. LAMBDA FUNCTIONS ==========
#what is a lambda function? A lambda function is a small anonymous function defined with the lambda keyword. Lambda functions can have any number of arguments but only one expression. They are often used for short, throwaway functions that are not complex enough to warrant a full function definition.
square = lambda x: x ** 2 # flow: define a lambda function that takes one argument x and returns its square (x ** 2).
print(square(5))
# Output: 25

#explain lambda with multiple arguments
add = lambda x, y: x + y # flow: define a lambda function that takes two arguments x and y and returns their sum (x + y).
print(add(3, 7))


#explain lambda used with map() function 
numbers = [1, 2, 3, 4, 5]
#what is map() function? The map() function in Python applies a given function to all items in an iterable (like a list or tuple) and returns an iterator. It is often used with lambda functions for concise transformations.
squared = list(map(lambda x: x ** 2, numbers)) # flow: use the map() function to apply a lambda function that squares each element (x ** 2) in the numbers list. The result is converted to a list.
print(squared)
# Output: [1, 4, 9, 16, 25]


# ========== 11. VARIABLE SCOPE ==========
global_var = "Global"

def scope_example():
    local_var = "Local"
    print(global_var)  # Can access global
    print(local_var)   # Can access local
    
scope_example()
# Output:
# Global
# Local

#explain global keyword
def modify_global():
    global global_var
    global_var = "Modified Global"
modify_global()
print(global_var)
# Output: Modified Global

#explain nonlocal keyword
def outer_function():
    outer_var = "Outer"
    
    def inner_function():
        nonlocal outer_var # Use nonlocal to modify outer function's variable
        outer_var = "Modified Outer"
    
    inner_function()
    print(outer_var)
outer_function()
# Output: Modified Outer

#explain closure with nested functions
#what is a closure? A closure is a nested function that captures the local variables from its enclosing scope. This allows the inner function to remember the state of those variables even after the outer function has finished executing.

def outer_function_closure(msg):
    def inner_function():
        return f"Message: {msg}"
    return inner_function #why we return inner_function without parentheses? Because we want to return the function itself, not the result of calling it.
closure_func = outer_function_closure("Hello, Closure!")
print(closure_func()) # Output: Message: Hello, Closure!

#explain the flow of above closure example
# Flow:
# 1. outer_function_closure is called with "Hello, Closure!" as the argument.
# 2. Inside outer_function_closure, a local variable msg is set to "Hello, Closure!".
# 3. inner_function is defined inside outer_function_closure and captures the local variable msg.
# 4. outer_function_closure returns inner_function (without parentheses).
# 5. closure_func now holds a reference to inner_function.
# 6. When closure_func() is called, it executes inner_function which uses the captured value of msg.

#what happens if we call inner function without calling outer function
#inner_function() # This will raise a NameError because inner_function is not defined in the global scope.

#explain the ways of calling inner function without calling outer function
def get_inner_function():
    outer_var = "Outer"
    
    def inner_function():
        return outer_var
    
    return inner_function  
inner = get_inner_function()
print(inner())
# Output: Outer

# ========== 12. NESTED FUNCTIONS ==========
def outer(x):
    def inner(y):
        return x + y
    return inner

add_5 = outer(5)
print(add_5(10))
# Output: 15


# ========== 13. DECORATORS ==========
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper

@my_decorator
def say_hello(name):
    return f"Hello, {name}!"

print(say_hello("Eve"))
# Output:
# Before function call
# Hello, Eve!
# After function call


# ========== 14. PRACTICAL EXAMPLE: FUNCTION WITH ALL FEATURES ==========
def process_data(name, *values, operation="sum", **settings):
    """
    Process data with multiple features
    - name: required parameter
    - *values: variable positional arguments
    - operation: keyword argument with default
    - **settings: additional keyword arguments
    """
    print(f"Processing data for {name}")
    print(f"Values: {values}")
    print(f"Operation: {operation}")
    print(f"Settings: {settings}")
    
    if operation == "sum":
        return sum(values)
    elif operation == "avg":
        return sum(values) / len(values) if values else 0
    
result = process_data("Data1", 10, 20, 30, operation="avg", verbose=True, debug=False)
print(f"Result: {result}")
# Output:
# Processing data for Data1
# Values: (10, 20, 30)
# Operation: avg
# Settings: {'verbose': True, 'debug': False}
# Result: 20.0