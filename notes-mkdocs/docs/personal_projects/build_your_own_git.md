---
tags:
  - Computer Programming
  - Version Control
  - Python
---

This journal documents errors made, lessons learned, troubleshooting steps taken, and resources used across all completed stages of the CodeCrafters "Build Your Own Git" challenge in Python.

---

## Stage 1: Read a Blob Object (`git cat-file`)

### Errors Made

**Jumping ahead mentally** — Before writing any code, assumed this stage was about commits and who committed code. It was only about reading blobs. Lesson: read the stage carefully and solve only what's in front of you.

**Wrong index for the hash** — Initially assumed `sys.argv` worked differently. Had to write out the full list to figure out the hash was at index `[3]`, not somewhere else.

**Splitting on the wrong character** — Tried to split on `\` instead of `\0`. The null byte is `\x00` in Python binary mode, not just a backslash.

**Using `print()` instead of `sys.stdout.write()`** — `print()` appends a newline which broke the tester output. Had to switch to `sys.stdout.write()`.

### What I Learned

- `sys.argv` is a list of everything typed on the command line. Index `[0]` is always the script name, so real arguments start at `[1]`.
- Git splits object hashes into a 2-character folder and 38-character filename to prevent inode exhaustion (too many files in one directory).
- Compressed files must be opened in binary mode `"rb"`, not text mode `"r"`.
- After decompressing a blob, the format is `blob <size>\0<content>`. The null byte `\x00` separates the header from the content.
- Binary data must be decoded with `.decode()` before printing as text.

### Troubleshooting Steps

1. Wrote out `sys.argv` as a full list to find the correct index for the hash.
2. Confirmed the null byte separator by re-reading the blob format in the instructions.
3. Switched from `print()` to `sys.stdout.write()` after reading the notes section warning about newlines.

### Resources Used

- CodeCrafters stage comments had links to resources
- Python `zlib` documentation (for `wbits` parameter, determined default was sufficient)
- `sys.argv` documentation

### Code 

```python

    elif command == "cat-file":
        hash = sys.argv[3]
        folderName = hash[:2] # spilting the hash, the first two is the folder name and after the first two is the file name
        fileName = hash[2:] # git splits the hash to avoid having millions of files in a single directory (prevents inode exhaustion)
        filePath = f".git/objects/{folderName}/{fileName}" # used an an f string to simplify concatenation, this is building out the file path.
        with open(filePath, "rb") as file:
            data = file.read() # opens up the file to read it in binary because the file is compressed
            alibDecompress = zlib.decompress(data) # decompresses the file and stores it in a variable
            splitBinary = alibDecompress.split(b"\x00") # git adds a separator or null byte to figure out what is the header and what is the content of the file so we need to split it out.
            finalOutput = splitBinary[1].decode() # giving a variable and decoding the binary that was split from the file.
            sys.stdout.write(finalOutput) # used sys.stdout.write() instead of print() because print() appends a new line by default which throws off the tester.

```

---

## Stage 2: Create a Blob Object (`git hash-object`)

### Errors Made

**`sys.arg` typo** — Wrote `sys.arg[3]` instead of `sys.argv[3]`. Python threw an `AttributeError`.

**Wrong slice index for filename** — Used `hash[3:]` instead of `hash[2:]` when splitting the hash into folder and filename.

**Using f-string to combine bytes** — Tried `f"{encodingHeader}{content}"` which creates a string, not bytes. You cannot mix strings and bytes in Python, it throws a `TypeError`.

**Using wrong variable name** — Used `data` instead of `combining` when hashing and compressing. Variable names must be consistent.

**`os.mkdir` crashing on existing folders** — If the folder already exists, `os.mkdir` throws a `FileExistsError`. Fixed by switching to `os.makedirs(path, exist_ok=True)`.

**`sys.stdout.write` inside the `with open` block** — Wrote the output inside the file-writing block instead of after it. Moved it outside.

### What I Learned

- This stage is the reverse of `cat-file`, instead of reading and decompressing, you build, compress and write.
- The SHA-1 hash must be computed over the header + content combined, not just the content alone. Two files with the same content but different headers must produce different hashes.
- Headers must be encoded to bytes with `.encode()` before combining with binary content.
- `os.makedirs` with `exist_ok=True` is safer than `os.mkdir` it won't crash if the folder already exists.
- The SHA-1 hash is computed on uncompressed data. Compression happens after hashing.
- `hashlib.sha1(data).hexdigest()` gives a readable 40-character hex string.

### Troubleshooting Steps

1. Wrote out the full `sys.argv` list to confirm the filename was at index `[3]`.
2. Traced through the variable names to find where `data` was used incorrectly instead of `combining`.
3. Tested `os.makedirs` with `exist_ok=True` to prevent crash on duplicate folder creation.

### Resources Used

- CodeCrafters stage comments had links to resources
- Python `hashlib` documentation
- Python `os.makedirs` documentation

### Code

```python

