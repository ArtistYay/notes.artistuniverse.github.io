---
tags:
  - Infrastructure as Code
  - DevOps
---

# HCP Terraform (formerly Terraform Cloud) & Enterprise

## What Problem This Solves

Terraform Community Edition (the free, local CLI tool) works well for one or two people on a small project. Once you're operating across many teams and hundreds of workspaces, new problems show up that the CLI alone doesn't solve: who has access to change what, how do you share state and modules safely, how do you enforce guardrails before infrastructure gets provisioned, and how do you get visibility across every workspace at once.

HCP Terraform (SaaS) and Terraform Enterprise (self-hosted) are HashiCorp's managed layer on top of core Terraform that address this. Key capabilities:

- **Remote runs** — Terraform executes on HashiCorp's infrastructure (or your own private agents), not on individual laptops, giving every run a consistent environment.
- **Shared, locked state** — built-in remote state storage with locking, so teams don't have to stand up their own S3+DynamoDB backend.
- **Workspaces** — one workspace maps to one Terraform configuration/state combination. Not the same concept as CLI-native `terraform workspace`.
- **Private module & provider registries** — publish internal modules for teams to reuse instead of everyone reinventing the same patterns.
- **Role-based access control** — restrict who can view, plan, or apply against which workspaces.
- **VCS integration** — connect a workspace to a Git repository so pushes automatically trigger runs.
- **Policy as code (Sentinel / OPA)** — see below.

## Workspaces

A workspace holds one configuration's variables, state, and run history. It can be connected to:

- A **VCS repository** (most common) — pushes trigger runs automatically.
- The **CLI-driven workflow** — you still run `terraform plan`/`apply` locally, but state lives remotely.
- The **API** — for custom automation.

Execution modes: **Remote** (runs on HCP Terraform's own disposable VMs, enables Sentinel/cost estimation/notifications), **Local** (state stored remotely, but the actual run happens on your machine via the CLI), or **Agent** (runs happen on your own lightweight HCP Terraform agent, for private or on-prem infrastructure).

## Policy as Code: Sentinel and OPA

Sentinel is HashiCorp's own policy-as-code framework; Open Policy Agent (OPA) is the more widely adopted alternative in the broader ecosystem. Both plug into the same checkpoint: after `plan`, before `apply`.

- Policies are grouped into **policy sets**, which can be applied globally or scoped to specific projects/workspaces.
- Policy sets are usually connected to a VCS repository, so policy changes go through the same code review process as everything else.
- Enforcement levels typically range from advisory (warns but doesn't block) up to hard-mandatory (blocks the run, no override).
- A policy can check things like: are all EC2 instances tagged, is the instance type in the approved list, is a change happening outside an approved maintenance window.

```hcl
# sentinel.hcl
policy "restrict-instance-types" {
  source             = "./policies/restrict-instance-types.sentinel"
  enforcement_level  = "hard-mandatory"
}
```

## Run Triggers

Run triggers let a workspace automatically queue a run when a run in a different (source) workspace succeeds. This is how you wire together dependent layers, for example, triggering the compute workspace's plan automatically once the networking workspace applies successfully, without manual coordination between teams.

## Tips from the Community

- **Start new policies as advisory, not hard-mandatory.** Deploying a brand-new policy set in advisory mode first lets you see its real-world impact (how many existing runs would it have blocked) before you turn it into something that can actually stop a deployment. Going straight to hard-mandatory risks blocking legitimate work you didn't anticipate.
  Source: [How to Use Sentinel Policy Sets in HCP Terraform – OneUptime](https://oneuptime.com/blog/post/2026-02-23-how-to-use-sentinel-policy-sets-in-hcp-terraform/view)

- **Keep policy sets in their own repository, separate from infrastructure code.** This lets policies version independently of the Terraform configuration they're checking, and makes it easier to review and roll back a policy change without touching infrastructure code at all.
  Source: [How to Use Sentinel Policy Sets in HCP Terraform – OneUptime](https://oneuptime.com/blog/post/2026-02-23-how-to-use-sentinel-policy-sets-in-hcp-terraform/view)

- **HCP Terraform's Free tier caps you at one policy set of up to five policies.** If you're prototyping policy as code on a free org and hit a wall, that limit (not a bug) is usually why. Connecting a policy set to a VCS repository, or creating policy set versions via the API, requires the Standard tier or above.
  Source: [Upload your Sentinel policy set to HCP Terraform – HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/policy/sentinel-cloud-integration)

- **A policy set can only contain policies from one framework at a time, but a workspace can use several policy sets.** If you want both Sentinel and OPA checks running against the same workspace, that's supported, just as two separate policy sets attached to the same workspace rather than mixed inside one.
  Source: [HCP Terraform policy enforcement overview – HashiCorp Developer](https://developer.hashicorp.com/terraform/cloud-docs/workspaces/policy-enforcement)

- **Weigh the dependency on HCP Terraform's availability before committing fully.** If HCP Terraform has an outage, you can't run Terraform against workspaces that depend on it for remote execution. Some teams keep the ability to fail over to a self-managed backend, but straddling both a managed and self-managed setup at once tends to create more confusion than it's worth, most teams pick one.
  Source: [Terraform State Management: Remote Backends, Locking, and Recovery – CloudToolStack](https://cloudtoolstack.com/blog/terraform-state-management)