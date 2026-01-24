"""
Demonstrates the usage of break, continue, and pass statements in loops,
along with various print() function parameters.

break statement:
    - Terminates the loop immediately when encountered
    - Useful for exiting loops based on a condition
    - Example: Stop printing numbers when we reach 5

continue statement:
    - Skips the current iteration and jumps to the next iteration
    - Useful for skipping specific values or conditions
    - Example: Skip printing even numbers

pass statement:
    - A null operation; does nothing when executed
    - Used as a placeholder for empty code blocks
    - Useful during development when a block is required syntactically
    - Example: Create an empty function or class structure

print() function parameters:
    - sep: Specifies the separator between multiple arguments (default: ' ')
    - end: Specifies what to print at the end (default: '\\n')
    - file: Specifies the file object to write to (default: sys.stdout)
    - flush: Boolean to force flushing the buffer (default: False)

Examples:

1. break statement:
   for i in range(1, 6):
       if i == 3:
           break
       print(i)
   Output: 1 2

2. continue statement:
   for i in range(1, 6):
       if i % 2 == 0:
           continue
       print(i)
   Output: 1 3 5

3. pass statement:
   for i in range(3):
       pass  # Placeholder, does nothing

4. print() with sep parameter:
   print('a', 'b', 'c', sep='-')
   Output: a-b-c

5. print() with end parameter:
   print('Hello', end=' ')
   print('World')
   Output: Hello World (on same line)

6. print() with sep and end:
   print(1, 2, 3, sep=', ', end='!\\n')
   Output: 1, 2, 3!
"""