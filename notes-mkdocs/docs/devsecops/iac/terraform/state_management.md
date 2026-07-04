---
tags:
  - Infrastructure as Code
  - DevOps
---

# State Management

## What State Actually Is

Terraform's state file (`terraform.tfstate`, JSON-formatted) is the map between your configuration and the real-world resources it manages, plus metadata: resource IDs, attributes, and dependency information. Without it, Terraform has no way to know what already exists, so it can't tell what needs to be created, changed, or destroyed.

- Stored locally by default (fine for solo experiments, not for anything else).
- Should be stored **remotely** for any team or production use: AWS S3, Azure Blob Storage, Google Cloud Storage, or HCP Terraform.
- **Never edit it by hand.** Use `terraform state` subcommands instead.

## Remote State and Locking

Local state breaks down the moment more than one person is involved: merge conflicts, accidental deletion, no versioning, and secrets sitting on individual laptops. Remote state fixes this by centralizing storage and adding:

- **Locking** — prevents two people (or two CI jobs) from running `apply` against the same state at once. Without it, both can read the same state, both try to create the same resource, and you end up with duplicated infrastructure and a corrupted state file.
- **Versioning** — enables rollback if state gets corrupted or a bad change gets applied.
- **Encryption** — state can contain sensitive values (passwords, keys) in plaintext, so encrypt at rest and in transit, and restrict access.

A typical AWS setup pairs an S3 bucket (with versioning and encryption enabled) with a DynamoDB table for locking. Azure Blob Storage and Google Cloud Storage have their own equivalents built in.

## Useful `terraform state` Commands

| Command | What it does |
|---|---|
| `terraform state list` | Lists all resources tracked in state. |
| `terraform state show <address>` | Shows the attributes of a specific resource in state. |
| `terraform state mv <src> <dst>` | Renames or moves a resource within state, without touching real infrastructure. |
| `terraform state rm <address>` | Removes a resource from state without destroying it. Use this when a resource is now managed elsewhere. |
| `terraform import <address> <id>` | Brings an existing, unmanaged resource under Terraform's management. |
| `terraform refresh` | Updates state to match real-world infrastructure. `plan` does this implicitly, but running it explicitly can surface drift on its own. |

## Drift

Drift is any gap between what your state file says exists and what's actually running, usually caused by manual changes made outside of Terraform. `terraform plan` is your drift detector: it shows you exactly where reality diverged from your last-known state. In CI, this can be scheduled to run periodically and alert on unexpected changes, rather than only surfacing drift the next time someone happens to run `apply`.

## Splitting State

Large, monolithic state files get slow and increase blast radius, one bad apply can touch everything. Common ways to split:

- **By environment** — separate state per dev/staging/prod.
- **By concern/service** — networking, compute, and data layers each get their own state, wired together with `terraform_remote_state` or, better, a native data source that queries the provider directly (see the tip below).

## Tips from the Community

- **Prefer a native cloud data source over `terraform_remote_state` for cross-team sharing.** The `terraform_remote_state` data source requires read access to another team's *entire* state file, which can expose outputs that have nothing to do with what you actually need. Where possible, use something like `aws_vpc` or `aws_subnets` to query the provider's API directly and get back only the specific values you need.
  Source: [Terraform Remote State: Setup, Locking & Best Practices – Spacelift](https://spacelift.io/blog/terraform-remote-state)

- **A stuck lock is a signal to investigate, not a reason to force-unlock reflexively.** If `apply` reports a lock error, first confirm nobody else is actually running Terraform against that state. Only force-unlock once you're certain the lock is orphaned (the process that held it crashed), since force-unlocking during a genuine in-progress write will corrupt the state.
  Source: [How to Handle Terraform State Conflicts and Locking Issues – OneUptime](https://oneuptime.com/blog/post/2026-02-12-terraform-state-conflicts-locking-issues/view)

- **Use `-refresh-only` when the drift is intentional and reality should win.** If someone made a change outside of Terraform on purpose, `terraform apply -refresh-only` updates the state to reflect the real infrastructure without trying to revert it back to match your configuration.
  Source: [How to Handle Terraform State Conflicts and Locking Issues – OneUptime](https://oneuptime.com/blog/post/2026-02-12-terraform-state-conflicts-locking-issues/view)

- **Splitting state can create dangling cross-references if you're not careful with `terraform state mv`.** One team moved a monolithic state into smaller ones, but moved a resource that referenced another resource still sitting in the old state, before the dependency itself had moved. Terraform couldn't resolve the reference and refused to plan or apply either state until it was fixed by hand. Move dependencies together, or move the dependency first.
  Source: [Terraform State Management: Remote Backends, Locking, and Recovery – CloudToolStack](https://cloudtoolstack.com/blog/terraform-state-management)

- **Mark sensitive outputs as `sensitive` and keep secrets out of state where you can.** State stores resource attributes in plaintext by default, including anything you output. Flagging sensitive outputs and leaning on an external secrets manager instead of storing secrets inline reduces what's exposed if the state file itself is ever compromised.
  Source: [Terraform State Files Best Practices – Scalr](https://scalr.com/learning-center/terraform-state-files-best-practices)