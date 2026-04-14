---
tags:
  - Version Control
  - DevOps
---

# `git config --global --add safe.directory`

This command tells Git to **trust a specific directory** that it might otherwise consider unsafe.

---

## Breaking It Down

| Part | What it does |
|------|--------------|
| `git config --global` | Writes the setting to your global Git config (`~/.gitconfig`), applying it to your entire user account |
| `--add safe.directory` | Adds an entry to Git's whitelist of directories it's allowed to operate in |
| `C:/Users/example` | The specific folder being whitelisted |

---

## Why Is This Needed?

Git introduced [**ownership checks** (in v2.35.2+)](https://support.atlassian.com/bitbucket-cloud/kb/git-command-returns-fatal-error-detected-dubious-ownership/) as a security measure. If Git detects that the directory is owned by a *different* user than the one running the command, it refuses to operate and throws an error like:

```
fatal: unsafe repository ... is owned by someone else
```

This commonly happens when:
- You're on Windows and there's a mismatch between the file owner and the current user
- You're using WSL (Windows Subsystem for Linux)
- Files were created by a different account (e.g., an admin vs. a regular user)
- You're running Git inside a Docker container

---

## What It Does in Practice

It adds this line to your `~/.gitconfig`:

```ini
[safe]
    directory = C:/Users/example
```

After running it, Git will stop complaining about ownership for that specific repo and let you run commands like `git status`, `git pull`, etc. normally.

# `git config --global core.autocrlf input`

This sets Git's line ending conversion behavior. With `input`:

- **On commit**: Git converts `CRLF` → `LF` (Windows-style line endings are normalized to Unix-style)
- **On checkout**: Git does nothing — files are checked out with whatever line endings are stored in the repo (no conversion back to CRLF)

Recommended for Mac/Linux developers, or cross-platform teams using a Unix-style repo. Ensures you never accidentally commit Windows `CRLF` line endings, but doesn't force-convert files on your working copy.

---

# `git config --global core.safecrlf true`

This is a safety check. With `true`:

- Before converting line endings, Git verifies the conversion is **reversible**
- If a file would be corrupted or changed irreversibly by the CRLF conversion, Git **rejects the commit** with an error
- Protects binary files or files with mixed line endings from being silently mangled

**Example error:**
```
fatal: CRLF would be replaced by LF in somefile.txt
```

---

## Together

These two settings work well as a pair:

| Setting | Effect |
|---|---|
| `autocrlf input` | Normalize CRLF → LF on commit, leave checkouts alone |
| `safecrlf true` | Abort if any conversion would be lossy/irreversible |