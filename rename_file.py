from pathlib import Path

# Current directory
root_dir = Path.cwd()

# Find all .txt files recursively
txt_files = root_dir.rglob("*.txt")

count = 0

for txt_file in txt_files:
    # Create new file path with .md extension
    md_file = txt_file.with_suffix(".md")
    
    # Rename file
    txt_file.rename(md_file)
    
    print(f"Renamed: {txt_file} -> {md_file}")
    count += 1

print(f"\nDone! Renamed {count} file(s).")