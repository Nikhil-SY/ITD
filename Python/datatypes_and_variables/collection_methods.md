🔥 Interview Gold (Must Remember)

find() → safe (-1)

index() → unsafe (error)

replace() → string only

No replace() for list/set/dict

Strings are immutable


# Python String Methods – Substring + Recap (Complete)

> 🔑 Reminder: **Strings are immutable** → every method returns a **new string**

---

## 1️⃣ Substring Extraction Methods (VERY IMPORTANT)

---

### 🔹 Slicing (`[:]`)  ← *Primary substring mechanism*

```python
s = "aws azure gcp"
print(s[0:3])
```

**Output**

```
aws
```

#### Forms of slicing

```python
s[start:end]      # end excluded
s[:end]           # from beginning
s[start:]         # till end
s[start:end:step] # step
```

```python
print(s[:3])
print(s[4:])
print(s[::2])
```

**Output**

```
aws
azure gcp
a z r c
```

---

### 🔹 Negative Indexing

```python
print(s[-3:])
```

**Output**

```
gcp
```

---

## 2️⃣ Substring Search Methods

---

### 🔹 `find()`

```python
s = "aws azure gcp"
print(s.find("azure"))
```

**Output**

```
4
```

> Returns `-1` if not found

---

### 🔹 `rfind()` (search from right)

```python
s = "aws azure aws"
print(s.rfind("aws"))
```

**Output**

```
11
```

---

### 🔹 `index()` / `rindex()`

```python
print(s.index("azure"))
```

**Output**

```
4
```

> ❌ Raises error if substring not found

---

### 🔹 `count()` (substring frequency)

```python
s = "aws aws azure aws"
print(s.count("aws"))
```

**Output**

```
3
```

---

## 3️⃣ Substring Replacement Methods (Recap + Clarity)

---

### 🔹 `replace()`

```python
s = "aws aws azure aws"
print(s.replace("aws", "gcp", 2))
```

**Output**

```
gcp gcp azure aws
```

#### Execution recap:

* Scans **left → right**
* Replaces **first 2 matches**
* Stops after count reached

---

### 🔹 Replace ONLY second occurrence (recap)

```python
s = "aws aws azure aws"
parts = s.split("aws", 2)
result = parts[0] + "aws" + "gcp" + parts[2]
print(result)
```

**Output**

```
aws gcp azure aws
```

---

## 4️⃣ Split-Based Substring Methods (Previously Used)

---

### 🔹 `split()`

```python
s = "aws azure gcp"
print(s.split())
```

**Output**

```
['aws', 'azure', 'gcp']
```

---

### 🔹 `split(sep, maxsplit)`

```python
s = "aws:azure:gcp"
print(s.split(":", 1))
```

**Output**

```
['aws', 'azure:gcp']
```

---

### 🔹 `rsplit()`

```python
print(s.rsplit(":", 1))
```

**Output**

```
['aws:azure', 'gcp']
```

---

### 🔹 `join()` (reverse of split)

```python
lst = ['aws', 'azure', 'gcp']
print(" ".join(lst))
```

**Output**

```
aws azure gcp
```

---

## 5️⃣ Boundary / Substring Validation

---

### 🔹 `startswith()`

```python
print("aws azure".startswith("aws"))
```

**Output**

```
True
```

---

### 🔹 `endswith()`

```python
print("aws azure".endswith("azure"))
```

**Output**

```
True
```

---

## 6️⃣ Substring Cleanup Methods (Previously Used)

---

### 🔹 `strip()` / `lstrip()` / `rstrip()`

```python
s = "  aws  "
print(s.strip())
print(s.lstrip())
print(s.rstrip())
```

**Output**

```
aws
aws  
  aws
```

---

## 7️⃣ Substring Case Transformation

---

```python
s = "aws DevOps"
print(s.upper())
print(s.lower())
print(s.title())
print(s.capitalize())
```

**Output**

```
AWS DEVOPS
aws devops
Aws Devops
Aws devops
```

---

## 8️⃣ Substring Checking (Boolean Methods)

---

```python
print("aws123".isalnum())
print("aws".isalpha())
print("123".isdigit())
```

**Output**

```
True
True
True
```

---

## 9️⃣ Advanced Substring Translation (Previously Shown)

---

### 🔹 `maketrans()` + `translate()`

```python
table = str.maketrans("aws", "123")
print("aws".translate(table))
```

**Output**

```
123
```

---

## 🔥 Final Interview Summary Table

| Category          | Key Methods          |
| ----------------- | -------------------- |
| Extract substring | slicing              |
| Search substring  | find, rfind, index   |
| Replace substring | replace              |
| Split substring   | split, rsplit        |
| Join substring    | join                 |
| Boundary check    | startswith, endswith |
| Cleanup           | strip                |
| Case change       | upper, lower         |
| Count             | count                |

---

## 🧠 One-Line Interview Explanation

