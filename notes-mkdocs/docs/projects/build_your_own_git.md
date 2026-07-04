---
tags:
  - Computer Programming
  - Version Control
  - Python
---

This journal documents errors made, lessons learned, troubleshooting steps taken, and resources used across all completed stages of the CodeCrafters "Build Your Own Git" challenge in Python.

---

# Stage 1: Read a Blob Object (`git cat-file`)

## Errors Made

**Jumping ahead mentally** — Before writing any code, assumed this stage was about commits and who committed code. It was only about reading blobs. Lesson: read the stage carefully and solve only what's in front of you.

**Wrong index for the hash** — Initially assumed `sys.argv` worked differently. Had to write out the full list to figure out the hash was at index `[3]`, not somewhere else.

**Splitting on the wrong character** — Tried to split on `\` instead of `\0`. The null byte is `\x00` in Python binary mode, not just a backslash.

**Using `print()` instead of `sys.stdout.write()`** — `print()` appends a newline which broke the tester output. Had to switch to `sys.stdout.write()`.

**Indentation issues** — Python uses indentation instead of curly braces `{}`. Copy-pasting into chat mangled the indentation, but the underlying logic was correct.

## What I Learned

- `sys.argv` is a list of everything typed on the command line. Index `[0]` is always the script name, so real arguments start at `[1]`.
- Git splits object hashes into a 2-character folder and 38-character filename to prevent inode exhaustion (too many files in one directory).
- Compressed files must be opened in binary mode `"rb"`, not text mode `"r"`.
- After decompressing a blob, the format is `blob <size>\0<content>`. The null byte `\x00` separates the header from the content.
- Binary data must be decoded with `.decode()` before printing as text.

## Troubleshooting Steps

1. Wrote out `sys.argv` as a full list to find the correct index for the hash.
2. Confirmed the null byte separator by re-reading the blob format in the instructions.
3. Switched from `print()` to `sys.stdout.write()` after reading the notes section warning about newlines.

## Resources Used

- CodeCrafters stage instructions
- Python `zlib` documentation (for `wbits` parameter, determined default was sufficient)
- `sys.argv` documentation

---

# Stage 2: Create a Blob Object (`git hash-object`)

## Errors Made

**`sys.arg` typo** — Wrote `sys.arg[3]` instead of `sys.argv[3]`. Python threw an `AttributeError`.

**Wrong slice index for filename** — Used `hash[3:]` instead of `hash[2:]` when splitting the hash into folder and filename.

**Using f-string to combine bytes** — Tried `f"{encodingHeader}{content}"` which creates a string, not bytes. You cannot mix strings and bytes in Python — it throws a `TypeError`.

**Using wrong variable name** — Used `data` instead of `combining` when hashing and compressing. Variable names must be consistent.

**`os.mkdir` crashing on existing folders** — If the folder already exists, `os.mkdir` throws a `FileExistsError`. Fixed by switching to `os.makedirs(path, exist_ok=True)`.

**`sys.stdout.write` inside the `with open` block** — Wrote the output inside the file-writing block instead of after it. Moved it outside.

## What I Learned

- This stage is the reverse of `cat-file` — instead of reading and decompressing, you build, compress and write.
- The SHA-1 hash must be computed over the header + content combined, not just the content alone. Two files with the same content but different headers must produce different hashes.
- Headers must be encoded to bytes with `.encode()` before combining with binary content.
- `os.makedirs` with `exist_ok=True` is safer than `os.mkdir` it won't crash if the folder already exists.
- The SHA-1 hash is computed on uncompressed data. Compression happens after hashing.
- `hashlib.sha1(data).hexdigest()` gives a readable 40-character hex string.

## Troubleshooting Steps

1. Wrote out the full `sys.argv` list to confirm the filename was at index `[3]`.
2. Traced through the variable names to find where `data` was used incorrectly instead of `combining`.
3. Tested `os.makedirs` with `exist_ok=True` to prevent crash on duplicate folder creation.

## Resources Used

- CodeCrafters stage instructions
- Python `hashlib` documentation
- Python `os.makedirs` documentation

---

# Stage 3: Read a Tree Object (`git ls-tree`)

## Errors Made

**Misidentifying the stage** — Initially thought this was about "creating blob storage." Re-reading confirmed it was about reading/listing tree contents.

**Opening `.git/objects` directly** — Tried to open the directory itself instead of building the full file path from the hash.

**Using wrong `sys.argv` index** — Assumed the hash was at `sys.argv[4]`. Writing out the full list confirmed it was at `sys.argv[3]`.

**Splitting on wrong type** — Used `'\0'` (a string) instead of `b'\x00'` (bytes) when splitting binary data. Python throws a `TypeError` when mixing types.

**Using `splitBinary[7:]`** — Misunderstood list indexing. Splitting on `\x00` gives only 2 parts: index `[0]` is the header, index `[1]` is the content.

**Using `return` inside the while loop** — `return name` exits the function after the first entry. Should use `print(name)` to output each name and continue looping.

**`position =+ 20` outside the loop** — This only ran once and was outside the while loop. Needed to be `position = positionOfnull + 1 + 20` inside the loop.

## What I Learned

- Tree objects have multiple entries, each with a mode, name, null byte, and raw 20-byte SHA.
- The SHA in tree objects is raw bytes (not hex), so you cannot read the file as text.
- A `while` loop with manual position tracking is needed to parse binary formats where entries have variable length.
- `entries.index(b"\x00", position)` finds the next null byte starting from a given position.
- After the null byte, you skip exactly 20 bytes for the SHA before the next entry starts.
- `split(" ", 1)` splits on the first space only, giving `["100644", "filename"]`. Index `[1]` is the name.

## Troubleshooting Steps

1. Wrote out the full `sys.argv` list to confirm the correct index.
2. Traced through the binary format manually to understand why `split()` alone wasn't enough.
3. Added `position = positionOfnull + 1 + 20` to correctly advance through entries.
4. Replaced `return` with `print()` to stop the function from exiting after the first entry.

## Resources Used

- CodeCrafters stage instructions
- Git tree object format documentation

---

# Stage 4: Write a Tree Object (`git write-tree`)

## Errors Made

**Iterating over `.git/objects` instead of the working directory** — The working directory `"."` is where actual files live. `.git/objects` is internal Git storage.

**`os.listdir.sort(directory)` — invalid syntax** — `sort()` is a method on a list, not on `os.listdir`. Had to store the list first, then call `.sort()` on it.

**`entries.append(sha1Hash)` — appending only the hash** — Each entry needs three things: mode, name, and hash. Should append a tuple `("100644", x, sha1Hash)`.

**Hardcoding `"3b"` in `os.mkdir`** — Used the example hash from the instructions instead of the actual `folderName` variable.

**`treeContent = b""` inside the loop** — This reset the content to empty on every iteration. Moved it before the loop.

**`treeContent =+ ...` — invalid operator** — Python uses `+=` to add to an existing variable, not `=+`.

**`combiningHeadercontent = treeHeader + treeContent`** — `treeHeader` is a string and `treeContent` is bytes. Must encode the header first.

**`from unicodedata import combining`** — An accidental import that conflicted with the variable name `combining`. Deleted it.

**`elif command == "write-tree"` had wrong body** — Was trying to read `sys.argv[3]` but `write-tree` takes no arguments. Should just call `writeTree(".")`.

## What I Learned

- Recursion means calling a function inside itself. `writeTree` calls itself when it encounters a subdirectory.
- `os.path.isfile(path)` and `os.path.isdir(path)` return `True` or `False` use them directly in `if` statements.
- `os.path.join(directory, x)` builds a full path from a directory and a filename.
- Tree entries must be tuples with `(mode, name, sha1Hash)` to store all three pieces of data.
- File mode is `"100644"` for regular files and `"40000"` for directories.
- `bytes.fromhex(sha1Hash)` converts a hex string to raw 20 bytes for writing into the tree.
- The `write-tree` command takes no arguments, it writes the current working directory as a tree.
- Refactoring `hash-object` logic into a `createBlob()` function made it reusable across stages.

## Troubleshooting Steps

1. Confirmed the working directory `"."` is the correct starting point, not `.git/objects`.
2. Fixed `os.listdir.sort()` by separating into two lines: store the list, then sort it.
3. Changed `entries.append(sha1Hash)` to `entries.append(("100644", x, sha1Hash))`.
4. Moved `treeContent = b""` before the loop so it doesn't reset each iteration.
5. Removed accidental `from unicodedata import combining` import.

## Resources Used

- CodeCrafters stage instructions
- Ben Hoyt's pygit article: https://benhoyt.com/writings/pygit/#committing
- Python `os.path` documentation

---

# Running Themes & Lessons

**Read the stage carefully before coding.** The first instinct was always to jump ahead. Each stage is one specific thing.

**Write out `sys.argv` as a list every time.** It removes all guesswork about which index holds what.

**Bytes and strings are different types in Python.** You cannot mix them. Always encode strings to bytes before combining with binary data.

**`os.makedirs` with `exist_ok=True` is always safer than `os.mkdir`.** Use it whenever creating directories in Git objects.

**Build pseudocode first.** Every stage went smoother when the steps were written in plain English before touching the code.

**Variable names must be consistent.** Several bugs came from using the wrong variable name.

**Position tracking in binary data requires a `while` loop.** When entries have variable length followed by fixed-length raw bytes, `split()` alone is not enough.