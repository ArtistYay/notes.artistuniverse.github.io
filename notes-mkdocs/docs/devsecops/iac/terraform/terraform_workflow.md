---
tags:
  - Infrastructure as Code
  - DevOps
---

# Terraform Workflow & Lifecycle

## The Three-Phase Cycle: Write, Plan, Apply

- **Write** — you edit `.tf` files. Terraform isn't involved yet, this is just you expressing what you want in HCL.
- **Plan** — Terraform compares your configuration (desired state) against the state file (what it believes exists) and produces an execution plan: what it will create, modify, or destroy, and in what order.
- **Apply** — Terraform executes the plan and records the result in an updated state file.

This cycle repeats every time you need to change something. Day zero, with nothing deployed yet, the plan is simple: create everything. Later, changing one field (say, resizing a database from small to medium) can cascade: Terraform has to figure out what depends on what and sequence the changes correctly, for example, creating a new VM before it can update a load balancer that needs the new VM's IP.

Terraform will never make a change that wasn't in the plan you reviewed. That's the core safety guarantee of the workflow.

## Core Commands

| Command | What it does | When to Use |
|---|---|---|
| `terraform init` | Sets up the working directory: downloads providers and modules, configures the backend. Run this first, and again any time you add a provider or module. | Starting a new project, cloning an existing one, or after editing `required_providers` or a `module` block. |
| `terraform validate` | Checks configuration syntax without touching any infrastructure. | A quick sanity check while you're writing, or as an early, fast-failing step in CI before `plan`. |
| `terraform fmt` | Reformats `.tf` files to the canonical style. | Before committing, so diffs stay clean and consistent across the team. Good to run as a pre-commit hook. |
| `terraform plan` | Generates and shows the execution plan. | Any time you've changed configuration and want to see what would happen before touching real infrastructure. |
| `terraform plan -out=tfplan` | Saves the plan to a file, so what gets reviewed is exactly what gets applied later. | Team or CI workflows where someone reviews or approves a plan before it's applied. |
| `terraform apply` | Applies changes. Without a saved plan file, it generates one and prompts for confirmation. | Local, interactive work where you're comfortable reviewing the plan Terraform shows you on the spot. |
| `terraform apply tfplan` | Applies a previously saved plan, no confirmation prompt. | Applying exactly what was already reviewed via `plan -out`, typically in CI/CD. |
| `terraform destroy` | Destroys everything Terraform manages, essentially a plan in reverse. | Tearing down a temporary environment, or fully decommissioning a piece of infrastructure. |

## The Dependency Lock File

`terraform init` also creates or updates `.terraform.lock.hcl`. It records the exact provider versions and cryptographic checksums Terraform selected, so re-running `init` later picks the same versions rather than silently upgrading.

- Commit this file to version control. It's the Terraform equivalent of `package-lock.json` or `go.sum`.
- If you need to intentionally move to a newer provider version, run `terraform init -upgrade` and review the diff before committing.
- In CI, run `terraform init -lockfile=readonly`. This makes init fail loudly if the lock file and configuration disagree, instead of silently rewriting the lock file with different versions than what was tested locally.

## Declarative vs. Imperative, and Idempotence

Terraform is declarative: you describe the desired end state, and it works out how to get there, rather than scripting each step. Paired with that is idempotence: running the same configuration against infrastructure that already matches it should make no changes at all. Terraform achieves this by comparing your configuration against the recorded state and only acting on the differences.

## Day 0 / Day 1 / Day 2+

It's useful to separate the infrastructure lifecycle into stages rather than treating deployment as a single event:

- **Day 0** — foundational setup. Cloud account structure, landing zones, core networking, guardrails.
- **Day 1** — initial deployment of the actual application infrastructure: compute, database, load balancer, etc.
- **Day 2+** — everything after that, for as long as the infrastructure lives. Patching, resizing, scaling, adding new components, responding to new compliance requirements, decommissioning when the application is retired.

Most of an infrastructure's life is spent in day 2+. Because it's all defined in code, day 2+ changes (bump a database tier, patch a base image, add a DNS record) become a matter of editing the definition and re-running `plan`/`apply`, instead of a bespoke manual task each time.

## Policy as Code in the Pipeline

Because `plan` happens before `apply`, there's a natural checkpoint to insert automated policy checks: does this plan open a security group to the whole internet, turn off encryption, or leave only one instance behind a load balancer? Tools like Sentinel or Open Policy Agent evaluate the plan against rules like this and can block the run before anything actually changes. See [HCP Terraform](hcp_terraform.md) for how this is wired up in practice.

## Tips from the Community

- **Look for unexpected replacements in the plan output, not just the counts.** A single changed attribute (like an AMI ID) can force a full destroy-and-recreate instead of an in-place update. The `+/-` (create then destroy) versus `-/+` (destroy then create) symbols in the plan output tell you which order Terraform will use, worth reading closely before approving.
  Source: [How to Understand the Terraform Core Workflow – OneUptime](https://oneuptime.com/blog/post/2026-02-23-how-to-understand-the-terraform-core-workflow-write-plan-apply/view)

- **Use `-target` sparingly.** You can plan or apply against a single resource for a surgical fix, but it can miss dependency changes elsewhere in the graph and leave your state and configuration quietly out of sync. Treat it as an exception, not a habit.
  Source: [How to Understand the Terraform Core Workflow – OneUptime](https://oneuptime.com/blog/post/2026-02-23-how-to-understand-the-terraform-core-workflow-write-plan-apply/view)

- **Always save plans in CI/CD with `-out`.** Running `terraform plan -out=tfplan` and then applying that exact file guarantees what a reviewer approved is what actually gets executed, rather than trusting that nothing changed between review and apply.
  Source: [How to Understand the Terraform Core Workflow – OneUptime](https://oneuptime.com/blog/post/2026-02-23-how-to-understand-the-terraform-core-workflow-write-plan-apply/view)

- **A stale or unpinned build environment is a common source of "it worked yesterday" failures.** Prep the CI environment ahead of time (Terraform CLI version, provider plugins, machine images), and consider a shared plugin cache, since Terraform normally looks for plugins in a project-local `.terraform` directory that's unique to each CI job.
  Source: [A best practices guide for Terraform CI/CD workflows – Buildkite](https://buildkite.com/resources/blog/best-practices-for-terraform-ci-cd/)

- **`.terraform.lock.hcl` conflicts are usually a merge problem, not a Terraform bug.** If two branches add or bump different providers and get merged without re-running `init`, the lock file can end up inconsistent. The fix is almost always `terraform init -upgrade`, review the resulting diff, then commit.
  Source: [Terraform Lock File Demystified – EzyInfra](https://ezyinfra.dev/blog/terraform-lock-file)