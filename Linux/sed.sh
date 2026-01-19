#!/bin/bash

# SED (Stream Editor) Interview Commands & Examples

# 1. SUBSTITUTION - Replace first occurrence in each line
echo "=== Substitution (s command) ==="
echo "hello world hello" | sed 's/hello/hi/'
# Output: hi world hello

# 2. SUBSTITUTION - Replace all occurrences (global flag)
echo "hello world hello" | sed 's/hello/hi/g'
# Output: hi world hi

# 3. SUBSTITUTION - Case insensitive
echo "Hello HELLO hello" | sed 's/hello/hi/gi'
# Output: hi hi hi

# 4. SUBSTITUTION - With delimiters (useful for paths)
echo "/home/user/file" | sed 's|/home|/root|'
# Output: /root/user/file

# 5. DELETE - Remove entire line matching pattern
echo -e "keep this\ndelete this\nkeep this" | sed '/delete/d'
# Output: keep this, keep this

# 6. PRINT - Print specific lines only
echo -e "line1\nline2\nline3" | sed -n '2p'
# Output: line2

# 7. PRINT - Print range of lines
echo -e "line1\nline2\nline3\nline4" | sed -n '2,3p'
# Output: line2, line3

# 8. ADDRESS - Delete lines matching pattern
seq 1 5 | sed '/3/d'
# Output: 1,2,4,5

# 9. APPEND - Add line after match
echo -e "line1\nline2" | sed '/line1/a\new line'
# Output: line1, new line, line2

# 10. INSERT - Add line before match
echo -e "line1\nline2" | sed '/line2/i\new line'
# Output: line1, new line, line2

# 11. CHANGE - Replace entire matched line
echo -e "old1\nold2" | sed '/old1/c\new line'
# Output: new line, old2

# 12. MULTIPLE COMMANDS - Use -e flag
echo "hello" | sed -e 's/hello/hi/' -e 's/hi/bye/'
# Output: bye

# 13. BACKREFERENCE - Capture and reuse patterns
echo "hello world" | sed 's/\(hello\) \(world\)/\2 \1/'
# Output: world hello

# 14. RANGE WITH COMMANDS
seq 1 5 | sed '2,4s/^/PREFIX:/'
# Output: 1, PREFIX:2, PREFIX:3, PREFIX:4, 5

# 15. INPLACE EDITING - Modify file directly
sed -i 's/old/new/g' filename.txt

# 16. NEGATION - All lines except pattern
seq 1 5 | sed '/3/!d'
# Output: 3

# 17. MULTIPLE SUBSTITUTIONS in one line
echo "aaa bbb ccc" | sed 's/aaa/111/; s/bbb/222/; s/ccc/333/'
# Output: 111 222 333

# 18. HOLD BUFFER - Complex pattern matching
echo -e "start\nmiddle\nend" | sed -n '/start/,/end/p'
# Output: start, middle, end

# 19. TRANSLITERATE - Similar to tr command
echo "hello" | sed 'y/helo/HELO/'
# Output: HELLO

# 20. QUIET MODE - Suppress automatic printing (-n flag)
echo -e "line1\nline2\nline3" | sed -n 's/line/LINE/p'
# Output: LINE1, LINE2, LINE3

# 21. delete blank lines
sed '/^$/d' filename.txt

# 22. add text at the end of each line
sed 's/$/ - END/' filename.txt

# 23. add text at the beginning of each line
sed 's/^/START - /' filename.txt

# 24. add text before first line
sed '1i\This is the first line' filename.txt

# 25. add text after last line
sed '$a\This is the last line' filename.txt