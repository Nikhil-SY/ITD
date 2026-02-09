# Shell Script (`.sh`) — Modes, Symbols, and `set` Methods (Complete Guide)

---

## 1. Script Execution Modes

### 1.1 Interactive Mode

Commands typed manually.

```bash
ls
pwd
```

---

### 1.2 Non-Interactive Mode (Script Mode)

Commands executed from a file.

```bash
./script.sh
# or
bash script.sh
```

---

## 2. Shebang (`#!`)

### Purpose

Defines which interpreter executes the script.

```bash
#!/bin/bash
```

Other examples:

```bash
#!/bin/sh
#!/usr/bin/env bash
```

---

## 3. Comments (`#`)

```bash
# This is a comment
echo "Hello"
```

Output:

```text
Hello
```

---

## 4. Variables and `$` Symbol

```bash
name="Nikhil"
echo $name
```

Output:

```text
Nikhil
```

---

## 5. Quotes

### Single Quotes `' '`

No expansion.

```bash
echo '$name'
```

Output:

```text
$name
```

### Double Quotes `" "`

Allows expansion.

```bash
echo "$name"
```

Output:

```text
Nikhil
```

### Command Substitution

```bash
today=$(date)
echo $today
```

---

## 6. Input / Output Symbols

| Symbol | Meaning           |      |
| ------ | ----------------- | ---- |
| `>`    | Overwrite output  |      |
| `>>`   | Append            |      |
| `<`    | Input redirection |      |
| `      | `                 | Pipe |

Example:

```bash
ls | wc -l
```

---

## 7. Logical Operators

| Symbol | Meaning |   |    |
| ------ | ------- | - | -- |
| `&&`   | AND     |   |    |
| `      |         | ` | OR |

```bash
mkdir test && echo "Created"
```

---

## 8. Condition Symbols

### `[ ]`

```bash
if [ -f file.txt ]; then
  echo "File exists"
fi
```

### `[[ ]]` (recommended)

```bash
if [[ $name == "Nikhil" ]]; then
  echo "Match"
fi
```

---

## 9. File Test Operators

| Flag | Meaning    |
| ---- | ---------- |
| `-f` | File       |
| `-d` | Directory  |
| `-x` | Executable |
| `-r` | Readable   |
| `-w` | Writable   |

---

## 10. Arithmetic Symbols

```bash
a=10
b=5
((sum=a+b))
echo $sum
```

Output:

```text
15
```

---

## 11. Special Variables

| Symbol  | Meaning          |
| ------- | ---------------- |
| `$0`    | Script name      |
| `$1…$n` | Arguments        |
| `$#`    | Argument count   |
| `$@`    | All arguments    |
| `$?`    | Last exit status |
| `$$`    | Process ID       |

Example:

```bash
./test.sh hello
```

---

## 12. Loops

### For Loop

```bash
for i in 1 2 3; do
  echo $i
done
```

### While Loop

```bash
count=1
while [ $count -le 3 ]; do
  echo $count
  ((count++))
done
```

---

## 13. Case Statement

```bash
case $1 in
  start) echo "Starting" ;;
  stop) echo "Stopping" ;;
  *) echo "Unknown" ;;
esac
```

---

## 14. Background & Control Symbols

| Symbol | Meaning           |
| ------ | ----------------- |
| `&`    | Background        |
| `;`    | Command separator |
| `\`    | Escape            |

```bash
sleep 5 & echo "Running"
```

---

## 15. Exit Codes

```bash
exit 0   # success
exit 1   # failure
```

---

# 16. `set` Methods (VERY IMPORTANT)

`set` controls **script behavior** and is heavily used in production scripts.

---

## 16.1 `set -e` (Exit on error)

Stops script if any command fails.

```bash
set -e
ls valid_file
ls invalid_file
echo "This will not run"
```

Output:

```text
ls: cannot access 'invalid_file'
```

---

## 16.2 `set -x` (Debug mode)

Prints commands before executing.

```bash
set -x
echo "Hello"
```

Output:

```text
+ echo Hello
Hello
```

---

## 16.3 `set -u` (Undefined variable check)

Errors if variable is not defined.

```bash
set -u
echo $UNDEFINED
```

Output:

```text
UNDEFINED: unbound variable
```

---

## 16.4 `set -o pipefail` (Pipeline failure)

Fails pipeline if **any command fails**.

```bash
set -o pipefail
cat file.txt | grep "data" | wc -l
```

If `cat` fails → script fails ❌

---

## 16.5 Combined Best Practice (Recommended)

```bash
set -euo pipefail
```

Meaning:

* `-e` → exit on error
* `-u` → undefined variable error
* `pipefail` → pipeline safety

---

## 16.6 Disable `set` temporarily

```bash
set +e   # disable exit on error
set +x   # disable debug
```

---

## 17. File Permission Modes (for `.sh`)

```bash
chmod +x script.sh
```

| Mode | Meaning |
| ---- | ------- |
| r    | read    |
| w    | write   |
| x    | execute |

---

## 18. Real Production Script Example

```bash
#!/bin/bash
set -euo pipefail

APP="myapp"
echo "Deploying $APP"

mkdir /tmp/$APP
echo "Deployment complete"
```

---

## Interview-ready One-liner

> A shell script uses symbols like `#!`, `$`, `&&`, `||`, `|`, redirections, special variables, and control structures, while `set` options like `-e`, `-x`, `-u`, and `pipefail` control error handling, debugging, and script safety.

---