def createBlob(fileName): # putting the creating blob from elif command == "hash-object" into a function.
    with open(fileName, "rb") as file:
        content = file.read()  # opens the file to read it since it's in binary I have to specify to open it as binary, give a variable to store the file contents
    header = f"blob {len(content)}\x00"  # created the header of the file using an f string and encoding it, the header needs to know the length of the cotent so git can know and use a null separator. used .encode() because content is bytes and going to combine them
    encodingHeader = header.encode()  # encoding the header
    combining = encodingHeader + content  # combining the encoded header with the content to hash them together. the hash needs to represent the complete blob object not just the file contents. If two files had the same content but different headers, Git needs to be able to tell them apart. The header includes the type and size, so hashing everything together makes the hash a unique fingerprint for the entire object
    sha1Hash = hashlib.sha1(combining).hexdigest()  # sha1 hash of the content and header and converts the hash into a readable 40-character string of hexadecimal characters.
    alibCompress = zlib.compress(combining)  # compresses the header and content to save disk space
    folderName = sha1Hash[:2]  # gets the folder name which is the first two characters of the hash
    fileName2 = sha1Hash[2:]  # gets the file name which is the hash after the two characters
    os.makedirs( f".git/objects/{folderName}/", exist_ok=True)  # makes a directory based on the foldername, if the folder doesn't exist yet, Python will error when you try to write a file into it. You have to create the folder first before you can put anything inside it. Changed it to os.makedirs() with exist_ok=True so it doesn't complain if it already exists
    filePath = f".git/objects/{folderName}/{fileName2}"  # sets a variable that creates the file path of the object
    with open(filePath, "wb") as file:
        data = file.write(alibCompress)  # writes the compressed binary file to the specified file path
    return sha1Hash

```

---

## Stage 3: Read a Tree Object (`git ls-tree`)

### Errors Made

**Opening `.git/objects` directly** — Tried to open the directory itself instead of building the full file path from the hash.

**Using wrong `sys.argv` index** — Assumed the hash was at `sys.argv[4]`. Writing out the full list confirmed it was at `sys.argv[3]`.

**Splitting on wrong type** — Used `'\0'` (a string) instead of `b'\x00'` (bytes) when splitting binary data. Python throws a `TypeError` when mixing types.

**Using `splitBinary[7:]`** — Misunderstood list indexing. Splitting on `\x00` gives only 2 parts: index `[0]` is the header, index `[1]` is the content.

**Using `return` inside the while loop** — `return name` exits the function after the first entry. Should use `print(name)` to output each name and continue looping.

**`position =+ 20` outside the loop** — This only ran once and was outside the while loop. Needed to be `position = positionOfnull + 1 + 20` inside the loop.

### What I Learned

- Tree objects have multiple entries, each with a mode, name, null byte, and raw 20-byte SHA.
- The SHA in tree objects is raw bytes (not hex), so you cannot read the file as text.
- A `while` loop with manual position tracking is needed to parse binary formats where entries have variable length.
- `entries.index(b"\x00", position)` finds the next null byte starting from a given position.
- After the null byte, you skip exactly 20 bytes for the SHA before the next entry starts.
- `split(" ", 1)` splits on the first space only, giving `["100644", "filename"]`. Index `[1]` is the name.

### Troubleshooting Steps

1. Wrote out the full `sys.argv` list to confirm the correct index.
2. Traced through the binary format manually to understand why `split()` alone wasn't enough.
3. Added `position = positionOfnull + 1 + 20` to correctly advance through entries.
4. Replaced `return` with `print()` to stop the function from exiting after the first entry.

### Resources Used

- Git tree object format documentation

### Code

```python

    elif command == "ls-tree":
        sha1Hash = sys.argv[3] # Get the tree sha1 hash from sys.argv[3]
        folderName = sha1Hash[:2]
        fileName = sha1Hash[2:]
        filePath = f".git/objects/{folderName}/{fileName}" # Build the file path (same as before)
        with open(filePath, "rb") as file:
            contents = file.read()
            alibDecompress = zlib.decompress(contents) # Read and decompress the file
            splitFile = alibDecompress.split(b"\x00", 1) # Strip the header by splitting on \0
            entries = splitFile[1]
        position = 0
        while position < len(entries):
            positionOfnull = entries.index(b"\x00", position) # find the position of \0
            modeAndname = entries[position:positionOfnull] # extract mode and name
            Output = modeAndname.decode() # decode
            finalOutput = Output.split(" ", 1) # split the space
            name = finalOutput[1] # get the name which is index 1 and set the variable
            print(name)
            position = positionOfnull + 1 + 20 # skip 20 bytes for SHA and move to the next entry

