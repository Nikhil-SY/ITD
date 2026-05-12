#!/bin/bash

# ============================================
# CONDITIONALS
# ============================================

# IF-ELSE Statement
echo "=== IF-ELSE Example ==="
age=20
if [ $age -ge 18 ]; then
    echo "You are an adult"
else
    echo "You are a minor"
fi

# IF-ELIF-ELSE
echo -e "\n=== IF-ELIF-ELSE Example ==="
score=75
if [ $score -ge 90 ]; then
    echo "Grade: A"
elif [ $score -ge 80 ]; then
    echo "Grade: B"
elif [ $score -ge 70 ]; then
    echo "Grade: C"
else
    echo "Grade: F"
fi

# Test Operators
echo -e "\n=== Test Operators ==="
file="/etc/passwd"
[ -f "$file" ] && echo "File exists" || echo "File not found"
[ -d "/home" ] && echo "Directory exists"
[ -z "" ] && echo "String is empty"

# ============================================
# LOOPS
# ============================================

# FOR Loop
echo -e "\n=== FOR Loop Example ==="
for i in 1 2 3 4 5; do
    echo "Number: $i"
done

# FOR Loop with Range
echo -e "\n=== FOR Loop with Range ==="
for i in {1..3}; do
    echo "Count: $i"
done

# FOR Loop with C-style syntax
echo -e "\n=== C-style FOR Loop ==="
for ((i=0; i<3; i++)); do
    echo "Index: $i"
done

# WHILE Loop
echo -e "\n=== WHILE Loop Example ==="
counter=1
while [ $counter -le 3 ]; do
    echo "Loop iteration: $counter"
    ((counter++))
done

# UNTIL Loop (opposite of while)
echo -e "\n=== UNTIL Loop Example ==="
count=1
until [ $count -gt 3 ]; do
    echo "Until loop: $count"
    ((count++))
done

# CASE Statement
echo -e "\n=== CASE Statement Example ==="
color="red"
case $color in
    red)
        echo "Color is red"
        ;;
    blue)
        echo "Color is blue"
        ;;
    green)
        echo "Color is green"
        ;;
    *)
        echo "Unknown color"
        ;;
esac

# BREAK and CONTINUE
echo -e "\n=== BREAK Example ==="
for i in {1..5}; do
    if [ $i -eq 3 ]; then
        break
    fi
    echo "Value: $i"
done

echo -e "\n=== CONTINUE Example ==="
for i in {1..5}; do
    if [ $i -eq 3 ]; then
        continue
    fi
    echo "Value: $i"
done

####Special variables and expression#####

# 1️⃣ $* and $@ in Bash

## What are $* and $@?

Both `$*` and `$@` are **special parameters** representing all positional arguments passed to a script.

Example:

```bash
./script.sh one two three
```

Inside script:

* `$1 = one`
* `$2 = two`
* `$3 = three`

---

## "$*" (Single String)

```bash
echo "$*"
```

Output:

```
one two three
```

Internally treated as:

```
"one two three"
```

---

## "$@" (Separate Arguments)

```bash
echo "$@"
```

Internally treated as:

```
"one" "two" "three"
```

---

## Loop Difference (Important)

```bash
for arg in "$*"; do
  echo "$arg"
done
```

✔ One iteration

```bash
for arg in "$@"; do
  echo "$arg"
done
```

✔ Multiple iterations (recommended)

---

## Without Quotes (Dangerous)

```bash
for arg in $@; do
```

Arguments with spaces will break.

---

## Interview One-Liner

> Always use `"$@"` when iterating over arguments.

---

# 2️⃣ $() and $(()) in Bash

## $() – Command Substitution

```bash
today=$(date)
echo $today
```

Executes command and stores output.

---

## $(()) – Arithmetic Expansion

```bash
a=10
b=5
echo $((a + b))
```

Supports:

* `+ - * / %`
* `++ --`

---

## Difference

| Feature    | $()            | $(())      |
| ---------- | -------------- | ---------- |
| Purpose    | Command output | Arithmetic |
| Works with | Commands       | Integers   |

---

# 3️⃣ bc and expr

## expr (Integer Only)

```bash
expr 10 + 5
```

Must use spaces:

```bash
expr $a \* $b
```

---

## bc (Floating Point)

```bash
echo "scale=2; 10/3" | bc
```

Output:

```
3.33
```

---

## Comparison

| Feature  | expr | bc | $(()) |
| -------- | ---- | -- | ----- |
| Integer  | ✅    | ✅  | ✅     |
| Floating | ❌    | ✅  | ❌     |

---

# 4️⃣ Combined Example (All Concepts Together)

Script:

```bash
#!/bin/bash

echo "Arguments: $@"

num1=$1
num2=$2

if (( num1 > num2 )); then
    sum=$((num1 + num2))
    echo "Sum: $sum"
else
    result=$(echo "scale=2; $num1 / $num2" | bc)
    echo "Division: $result"
fi

echo "Executed on: $(date)"
```

---

# 5️⃣ if Statement in Bash

## Basic Syntax

```bash
if [ condition ]; then
    commands
fi
```

---

## Integer Comparison

| Operator | Meaning   |
| -------- | --------- |
| -eq      | equal     |
| -ne      | not equal |
| -gt      | greater   |
| -lt      | less      |

---

## Example

```bash
if (( a > b )); then
    echo "a is greater"
fi
```

---

## File Check

```bash
if [ -f file.txt ]; then
    echo "File exists"
fi
```

---

# 6️⃣ for Loop with $* and $@

## Basic Syntax

```bash
for var in list; do
    commands
done
```

---

## Using "$@"

```bash
for arg in "$@"; do
    echo "$arg"
done
```

✔ Safe
✔ Preserves spaces

---

## Using "$*"

```bash
for arg in "$*"; do
    echo "$arg"
done
```

❌ Single iteration

---

# 7️⃣ Check Even Number (Argument)

```bash
#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <number>"
    exit 1
fi

num=$1

if (( num % 2 == 0 )); then
    echo "$num is Even"
else
    echo "$num is Odd"
fi
```

---

# 8️⃣ String Operations in Bash

---

## String Length

```bash
str="hello"
echo ${#str}
```

---

## Concatenation

```bash
result="$a $b"
```

---

## Comparison

```bash
if [ "$a" = "$b" ]; then
```

Operators:

* `=`
* `!=`
* `-z`
* `-n`

---

## Substring

```bash
echo ${str:0:4}
```

---

## Remove Prefix

```bash
${file#*.}
```

---

## Remove Suffix

```bash
${file%.*}
```

---

## Replace

```bash
${str/Linux/Bash}
```

---

## Uppercase / Lowercase

```bash
${str^^}
${str,,}
```

---

## Pattern Matching

```bash
if [[ $file == *.txt ]]; then
```

---

# 🎯 Master Interview Summary

* `"$@"` → safe argument handling
* `$()` → command substitution
* `$(())` → integer arithmetic
* `bc` → floating-point math
* `if` → decision making
* `for` → iteration
* `${variable}` → powerful string manipulation