> **“Python provides slicing for extraction, search methods for locating substrings, replace for modification, and split/join for structural substring manipulation — all returning new strings due to immutability.”**



# Python Collection Methods – List, Tuple, Set, Dictionary

---

## 1️⃣ List Methods (`list`)

Lists are **ordered, mutable, and allow duplicates**.

### 🔹 Adding Elements

```python
lst = [1, 2, 3]
lst.append(4)
print(lst)
```

**Output**

```
[1, 2, 3, 4]
```

```python
lst.extend([5, 6])
print(lst)
```

**Output**

```
[1, 2, 3, 4, 5, 6]
```

```python
lst.insert(1, 10)
print(lst)
```

**Output**

```
[1, 10, 2, 3, 4, 5, 6]
```

---

### 🔹 Removing Elements

```python
lst.remove(10)
print(lst)
```

**Output**

```
[1, 2, 3, 4, 5, 6]
```

```python
x = lst.pop()
print(x, lst)
```

**Output**

```
6 [1, 2, 3, 4, 5]
```

```python
lst.clear()
print(lst)
```

**Output**

```
[]
```

---

### 🔹 Searching & Counting

```python
lst = [1, 2, 2, 3]
print(lst.index(2))
print(lst.count(2))
```

**Output**

```
1
2
```

---

### 🔹 Sorting & Reversing (Different Forms)

```python
lst = [3, 1, 4, 2]
lst.sort()
print(lst)
```

**Output**

```
[1, 2, 3, 4]
```

```python
lst.sort(reverse=True)
print(lst)
```

**Output**

```
[4, 3, 2, 1]
```

```python
lst.reverse()
print(lst)
```

**Output**

```
[1, 2, 3, 4]
```

---

## 2️⃣ Tuple Methods (`tuple`)

Tuples are **ordered and immutable** → very few methods.

### 🔹 Available Methods

```python
t = (1, 2, 2, 3)
print(t.count(2))
print(t.index(3))
```

**Output**

```
2
3
```

> ⚠️ No add/remove/update methods because tuples are immutable.

---

## 3️⃣ Set Methods (`set`)

Sets are **unordered, mutable, and do NOT allow duplicates**.

---

### 🔹 Adding & Removing

```python
s = {1, 2, 3}
s.add(4)
print(s)
```

**Output**

```
{1, 2, 3, 4}
```

```python
s.update([5, 6])
print(s)
```

**Output**

```
{1, 2, 3, 4, 5, 6}
```

```python
s.remove(6)
print(s)
```

**Output**

```
{1, 2, 3, 4, 5}
```

```python
s.discard(10)  # no error
print(s)
```

**Output**

```
{1, 2, 3, 4, 5}
```

---

### 🔹 Set Operations (Multiple Forms Exist)

```python
a = {1, 2, 3}
b = {3, 4, 5}

print(a.union(b))
print(a | b)
```

**Output**

```
{1, 2, 3, 4, 5}
```

```python
print(a.intersection(b))
print(a & b)
```

**Output**

```
{3}
```

```python
print(a.difference(b))
print(a - b)
```

**Output**

```
{1, 2}
```

```python
print(a.symmetric_difference(b))
print(a ^ b)
```

**Output**

```
{1, 2, 4, 5}
```

---

## 4️⃣ Dictionary Methods (`dict`)

Dictionaries store **key–value pairs**, keys are unique.

---

### 🔹 Accessing Data

```python
d = {"name": "Nikhil", "role": "DevOps"}

print(d.get("name"))
print(d.get("age", "Not Found"))
```

**Output**

```
Nikhil
Not Found
```

---

### 🔹 Adding & Updating

```python
d["experience"] = 2
print(d)
```

**Output**

```
{'name': 'Nikhil', 'role': 'DevOps', 'experience': 2}
```

```python
d.update({"role": "Infra Engineer"})
print(d)
```

**Output**

```
{'name': 'Nikhil', 'role': 'Infra Engineer', 'experience': 2}
```

---

### 🔹 Removing

```python
d.pop("experience")
print(d)
```

**Output**

```
{'name': 'Nikhil', 'role': 'Infra Engineer'}
```

```python
d.popitem()
print(d)
```

**Output**

```
{'name': 'Nikhil'}
```

---

### 🔹 Views (Different Forms)

```python
d = {"a": 1, "b": 2}

print(d.keys())
print(d.values())
print(d.items())
```

**Output**

```
dict_keys(['a', 'b'])
dict_values([1, 2])
dict_items([('a', 1), ('b', 2)])
```

---

## 🔥 Quick Interview Comparison

| Collection | Mutable | Ordered    | Duplicate Allowed | Key Methods          |
| ---------- | ------- | ---------- | ----------------- | -------------------- |
| List       | Yes     | Yes        | Yes               | append, extend, sort |
| Tuple      | No      | Yes        | Yes               | count, index         |
| Set        | Yes     | No         | No                | union, intersection  |
| Dict       | Yes     | Yes (3.7+) | Keys ❌            | get, update          |



