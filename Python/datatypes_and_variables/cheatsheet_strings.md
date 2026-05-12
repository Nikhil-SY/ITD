# 🧾 Python String Methods – One-Page Cheat Sheet

> 🔑 **Strings are immutable** → every method returns a **new string**

---

## 🔹 Substring Extraction

```python
s = "aws azure gcp"

s[0:3]      # 'aws'
s[:3]       # 'aws'
s[4:]       # 'azure gcp'
s[-3:]      # 'gcp'
s[::2]      # 'a z r c'
```

---

## 🔹 Search & Position

```python
s.find("azure")     # 4        (-1 if not found)
s.rfind("aws")      # last index
s.index("gcp")      # error if not found
s.count("aws")      # frequency
```

---

## 🔹 Replace

```python
s.replace("aws", "gcp")       # replace all
s.replace("aws", "gcp", 2)    # first 2 only
```

➡ Replace **only 2nd occurrence**

```python
parts = s.split("aws", 2)
parts[0] + "aws" + "gcp" + parts[2]
```

---

## 🔹 Split & Join

```python
s.split()                 # ['aws','azure','gcp']
s.split(":", 1)           # maxsplit
s.rsplit(":", 1)          # from right
" ".join(list)            # join list → string
```

---

## 🔹 Case Conversion

```python
s.upper()
s.lower()
s.title()
s.capitalize()
s.swapcase()
```

---

## 🔹 Trim / Cleanup

```python
s.strip()      # both sides
s.lstrip()     # left
s.rstrip()     # right
```

---

## 🔹 Validation (Boolean)

```python
s.isalnum()
s.isalpha()
s.isdigit()
s.islower()
s.isupper()
s.isspace()
s.istitle()
```

---

## 🔹 Boundary Checks

```python
s.startswith("aws")
s.endswith("gcp")
```

---

## 🔹 Alignment / Padding

```python
s.center(10, "-")
s.ljust(10, "*")
s.rjust(10, "*")
"42".zfill(5)     # 00042
```

---

## 🔹 Formatting

```python
"Hello {}".format("Nikhil")
f"Hello {name}"
```

---

## 🔹 Encoding & Translation

```python
s.encode()                      # bytes
table = str.maketrans("aws","123")
"aws".translate(table)
```

---

## 🔥 Interview Gold (Must Remember)

* `find()` → safe (`-1`)
* `index()` → unsafe (error)
* `replace()` → **string only**
* No `replace()` for list/set/dict
* Strings are **immutable**

---

## 🧠 One-Line Interview Summary

> **“Python string methods provide slicing, searching, replacement, validation, formatting, and cleanup, all returning new strings due to immutability.”**
