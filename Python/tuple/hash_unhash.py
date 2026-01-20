# HASHABLE OBJECTS (can be dict keys or set elements)

# 1. Integers, Strings, Tuples are hashable
hashable_dict = {
    1: "integer key",
    "name": "string key",
    (1, 2): "tuple key"
}
print("Hashable dict:", hashable_dict)

# Set with hashable objects
hashable_set = {1, "hello", (3, 4)}
print("Hashable set:", hashable_set)

# Hash value of immutable objects
print(f"Hash of 42: {hash(42)}") # output: Hash of 42: <some integer>
print(f"Hash of 'python': {hash('python')}") # output: Hash of 'python': <some integer>
print(f"Hash of (1,2,3): {hash((1, 2, 3))}") # output: Hash of (1,2,3): <some integer>

print("\n" + "="*50 + "\n")

# UNHASHABLE OBJECTS (cannot be dict keys or in sets) ----> Important

# 1. Lists are unhashable
my_list = [1, 2, 3]
try:
    unhashable_dict = {my_list: "list key"}  # ERROR!
except TypeError as e:
    print(f"Error with list as key: {e}")

# 2. Dictionaries are unhashable
my_dict = {"a": 1}
try:
    test_set = {my_dict}  # ERROR!
except TypeError as e:
    print(f"Error with dict in set: {e}")

# 3. Sets are unhashable
my_set = {1, 2, 3}
try:
    another_set = {my_set}  # ERROR!
except TypeError as e:
    print(f"Error with set in set: {e}")

print("\n" + "="*50 + "\n")

# Tuple with mutable object inside is unhashable
tuple_with_list = (1, [2, 3])  # Contains a list
try:
    test = {tuple_with_list: "value"}
except TypeError as e:
    print(f"Error with tuple containing list: {e}")

# Pure tuple is hashable
pure_tuple = (1, 2, 3)
print(f"Pure tuple as key works: {(pure_tuple): 'value'}")