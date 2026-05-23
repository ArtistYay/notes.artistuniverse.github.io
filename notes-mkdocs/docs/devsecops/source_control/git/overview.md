---
tags:
  - Version Control
  - DevOps
---

# Core Vocabulary (Know These Cold)

| Term | What It Actually Means |
|---|---|
| **Repository (repo)** | The project folder tracked by Git, locally and/or in the cloud (GitHub, Azure DevOps) |
| **Clone** | Make a local copy of a remote repository |
| **Branch** | A lightweight construct that groups commits together so you can work in isolation |
| **Commit** | A saved snapshot of changes, includes *who*, *when*, *exactly what lines changed*, and a description |
| **Stage / Staging Area** | The holding area before a commit (`git add` moves files here) |
| **Push** | Send your local commits on the current branch to the remote |
| **Pull** | Bring remote changes for the current branch into your local copy |
| **Fetch** | Collect the index of everything that's happened remotely (branches, commits) without checking anything out |
| **Merge** | Integrate changes from one branch into another |
| **Pull Request (PR)** | A **review** , not an approval. A formal request for someone to review your code before merging |
| **Protected Branch** | A branch (usually `main`) that requires a passing PR review before anyone can push to it |
| **Merge Conflict** | What happens when two branches edited the same lines of code differently, Git can't auto-resolve it |
| **Stash** | Temporarily shelve uncommitted changes so you can switch context, then restore them later |

> **Critical distinction:** A PR is a **review**, not an approval. The reviewer makes an independent judgment. When you say "approve my code," you're asking for a rubber stamp. When you say "review my code," you're asking for a discussion. The language matters.

---

# The Two Branching Strategies

## Trunk-Based Development ✅ (Preferred)
- One protected branch: `main`
- Everyone cuts short-lived feature branches off `main`
- Merge back into `main` frequently via PR
- Enables flow, fast feedback, and continuous learning, the three fundamentals of DevOps

## Git Flow ❌ (Avoid when possible)
- Multiple protected branches (`main`, `develop`, `release`, `hotfix`, etc.)
- Every change requires a PR at multiple layers
- Slows down delivery, delays feedback, increases merge conflict risk

---

# Workflows

## Workflow A: Starting From Scratch (Local)
```
git init          = Initialize a new repo in your current folder (rare, usually you clone instead).
git add .         = Stage all files
git commit -m ""  = Commit staged files with a message
git push          = Push to remote
```

## Workflow B: Standard Team Workflow (Clone-Based)
```
git clone <url>           = Pull down the remote repo
git checkout -b <name>    = Create and switch to a new branch (never work directly on main)
git add <file>            = Stage specific file
git add .                 = Stage everything
git commit -m "message"   = Commit with a description
git push                  = Push your branch to remote

Open a Pull Request for review in GitHub / Azure DevOps

```

> **Common mistake:** Cloning and immediately starting work without cutting a branch. If you've already committed to `main` locally, you can still cut a branch at that point, `git checkout -b <name>`, and push it. Your commits travel with you. The branch is just a reference.

---

# Key Git Commands Reference

| Command | What It Does |
|---|---|
| `git init` | Initialize a new local repo |
| `git clone <url>` | Clone a remote repo locally |
| `git checkout -b <name>` | Create and switch to a new branch |
| `git checkout <name>` | Switch to an existing branch |
| `git add <file>` | Stage a specific file |
| `git add .` | Stage all changed files |
| `git commit -m "message"` | Commit staged changes with a description |
| `git push` | Push current branch to remote |
| `git pull` | Pull remote changes into current branch |
| `git fetch` | Sync the index of all remote branches/commits locally (additive only) |
| `git fetch --prune` | Sync the index AND remove references to deleted remote branches |
| `git merge <branch>` | Merge another branch into your current branch |
| `git stash` | Shelve uncommitted changes temporarily |
| `git stash pop` | Restore the most recent stash |
| `git reset` | Undo all uncommitted changes back to the last commit |
| `git reset <commit-id>` | Undo everything back to a specific commit (destructive) |
| `git revert <commit-id>` | Undo a specific past commit by creating a *new* commit that reverses it (non-destructive, preferred) |
| `git status` | Show what's staged, unstaged, and untracked |
| `git log` | Show commit history |
| `git config --global user.name "username"` | Set your Git display name |
| `git config --global user.email "you@users.noreply.github.com"` | Set your Git email (use GitHub no-reply to avoid exposure) |

