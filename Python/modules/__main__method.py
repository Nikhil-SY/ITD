from calculator import add, multiply

"""
Module docstring explaining __name__ and __main__ in Python.

The __name__ variable is a special built-in variable in Python that contains the name of the 
current module. Its value depends on how the Python file is executed:

1. When a file is run directly (as the main program):
    __name__ is set to "__main__"
    
2. When a file is imported as a module in another file:
    __name__ is set to the module's name (the filename without .py)

The if __name__ == "__main__": pattern is a common Python idiom that allows you to:
- Write code that only executes when the script is run directly
- Write code that doesn't execute when the module is imported elsewhere
- Create files that can be both executed as standalone scripts and imported as reusable modules

Example Usage:

Consider two files:

FILE 1: calculator.py
     def add(a, b):
          return a + b
     
     def multiply(a, b):
          return a * b
     
     if __name__ == "__main__":
          print("Running calculator as main program")
          print("5 + 3 =", add(5, 3))
          print("5 * 3 =", multiply(5, 3))

FILE 2: main.py
     
     result1 = add(10, 20)
     result2 = multiply(10, 20)
     print("Results:", result1, result2)

OUTPUTS:

When running calculator.py directly:
     python calculator.py
     Output:
          Running calculator as main program
          5 + 3 = 8
          5 * 3 = 15

When running main.py (which imports calculator.py):
     python main.py
     Output:
          Results: 30 200
     
     (The code inside if __name__ == "__main__": in calculator.py does NOT execute)

This pattern is essential for writing reusable, modular Python code.
"""

#what will print if we print __name__ in main.py in this case
print("Value of __name__ in __main__method.py:", __name__) #Output: __main__