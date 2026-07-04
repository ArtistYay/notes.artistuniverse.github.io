---
tags:
  - Cybersecurity
  - Microsoft Azure
  - DevOps
---

# Why I Built This

Most companies have CI/CD pipelines and a SIEM, but those two things don't talk to each other. The pipeline knows what got deployed and whether it passed a scan. The SIEM knows something weird happened at runtime. Neither one has the other's context. That gap is what this project tries to close.

The Flask app generates structured JSON logs when endpoints are hit. Docker captures those logs, Azure Monitor ships them to Sentinel. GitHub Actions runs security gates (Trivy, Checkov, Bandit, Gitleaks) and generates its own pipeline events, scan results, deployment status, that also land in Sentinel. The Terraform modules are reusable templates with security baked in so devs don't have to figure out encryption, network rules, or identity from scratch. Azure Policy sits on top as a hard enforcement layer, even if someone edits a module and removes a control, the policy blocks the deployment before it reaches production.

I built this because I wanted to prove I understand how these pieces fit together, not just that I can click buttons in a portal. Anyone can enable Defender for Cloud. Not everyone can architect the pipeline that feeds it.

## Project mental model
```
Flask app    = the thing being protected
Docker       = the package it ships in
Pipeline     = the security checkpoint that package goes through
Azure        = where it runs in production
Sentinel     = the system watching it at runtime
```

---

# Phase 1: Flask App

## What I built
A minimal Flask API with one endpoint (`/health`) that returns structured JSON and writes logs to stdout.

## Why structured JSON logging?
Plain text logs are stored but not easily queryable. Structured JSON means every field (event, endpoint, status) becomes a named column in Sentinel, enabling detection rules without regex parsing.

## Key decisions

**Why Flask over FastAPI or Django?**
Tool selection framework to match complexity to the problem:
1. What does the app need to do?
2. What's the simplest tool that solves it?
3. Does the tool's complexity match the problem's complexity?

Flask was the answer. One endpoint, no concurrency requirements, FastAPI would be over-engineered; Django would be absurd.

**Why `host='0.0.0.0'`?**
`127.0.0.1` only listens on the local machine. `0.0.0.0` binds to every network interface. Without it, Docker's port mapping doesn't work even if the port is exposed.

**Why `debug=False` in production?**
Flask debug mode turns on an interactive Python console in the browser. If an attacker triggers an error, they get live code execution on the server. That's RCE.

**Why Gunicorn instead of `flask run`?**
Flask's built-in server handles one request at a time. Gunicorn is a WSGI (Web Server Gateway Interface) server that runs multiple worker processes so the app can handle concurrent requests. You can't use `flask run` inside a container anyway, the container needs a direct command to start the app on its own.

## How logs flow to Sentinel
```
Flask app → writes JSON to stdout → Docker captures stdout →
Azure Monitor Agent collects it → Sentinel ingests it
```
The app never talks to Sentinel directly.

---

# Phase 2: Docker

## What I built
A Dockerfile that packages the Flask app into a production-ready container image.

## Key decisions

**Why Alpine as the base image?**
`python:3.12-alpine` is under 50MB vs 900MB+ for the standard Python image. Smaller image = smaller attack surface = fewer CVEs for Trivy to find.

**Why copy `requirements.txt` before the app code?**
Docker layer caching. Dependencies change rarely, app code changes constantly. Copy requirements first, install them, then copy the app, rebuilds skip straight to the app copy step instead of reinstalling everything from scratch every time.

**Why Gunicorn in the CMD?**
Production-grade WSGI server. `flask run` is not appropriate inside a container. Gunicorn binds to `0.0.0.0:5000` with 4 workers and starts the Flask instance named `app` inside `app.py`.

## How Docker feeds the rest of the pipeline
- Trivy scans the **image**, not raw Python files
- Azure Container Registry stores the **image**
- Azure Container Apps runs the **image**
- Defender for Containers monitors the running **container**

## Errors hit
- `permission denied` on Docker socket — fixed with `sudo usermod -aG docker $USER`

---

# Phase 3: Terraform

You can create nested subfolders in one command using brace expansion:
`mkdir -p terraform/modules/{network,compute,storage,identity,policy}`
The shell expands the braces before `mkdir` ever runs.

**Module structure — every module has three files:**
- `main.tf` — what gets built
- `variables.tf` — what the module accepts as inputs (how you make it reusable)
- `outputs.tf` — what the module exposes after it runs, so other modules can reference it

Modules talk to each other through outputs. The network module doesn't know anything about compute internals, and compute doesn't know about network internals. Clean interfaces.



## Network Module

- Used [validation](https://developer.hashicorp.com/terraform/language/validate) on variables so wrong region deployments and naming issues get caught at `terraform plan` time, before anything touches Azure.

- Azure accepts a list of address spaces so used [`list(string)`](https://oneuptime.com/blog/post/2026-02-23-how-to-use-the-tolist-function-in-terraform/view) for `vnet_address_space` so others can pass multiple ranges if needed.

- Kept the subnet inline inside the VNet resource to reduce lines of code. Had to use `tolist()` to grab the first subnet's ID for the NSG association — the inline block exports a set, not a single value.

- Used multi-variable validation to keep the code compact.

## Storage Module

- Need to host the container image somewhere, went with [Basic SKU](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-skus) for ACR because this is a side project.

# Errors hit

1. Committed the Terraform scaffold on main locally and tried to push but GitHub rejected it because of branch protection.

2. Created a GitHub Issue to track the Terraform work. Issues are how teams track what needs to be done. Attaching a branch to an issue links the work to the task. **MAKE SURE WHEN CHECKING OUT A BRANCH YOU INCLUDE THE `-b` FLAG!!**

3. Created a terraform branch but couldn't switch to it because I had uncommitted local changes that would've been overwritten. Git protects me from losing work.

4. Ran `git reset HEAD~1` which undid my last commit but kept the file changes locally. This put me back to a clean state to switch branches.

5. Tried `git stash` to temporarily save my changes and it threw an error because after the reset there was nothing staged to stash.

6. Switched to the terraform branch, made my changes there, and committed.

7. Git rejected the push because the local branch wasn't linked to a remote branch yet, that's the `--set-upstream` error. Running `git push --set-upstream origin terraform` tells Git "this local branch lives at origin/terraform."

8. GitHub blocked the push because my commits had my real email in them. Fixed with `git config`.

# References:
- https://www.howtogeek.com/devops/how-to-move-changes-to-another-branch-in-git/
- https://stackoverflow.com/questions/7217894/moving-changed-files-to-another-branch-for-check-in
- https://stackoverflow.com/questions/38200616/git-stash-throws-error-no-local-changes-to-save
- https://medium.com/@python-javascript-php-html-css/resolving-githubs-push-declined-due-to-email-privacy-restrictions-issue-c346a9cf1da0