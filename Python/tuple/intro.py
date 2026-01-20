# TUPLES IN PYTHON - Complete Guide

# 1. WHAT IS A TUPLE?
# A tuple is an immutable (unchangeable) collection of ordered items
# Tuples are created using parentheses () and cannot be modified after creation

# 2. CREATING TUPLES
empty_tuple = ()
print(empty_tuple)  # Output: ()

single_item_tuple = (5,)  # Note: comma required for single item
print(single_item_tuple)  # Output: (5,)

mixed_tuple = (1, "hello", 3.14, True)
print(mixed_tuple)  # Output: (1, 'hello', 3.14, True)

tuple_without_parens = 10, 20, 30
print(tuple_without_parens)  # Output: (10, 20, 30)

# 3. ACCESSING TUPLE ELEMENTS
my_tuple = ("apple", "banana", "cherry", "date")
print(my_tuple[0])  # Output: apple
print(my_tuple[-1])  # Output: date (last element)
print(my_tuple[1:3])  # Output: ('banana', 'cherry') - slicing

# 4. TUPLE IMMUTABILITY (cannot change)
# my_tuple[0] = "orange"  # This would raise TypeError
# my_tuple.append("grape")  # This would raise AttributeError

# 5. TUPLE METHODS
numbers = (1, 2, 3, 2, 4, 2)
print(numbers.count(2))  # Output: 3 - counts occurrences
print(numbers.index(3))  # Output: 2 - finds first index of value

# 6. TUPLE UNPACKING
coordinates = (10, 20, 30)
x, y, z = coordinates
print(f"x={x}, y={y}, z={z}")  # Output: x=10, y=20, z=30

# 7. LOOPING THROUGH TUPLES
colors = ("red", "green", "blue")
for color in colors:
    print(color)  # Output: red, green, blue (each on new line)

# 8. TUPLE CONCATENATION & REPETITION
tuple1 = (1, 2)
tuple2 = (3, 4)
combined = tuple1 + tuple2
print(combined)  # Output: (1, 2, 3, 4)

repeated = ("x",) * 3
print(repeated)  # Output: ('x', 'x', 'x')

# 9. CHECKING MEMBERSHIP
print(2 in numbers)  # Output: True
print(5 in numbers)  # Output: False

# 10. TUPLE LENGTH
print(len(my_tuple))  # Output: 4

# 11. NESTED TUPLES
nested = ((1, 2), (3, 4), (5, 6))
print(nested[0])  # Output: (1, 2)
print(nested[1][0])  # Output: 3

# 12. TUPLE ADVANTAGES
# - Faster than lists
# - Can be used as dictionary keys
# - Safer for data that shouldn't change
dict_with_tuple_key = {(1, 2): "coordinates"}
print(dict_with_tuple_key[(1, 2)])  # Output: coordinates