#!/bin/bash

# ============================================
# BASH OPERATORS - Complete Guide
# ============================================

echo "===== ARITHMETIC OPERATORS ====="
a=10
b=3

echo "a=$a, b=$b"
echo "Addition (a+b): $((a + b))"
echo "Subtraction (a-b): $((a - b))"
echo "Multiplication (a*b): $((a * b))"
echo "Division (a/b): $((a / b))"
echo "Modulus (a%b): $((a % b))"
echo "Exponentiation (a**b): $((a ** b))"

echo -e "\n===== COMPARISON OPERATORS (Numeric) ====="
if [ $a -eq $b ]; then echo "$a -eq $b: true"; else echo "$a -eq $b: false"; fi
if [ $a -ne $b ]; then echo "$a -ne $b: true"; else echo "$a -ne $b: false"; fi
if [ $a -gt $b ]; then echo "$a -gt $b: true"; else echo "$a -gt $b: false"; fi
if [ $a -lt $b ]; then echo "$a -lt $b: true"; else echo "$a -lt $b: false"; fi
if [ $a -ge $b ]; then echo "$a -ge $b: true"; else echo "$a -ge $b: false"; fi
if [ $a -le $b ]; then echo "$a -le $b: true"; else echo "$a -le $b: false"; fi

echo -e "\n===== COMPARISON OPERATORS (String) ====="
str1="hello"
str2="world"

if [ "$str1" = "$str2" ]; then echo "str1 = str2: true"; else echo "str1 = str2: false"; fi
if [ "$str1" != "$str2" ]; then echo "str1 != str2: true"; else echo "str1 != str2: false"; fi
if [ -z "$str1" ]; then echo "str1 is empty: true"; else echo "str1 is empty: false"; fi
if [ -n "$str1" ]; then echo "str1 is not empty: true"; else echo "str1 is not empty: false"; fi

echo -e "\n===== LOGICAL OPERATORS ====="
x=5
y=10

if [ $x -lt 10 ] && [ $y -gt 5 ]; then echo "AND (&&): true"; fi
if [ $x -gt 10 ] || [ $y -gt 5 ]; then echo "OR (||): true"; fi
if ! [ $x -gt 10 ]; then echo "NOT (!): true"; fi

echo -e "\n===== FILE TEST OPERATORS ====="
file="/etc/passwd"

[ -e "$file" ] && echo "-e (exists): true"
[ -f "$file" ] && echo "-f (regular file): true"
[ -d "/home" ] && echo "-d (directory): true"
[ -r "$file" ] && echo "-r (readable): true"
[ -w "$file" ] && echo "-w (writable): false (probably)"
[ -x "/usr/bin/bash" ] && echo "-x (executable): true"
[ -s "$file" ] && echo "-s (size > 0): true"

echo -e "\n===== ASSIGNMENT OPERATORS ====="
num=5
echo "num=$num"
num=$((num + 3))
echo "After +=3: num=$num"
num=$((num - 2))
echo "After -=2: num=$num"
num=$((num * 2))
echo "After *=2: num=$num"

echo -e "\n===== BITWISE OPERATORS ====="
p=5     # 0101
q=3     # 0011

echo "p=$p, q=$q"
echo "AND (p & q): $((p & q))"
echo "OR (p | q): $((p | q))"
echo "XOR (p ^ q): $((p ^ q))"
echo "NOT (~p): $((~p))"
echo "Left Shift (p << 1): $((p << 1))"
echo "Right Shift (p >> 1): $((p >> 1))"