```

---

## Stage 4: Write a Tree Object (`git write-tree`)

### Errors Made

**Iterating over `.git/objects` instead of the working directory** — The working directory `"."` is where actual files live. `.git/objects` is internal Git storage.

**`os.listdir.sort(directory)` — invalid syntax** — `sort()` is a method on a list, not on `os.listdir`. Had to store the list first, then call `.sort()` on it.

**`entries.append(sha1Hash)` — appending only the hash** — Each entry needs three things: mode, name, and hash. Should append a tuple `("100644", x, sha1Hash)`.

**Hardcoding `"3b"` in `os.mkdir`** — Used the example hash from the instructions instead of the actual `folderName` variable.

**`treeContent = b""` inside the loop** — This reset the content to empty on every iteration. Moved it before the loop.

**`treeContent =+ ...` — invalid operator** — Python uses `+=` to add to an existing variable, not `=+`.

**`combiningHeadercontent = treeHeader + treeContent`** — `treeHeader` is a string and `treeContent` is bytes. Must encode the header first.

**`from unicodedata import combining`** — An accidental import that conflicted with the variable name `combining`. Deleted it.

**`elif command == "write-tree"` had wrong body** — Was trying to read `sys.argv[3]` but `write-tree` takes no arguments. Should just call `writeTree(".")`.

### What I Learned

- Recursion means calling a function inside itself. `writeTree` calls itself when it encounters a subdirectory.
- `os.path.isfile(path)` and `os.path.isdir(path)` return `True` or `False` use them directly in `if` statements.
- `os.path.join(directory, x)` builds a full path from a directory and a filename.
- Tree entries must be tuples with `(mode, name, sha1Hash)` to store all three pieces of data.
- File mode is `"100644"` for regular files and `"40000"` for directories.
- `bytes.fromhex(sha1Hash)` converts a hex string to raw 20 bytes for writing into the tree.
- The `write-tree` command takes no arguments, it writes the current working directory as a tree.
- Refactoring `hash-object` logic into a `createBlob()` function made it reusable across stages.

### Troubleshooting Steps

1. Confirmed the working directory `"."` is the correct starting point, not `.git/objects`.
2. Fixed `os.listdir.sort()` by separating into two lines: store the list, then sort it.
3. Changed `entries.append(sha1Hash)` to `entries.append(("100644", x, sha1Hash))`.
4. Moved `treeContent = b""` before the loop so it doesn't reset each iteration.
5. Removed accidental `from unicodedata import combining` import.

### Resources Used

- Ben Hoyt's pygit article: https://benhoyt.com/writings/pygit/#committing
- Python `os.path` documentation

---

### Code

```python

    def writeTree(directory): # created a function to create the tree which gets the current directory of the user as the argument
    listCurrentdirectory = os.listdir(directory) # set a variable and lists all files and directories (folders) in the current directory
    listCurrentdirectory.sort() # sorts them alphabetically
    entries = []
    for x in listCurrentdirectory:
        fullPath = os.path.join(directory, x)
        if x == ".git":
            continue
        if os.path.isfile(fullPath): # checks to see if it's a file
           sha1Hash = createBlob(fullPath)
           entries.append(("100644", x, sha1Hash))
        if os.path.isdir(fullPath): # checks to see if it's a directory (folder)
            sha1Hash = writeTree(fullPath)
            entries.append(("40000", x, sha1Hash))
    treeContent = b""
    for mode, name, sha1Hash in entries:
        convert = bytes.fromhex(sha1Hash)
        treeContent += f"{mode} {name}\0".encode() + convert
    treeHeader = f"tree {len(treeContent)}\0"
    encodingHeader = treeHeader.encode()
    combiningHeadercontent = encodingHeader + treeContent
    sha1Hash = hashlib.sha1(combiningHeadercontent).hexdigest()
    alibCompress = zlib.compress(combiningHeadercontent)
    folderName = sha1Hash[:2]
    fileName2 = sha1Hash[2:]
    os.makedirs(f".git/objects/{folderName}/", exist_ok=True)
    filePath = f".git/objects/{folderName}/{fileName2}"
    with open(filePath, "wb") as file:
        data = file.write(alibCompress)
    return sha1Hash