---

# Fetch vs. Pull vs. Prune

**Fetch**
- Downloads the *index* (metadata) of all remote activity, branches created, commits made
- Does **not** check out or modify any of your files
- Additive only, keeps building up the local reference map
- Many IDEs auto-fetch every few minutes in the background

**Pull**
- Actually integrates remote changes into your *currently checked out branch*
- Always branch-specific, it is not pulling from `main`, it is pulling from whatever branch you have checked out

**Prune** (always pair with fetch)
- Removes local references to remote branches that have been deleted
- Does **not** delete branches you have checked out locally, only cleans up stale index references
- Use: `git fetch --prune`

---

# Reset vs. Revert

| | `git reset` | `git revert` |
|---|---|---|
| **What it does** | Undoes changes back to a point in history | Undoes a specific past commit by creating a new commit |
| **Modifies history?** | Yes, destructive | No, adds a new commit on top |
| **When to use** | Your current branch is a mess and nothing is worth keeping | A specific past commit was bad, but everything after it is fine |
| **Best for** | AI-assisted coding gone wrong, bad debugging paths | Reverting a deployed change without rewriting history |

> Revert is almost always the safer choice on shared branches.

---

# Pull Requests, How to Do Them Right

1. **Write a commit message that describes what changed and why**, not just "fix" or "update"
2. Your reviewer is checking: Did you solve the right problem? Does it meet the story requirements? Is the code sound?
3. Expect a ~95% merge rate, if PRs are constantly rejected, something is wrong with planning or communication, not the review process
4. When reviewing someone else's PR: check out their branch locally, run it, then give feedback, don't just read the diff
5. Both the author and the reviewer share ownership of what gets merged

---

# Merge Conflicts, Prevention First

**How conflicts happen:** Two people edit the same lines of the same file on different branches.

**How to prevent them:**
- Plan work so team members are not working on the same files simultaneously
- Merge `main` back into your branch regularly (a few times per day on active teams)
- Communicate when your work overlaps with someone else's

**How to resolve them when they happen:**
- Don't panic, Git will mark the conflict in the file
- Review both versions, pick the correct one (or combine them)
- Stage the resolved file and commit

---

# Security Practices in Git

- **Never commit credentials, passwords, or API keys**, not even temporarily
- **Never commit a email to a public repo**, use your GitHub no-reply address: `username@users.noreply.github.com`
- Use `.gitignore` to exclude sensitive files from being tracked
- Rotate credentials immediately if they are ever committed, do not assume "I deleted the file" is enough (Git history persists)
- Protected branches + PR requirements are your enforcement layer, configure them on every repo

---

# VS Code Git Integration, Quick Reference

| UI Element | What It Does |
|---|---|
| Source Control panel (left sidebar) | Shows staged, unstaged, and untracked changes |
| `U` next to a file | Untracked, not yet added to Git |
| `+` next to a file | Stages that file (`git add`) |
| Commit message box | Write your commit description here |
| **Sync Changes button** | This is a `git pull` + `git push` combined, not a real Git command. Don't use this vocabulary with teammates. |
| Cloud icon (bottom bar) | Publish branch to remote |
| GitLens extension (bottom) | Visualizes commit history, blame, branches , highly recommended |

---

# Mental Models

**Branch = a shoebox of commits.** The branch doesn't hold files, it holds a chain of commits. You can move that shoebox (checkout a different branch) and your uncommitted work follows you.

**Commit = a checkpoint.** Every commit is a permanent, unique snapshot. Moving forward in Git means building new commits, you don't erase old ones, you build on top of them.

**Stash = grandma's candy dish.** Swipe a few pieces (your changes), pocket them for later, and come back to finish what you were doing.

**Fetch = running a sweep.** You're not grabbing anything, you're just updating your map of what exists out there.

**Revert = a counter-move.** Git plays the exact opposite of whatever that commit did, in a new commit. History stays intact.