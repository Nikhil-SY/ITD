# Example of set and frozenset

# Creating a set
my_set = {1, 2, 3}
print("Original set:", my_set)

# Modifying the set
my_set.add(4)
print("Modified set:", my_set)

# Creating a frozenset
my_frozenset = frozenset([1, 2, 3])
print("Frozenset:", my_frozenset)

# Attempting to modify the frozenset (will raise an error)
try:
    my_frozenset.add(4)
except AttributeError as e:
    print("Error:", e)

# Using frozenset as a dictionary key
my_dict = {my_frozenset: "This is a frozenset"}
print("Dictionary with frozenset as key:", my_dict)