```

## Stage 5: Create a Commit Object (`git commit-tree`)
 
### Errors Made
 
**`return sha1Hash` inside `elif`** — `return` sends a value back from a function to whatever called it. But `elif command == "commit-tree":` is not a function — it's just a block inside `main()`. Nothing is calling it and waiting for a value back. Using `return` here just exits `main()` entirely. The fix is `sys.stdout.write(sha1Hash)`, which prints the hash to the terminal where the tester can read it.
 
**`encodingcommitString = commitString` without calling `.encode()`** — Named the variable as if it was encoded but never actually encoded it. So combining bytes header + string content threw a `TypeError`.
 
**Putting `\"` at the end of commit string lines** — Each line in the commit content ends with `\n` (newline), not `\"` (a quote character).
 
**Missing blank line before the commit message** — The commit format requires an empty line between the metadata and the message. Missing it would produce a malformed commit object.
 
**`message {sys.argv[6]}`** — The word "message" doesn't appear in the actual commit file format. The message is just the raw string on its own line.
 
### What I Learned
 
- The commit object follows the same build-hash-compress-write pattern as blobs and trees. The only difference is what the content looks like.
- Commit content is plain text with specific fields in a specific order: `tree`, `parent`, `author`, `committer`, blank line, then the message. Each line ends with `\n`.
- The tree and parent SHAs in a commit are 40-character hex strings, unlike in tree objects where they're 20 raw bytes.
- Author and committer can be hardcoded for this challenge. In a real Git implementation they'd come from your config.
- `return` exits a function and gives a value back to whoever called it. Inside an `elif` block in `main()`, there's no caller waiting — just use `sys.stdout.write()` to print the result.
- `commitString.encode()` converts the plain text commit content to bytes before combining with the encoded header. Same reason as always: can't mix strings and bytes in Python.
### Troubleshooting Steps
 
1. Wrote out the full `sys.argv` list to confirm tree sha at `[2]`, parent sha at `[4]`, message at `[6]`.
2. Fixed `return sha1Hash` to `sys.stdout.write(sha1Hash)` after realizing `elif` blocks can't return values.
3. Added `.encode()` to `commitString` after the `TypeError` from combining a string with bytes.
4. Added the blank `f"\n"` line between committer and message after re-reading the commit format.
### Resources Used
 
- CodeCrafters stage instructions (commit object format)
- Stack Overflow: https://stackoverflow.com/questions/22968856/what-is-the-file-format-of-a-git-commit-object-data-structure
### Code
 
```python
elif command == "commit-tree":
    commitString = (f"tree {sys.argv[2]}\n"
                    f"parent {sys.argv[4]}\n"
                    f"author John Doe <john@example.com> 1234567890 +0000\n"
                    f"committer John Doe <john@example.com> 1234567890 +0000\n"
                    f"\n"
                    f"{sys.argv[6]}\n")
    header = f"commit {len(commitString)}\x00"
    encodingHeader = header.encode()
    encodingcommitString = commitString.encode()
    combining = encodingHeader + encodingcommitString
    sha1Hash = hashlib.sha1(combining).hexdigest()
    alibCompress = zlib.compress(combining)
    folderName = sha1Hash[:2]
    fileName2 = sha1Hash[2:]
    os.makedirs(f".git/objects/{folderName}/", exist_ok=True)
    filePath = f".git/objects/{folderName}/{fileName2}"
    with open(filePath, "wb") as file:
        data = file.write(alibCompress)
    sys.stdout.write(sha1Hash)
```

## Running Themes & Lessons

**Read the stage carefully before coding.** The first instinct was always to jump ahead. Each stage is one specific thing.

**Write out `sys.argv` as a list every time.** It removes all guesswork about which index holds what.

**Bytes and strings are different types in Python.** You cannot mix them. Always encode strings to bytes before combining with binary data.

**`os.makedirs` with `exist_ok=True` is always safer than `os.mkdir`.** Use it whenever creating directories in Git objects.

**Build pseudocode first.** Every stage went smoother when the steps were written in plain English before touching the code.

**Variable names must be consistent.** Several bugs came from using the wrong variable name.

**Position tracking in binary data requires a `while` loop.** When entries have variable length followed by fixed-length raw bytes, `split()` alone is not enough.