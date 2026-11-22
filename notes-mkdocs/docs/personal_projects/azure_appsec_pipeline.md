---
tags:
  - Cybersecurity
  - Microsoft Azure
  - DevOps
---

## Why I Built This

Most companies have CI/CD pipelines and a SIEM, but those two things don't talk to each other. The pipeline knows what got deployed and whether it passed a scan. The SIEM knows something weird happened at runtime. Neither one has the other's context. That gap is what this project tries to close.

The Flask app writes structured JSON logs when endpoints are hit. Container Apps ships whatever the container prints to Log Analytics, and Sentinel runs detection rules on top of that. GitHub Actions runs the security gates (Bandit, Gitleaks, Grype, Checkov) and tags every image with the commit that built it, so when Sentinel flags something, the running image traces back to one commit and one pipeline run. The Terraform modules are reusable templates with security baked in so devs don't have to figure out encryption, network rules, or identity from scratch. Azure Policy sits on top as a hard enforcement layer, even if someone edits a module and removes a control, the policy blocks the deployment before it reaches production.

I built this because I wanted to prove I understand how these pieces fit together, not just that I can click buttons in a portal. Anyone can enable Defender for Cloud. Not everyone can architect the pipeline that feeds it.

### Project mental model
```
Flask app    = the thing being protected
Docker       = the package it ships in
Pipeline     = the security checkpoint that package goes through
Azure        = where it runs in production
Sentinel     = the system watching it at runtime
```

---

## Phase 1: Flask App

### What I built
A minimal Flask API with one endpoint (`/health`) that returns structured JSON and writes logs to stdout.

### Why structured JSON logging?
Plain text logs are stored but not easily queryable. Structured JSON means every field (event, endpoint, status) becomes a named column in Sentinel, enabling detection rules without regex parsing.

### Key decisions

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

### How logs flow to Sentinel
```
Flask app → writes JSON to stdout → Container Apps environment picks it up →
Log Analytics (ContainerAppConsoleLogs_CL table) → Sentinel analytics rule queries it
```
The app never talks to Sentinel directly. Originally wrote "Azure Monitor Agent collects it" here, that was wrong. There's no agent involved, the Container Apps environment sends console output to the workspace on its own.

---

## Phase 2: Docker

### What I built
A Dockerfile that packages the Flask app into a production-ready container image.

### Key decisions

**Why Alpine as the base image?**
`python:3.12-alpine` is under 50MB vs 900MB+ for the standard Python image. Smaller image = smaller attack surface = fewer CVEs for the image scanner to find.

**Why copy `requirements.txt` before the app code?**
Docker layer caching. Dependencies change rarely, app code changes constantly. Copy requirements first, install them, then copy the app, rebuilds skip straight to the app copy step instead of reinstalling everything from scratch every time.

**Why Gunicorn in the CMD?**
Production-grade WSGI server. `flask run` is not appropriate inside a container. Gunicorn binds to `0.0.0.0:5000` with 4 workers and starts the Flask instance named `app` inside `app.py`.

### How Docker feeds the rest of the pipeline
- Grype scans the **image**, not raw Python files
- Azure Container Registry stores the **image**
- Azure Container Apps runs the **image**
- Sentinel watches the running **container** through its logs

Defender for Containers was the original plan for that last line. Dropped it once I read the Container Apps security baseline: its runtime protection covers Kubernetes clusters, not Container Apps.

### Errors hit
- `permission denied` on Docker socket, fixed with `sudo usermod -aG docker $USER`

---

## Phase 3: Terraform

You can create nested subfolders in one command using brace expansion:
`mkdir -p terraform/modules/{network,compute,storage,identity,policy}`
The shell expands the braces before `mkdir` ever runs.

**Module structure, every module has three files:**
- `main.tf`, what gets built
- `variables.tf`, what the module accepts as inputs (how you make it reusable)
- `outputs.tf`, what the module exposes after it runs, so other modules can reference it

Modules talk to each other through outputs. The network module doesn't know anything about compute internals, and compute doesn't know about network internals. Clean interfaces.

### Network Module

- Used [validation](https://developer.hashicorp.com/terraform/language/validate) on variables so wrong region deployments and naming issues get caught at `terraform plan` time, before anything touches Azure.

- Azure accepts a list of address spaces so used [`list(string)`](https://oneuptime.com/blog/post/2026-02-23-how-to-use-the-tolist-function-in-terraform/view) for `vnet_address_space` so others can pass multiple ranges if needed.

- Kept the subnet inline inside the VNet resource to reduce lines of code. Had to use `tolist()` to grab the first subnet's ID for the NSG association, the inline block exports a set, not a single value.

- Used multi-variable validation to keep the code compact.

### Storage Module

Need to host the container image somewhere, went with [Basic SKU](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-skus) for ACR because this is a side project. Worth noting for later: Basic doesn't support private endpoints, so a real production setup would use Premium to keep ACR inside the VNet with no public exposure.

Added an `environment` variable and tied `acr_sku` to it with a validation block. If `environment == "production"`, `acr_sku` has to be `Premium`, no exceptions. That way the SKU choice isn't just a suggestion, it's enforced at `terraform plan` time. Same defense-in-depth idea as the network module's location validation.

Regex validation on `acr_name` took a second to get right. `regex()` needs two arguments, the pattern to match and the value to check it against. First attempt only had the pattern with no value, so it wasn't actually testing anything. `can()` wraps around it so a failed match returns `false` instead of throwing a hard error.

Tying `acr_sku` to `environment` meant using a ternary operator for the first time in this project:

```hcl
condition = var.environment == "production" ? var.acr_sku == "Premium" : true
```

Ternary = compact if/else in one line: `condition ? value_if_true : value_if_false`. Terraform's `validation` blocks only take a single expression, not a full if/else, so this shorthand is basically required once you're doing conditional validation. Reads as: if environment is production, sku has to be Premium, otherwise skip the check.

## Environments

Saw a LinkedIn post about a pattern I hadn't considered: one codebase, reusable modules, and separate `tfvars` files per environment instead of duplicating code for dev/qa/prod. `variables.tf` is the contract (what inputs a module accepts), `tfvars` is what fulfills it (the actual values). Same module, different inputs per environment.

Added an `environments/dev` and `environments/prod` folder at the root, each with its own `terraform.tfvars`. Not strictly needed for a project this size, but it's the pattern enterprises actually use and it's worth showing I understand it.

## Compute Module

Storage holds the image, but nothing runs it yet, that's what this module is for. Azure Container Apps was the target from day one instead of AKS, since Kubernetes is a whole learning curve on its own and this project is about the security pipeline, not container orchestration depth.

Went looking for a `azurerm_container_app` example on the registry and it required a `template` block I hadn't seen before, that's the actual runtime spec: what image, how much CPU, how much memory. Think of `azurerm_container_app_environment` as the neighborhood and the Container App as the house, `template` is the blueprint of what's actually living inside.

Learned the hard way that Terraform doesn't create a "container from an image". Docker already built and will eventually push that image. Terraform's job is standing up the Azure resource that knows how to pull and run whatever ends up in ACR. Also learned Container Apps requires a Log Analytics Workspace before it'll even accept an Environment, because the Environment needs a `log_analytics_workspace_id`. Turns out that's the same workspace Sentinel will eventually sit on top of.

**On `image` needing the full ACR path.** Just passing the image name wasn't enough. Azure needs `<login_server>/<image_name>:<tag>` or it assumes Docker Hub by default. Had to go back and add a `login_server` output to the storage module's `outputs.tf` that I'd missed the first time around.

**Almost made everything a variable with no guardrails.** First instinct was "let the dev pass anything in a tfvars file" but `cpu` and `memory` aren't like a name string, someone could set `cpu = 32` and rack up real cost, or set memory too low and the app just breaks. Landed on: everything's a variable, but the ones with real consequences (cpu, memory, sku, revision mode) get validated. Also learned Terraform validation happens at `plan` time, before anything touches Azure, Azure Policy is a second, slower layer that catches whatever bypasses Terraform. Not either/or, both.

**Reached for `range()` before realizing it was the wrong function.** Wanted to check if `cpu` fell inside a range and thought `range()` was the tool. it's actually for generating a list of discrete numbers to loop over, not for boundary checking, and doesn't handle decimals well anyway. `>=` and `<=` comparisons are what you want for "does this number fall between two bounds."

**Tied `container_memory` to `container_cpu`** instead of validating memory on its own, Azure Container Apps enforces roughly a 1:2 CPU-to-memory ratio (0.25 CPU → 0.5Gi, 0.5 → 1Gi, 1.0 → 2Gi, etc). Had to convert a string like `"1Gi"` into an actual number to compare it, which meant learning two new functions: `trimsuffix()` to strip the "Gi" off, `tonumber()` to convert what's left into a number Terraform can do math on. First pass didn't check that "Gi" was even present in the string, someone could pass `container_memory = "1"` with no unit and the check would silently pass. Added `endswith()` as a second condition to close that gap. Also had a typo (`containter_memory`) that would've thrown an undefined variable error, worth remembering to read variable names character by character, not just skim them.

**Container App needs an `identity` block to actually use the identity at runtime.** Wiring the identity module's output into `identity_ids` on the Container App isn't just for the role assignment, without this block the app has no way to authenticate to ACR at all when it tries to pull the image. Also needed a `registry` block with `server` (the ACR login server) and `identity` (the specific identity resource id, taking `[0]` out of the list since `identity_ids` wants the full list but `registry.identity` wants a single value). Learned identity_ids and registry.identity have different shapes even though they reference the same underlying value.

Decided not to add `custom_domain_verification_id` to the outputs, not relevant to this project's current scope, no custom domain plans. Noting it here so it reads as a decision, not a gap I missed.

## Policy Module

This is the enforcement layer that sits on top of everything else, even if a developer edits a module and removes a control, Azure Policy blocks the deployment at the Azure control-plane level before it ever reaches production. Same defense-in-depth logic as every validation block written today: Terraform validation catches mistakes fast and cheap at `plan` time, Policy catches whatever bypasses Terraform entirely (manual portal changes, a different tool, a compromised pipeline).

First draft was one giant policy definition trying to enforce location, ACR SKU, and the CPU/memory ratio all in one `anyOf` block. It worked, but it broke the Single Responsibility Principle I'd learned about earlier, one resource doing three unrelated jobs meant changing the CPU/memory rule would mean editing a huge nested JSON blob that also controlled location and SKU. Split it into three separate `azurerm_policy_definition` / `azurerm_policy_assignment` pairs instead, one per concern. Might separate it into files if I add any more.

**Used `jsonencode()` for the first time** to inject Terraform variables (`var.allowed_locations`, `var.allowed_acr_skus`) into the JSON heredoc blocks instead of hardcoding the same array three times across definitions and assignments. One source of truth instead of three copies that could drift out of sync.

**Scoped policy assignments to the resource group, not the subscription.** Same least-privilege reasoning as scoping the identity's role assignment to just the ACR instead of the whole resource group earlier. A subscription-wide policy would govern resources completely unrelated to this project. Resource-group scope keeps the blast radius limited to exactly what `azure-appsec-pipeline` deploys.

Outputs (the three policy definition ids) aren't consumed by any other module, added them purely for visibility via `terraform output`, and said so directly in each output's description rather than pretending they serve a wiring purpose they don't.

## Identity Module

First instinct was to look for a "managed identity" resource in the Terraform registry, turns out that's not a resource type on its own. Azure has two flavors: system-assigned (tied to the lifecycle of whatever resource it's attached to, created and destroyed automatically) and user-assigned (`azurerm_user_assigned_identity`, a standalone resource you create independently and attach to one or more things).

Almost went with system-assigned since it felt cleaner from a least-privilege angle, if the Container App gets torn down, the identity and its permissions go with it, no orphaned access sitting around.

But ran into a real ordering problem. With system-assigned, the identity doesn't exist until the Container App resource is actually applied, Azure generates it as a byproduct. That means the identity module can't create the identity itself, and a role assignment written ahead of time has nothing to point to yet. Worse, if I kept a separate `azurerm_user_assigned_identity` in the identity module anyway, I'd end up with two disconnected identities: one Azure auto-creates for the Container App, and one sitting unused in my module. No clean way to grant `AcrPull` to the one that's actually attached to the app.

Went with **user-assigned identity** instead. It exists as its own resource independent of Container Apps, so there's no chicken-and-egg problem, identity gets created first, compute references it, role assignment points to something that already exists. Trade-off is it doesn't get torn down automatically with the app, so if this were a real production setup I'd need a process for reviewing and cleaning up unused identities periodically. Noting that as a known gap rather than pretending it isn't one.

**Learned data sources are read-only.** A `data` block doesn't create anything in Azure, it looks up something that already exists and makes it available to reference. Different from a `resource` block, which builds something.

**Almost wrote a custom role for AcrPull.** Assumed I needed one since I was granting "certain permissions" to the identity. Wrong instinct, checked Azure's built-in roles first and `AcrPull` already exists as a built-in role with exactly one permission: `registries/pull/read`. Nothing more. Least privilege doesn't mean write a custom role, it means grant the smallest permission that does the job. Used the built-in role instead of building a `azurerm_role_definition` from scratch.

**Two separate resources for identity and role assignment, not one.** Same single-responsibility pattern as the NSG/NSG-association split in the network module. One resource maps to one Azure API object. An identity can have multiple role assignments (ACR pull, storage write, key vault read, all at once) so identity creation and permission granting have to be separate resources, combining them would mean one identity could only ever hold one permission. This is also why Terraform modules end up composable: you can attach the same identity to different role assignments across different modules without recreating the identity each time.

**Why does Terraform split things this way instead of bundling related actions into one resource?** It turns out there's an actual name for it, Single Responsibility Principle (SRP). SRP is specifically about not combining multiple responsibilities into one unit. Makes sense of a pattern I keep running into without naming it, one route per Flask endpoint, one concern per Terraform module, one job per Dockerfile layer.

**Scoped the role assignment to the ACR specifically, not the resource group.** `scope = var.acr_id`, not the resource group id. The identity can pull from this one registry and nothing else in the resource group. Also caught myself putting the ACR id into `principal_id` instead of the identity's own principal id, `principal_id` answers "who is receiving this permission," not "what resource are they getting access to."

**Locked `role_definition_name` down to `AcrPull` only** with a `contains()` validation, so the module can't accidentally be called with something overly permissive like `Owner`. Kept it as a variable instead of hardcoding so the module stays technically reusable, just constrained to the one role it's meant for.

## GitHub Actions OIDC Bootstrap (chicken-and-egg problem)

Hit a real ordering problem setting up authentication for GitHub Actions to run Terraform. The pipeline needs a resource group to deploy into. But the identity that lets the pipeline authenticate to Azure in the first place needs to live somewhere too, and it can't live in a resource group that Terraform itself is supposed to create, because then destroying that resource group would delete the very identity the pipeline needs to keep running.

This isn't a design flaw, it's just an unavoidable seam in any pipeline that manages its own infrastructure. Something always has to be bootstrapped manually before automation can take over.

**Decision:** create the resource group manually once via CLI, along with the GitHub Actions identity, its federated credential, and its role assignment, all outside of Terraform. Then switch the root `azurerm_resource_group.rg` resource block to a `data "azurerm_resource_group"` block instead. A data source only reads a resource, it never creates or destroys one. That means the resource group Terraform reports on is stable across every `plan`/`apply`/`destroy` cycle, and testing destroy no longer risks wiping out the GitHub Actions identity along with everything else.

**Known tradeoff:** whoever runs this project has to remember that the resource group is not managed by Terraform. Creating and destroying it is now a manual step, done once at setup, not something `terraform destroy` will ever touch. Documenting this clearly in the README so it isn't a silent gap.

**The actual sequence for setting this up:**
1. Create the resource group manually via CLI
2. Create the GitHub Actions identity inside it via CLI
3. Create the federated identity credential linking that identity to this specific repo and branch, this is what actually makes OIDC work instead of a stored secret
4. Grant that identity a role on the resource group so it can run Terraform (this turned into four roles later, see "Rebuilding from scratch" below)

On step 3, the `--subject` argument in the federated credential command isn't saying "this repo owns the identity," it's a trust condition. Azure will only accept a token as proof of this identity if the token's claim matches exactly, same repo, same branch. Tested this logic out loud: if someone forked the repo and tried running the same workflow, would Azure trust it? No, a fork has a different owner/repo path in its claim, so it fails the match even with identical workflow code. Azure isn't trusting the code, it's trusting the specific repo and branch path.

On step 4, Contributor scoped to the resource group is broader than strictly necessary (a fully custom role scoped to exactly the resource types this project creates would be tighter), but building that custom role means enumerating every resource type and action Terraform touches, Container Apps, ACR, VNets, NSGs, Managed Identities, Policy Definitions, Log Analytics, Role Assignments, and getting all of it right up front, or `terraform apply` fails partway through with a permission error instead of failing cleanly upfront. Went with Contributor scoped tightly to just this one resource group as a defensible middle ground for a portfolio project, documenting the custom-role version as a known next step rather than pretending Contributor is the final answer.

Official reference for the whole OIDC setup: [Authenticate to Azure from GitHub Actions by OpenID Connect (Microsoft Learn)](https://learn.microsoft.com/en-us/azure/developer/github/connect-from-azure-openid-connect)

**Testing the data source switch.** First `plan` after the change failed with "Resource Group was not found," even though it had definitely been created via `az group create` earlier. Turned out to be a subscription mismatch, my Azure CLI session was pointed at a different subscription than the one Terraform's provider was authenticated against. `az account show` confirmed it, `az account set` fixed it. Worth remembering for anyone with more than one subscription on their account, Terraform will happily fail with a confusing "not found" error instead of a clear "wrong subscription" one.

## OIDC subject claim risk (found after the fact)

Came across a GitHub changelog post about immutable subject claims for OIDC tokens, and it applies directly to the federated credential set up earlier today. GitHub now embeds permanent numeric owner/repo IDs into the subject claim for new repos, old format is `repo:owner/repo:ref:refs/heads/main`, new format is `repo:owner@123456/repo@456789:ref:refs/heads/main`. The reason it exists: if a repo or org name is ever deleted and recycled by someone else, the old name-only format could let a completely unrelated party mint a token that still matches your trust policy.

Source: [Immutable subject claims for GitHub Actions OIDC tokens (GitHub Changelog)](https://github.blog/changelog/2026-04-23-immutable-subject-claims-for-github-actions-oidc-tokens/)

Since this repo was created before the July 15, 2026 enforcement date, it's still on the classic format, and the federated credential set up earlier works fine right now. But found a real gotcha reading a related writeup about the same change breaking AWS deployments: AWS trust policies support wildcard patterns, so when the format changes you can just add a second pattern alongside the old one. Azure federated credentials don't have that option, the subject is matched as one exact string, no wildcards, no list of alternates. That means if this credential is ever rotated, or if I opt into the immutable format later, or if GitHub eventually migrates existing repos automatically, there's no graceful fallback, it just breaks outright with no clear error pointing at the cause.

**Practical note for next time this credential gets touched:** check the actual current subject format before assuming anything, `gh api /repos/<owner>/<repo>/actions/oidc/customization/sub` shows it directly. If it ever needs to move to the immutable format, that means deleting and recreating the federated credential with the new exact string, not just adding a second one.

Source for the AWS-breakage comparison: [GitHub changed its OIDC subject claims and broke my AWS deploys for new repos (dev.to)](https://dev.to/aws-builders/github-changed-its-oidc-subject-claims-and-broke-my-aws-deploys-for-new-repos-2cfp)

## Scanner stack decisions

Landed on: Bandit for Python SAST, Checkov for Terraform/IaC misconfiguration scanning, Gitleaks for secrets (on top of GHAS, not instead of it), Dependabot for dependency SCA, and Grype for container image vulnerability scanning.

**Dropped Trivy.** It was the original plan for both container scanning and IaC scanning, but in March 2026 its GitHub Action and Docker Hub images got compromised twice in three weeks, an attacker force-pushed 75 of 76 version tags on the action, turning trusted version references into a distribution channel for an infostealer that pulled cloud credentials, SSH keys, and Kubernetes tokens straight out of CI runners. That's not a hypothetical risk, that's exactly the kind of supply-chain attack a security-focused pipeline is supposed to be designed to avoid. Checkov picks up the IaC scanning half of what Trivy used to do, Grype picks up the container image half.

**Why Grype over other alternatives.** It's built by Anchore, scoped narrowly to just container image vulnerability scanning, no cluster scanning, no IaC scanning, nothing extra. That narrower footprint is a feature here, not a limitation, fewer moving parts means smaller attack surface, which is the direct lesson from what happened to Trivy. It also doesn't share any infrastructure or release pipeline with Trivy, so it's a genuinely independent second opinion, not just a rebrand of the same risk.

Almost lumped Checkov in as covering container scanning too, it doesn't, Checkov is purely an IaC misconfiguration scanner. It belongs in `terraform.yml`, scanning the five modules built earlier for things like whether encryption is enabled or public access is disabled where it should be. Expect it to flag the ACR's `public_network_access_enabled = true` right away, which is fine, that's already a documented, deliberate decision, not an oversight, so it's actually a good test case that the scanner and the reasoning behind it line up.

**Why Gitleaks even though GHAS has free secret scanning.** GHAS secret scanning is free for public repos and does scan history, but it only checks against roughly 230 partner patterns and push protection isn't on by default. Gitleaks lets custom rules get written for anything GHAS's partner list wouldn't catch, and running it explicitly in the pipeline is a stronger signal that the tooling was actually built and understood, not just quietly inherited from a platform default.

Semgrep, if added later, would fall in the same category as Bandit, not a separate layer, multi-language SAST versus Bandit's Python-only scope. Redundant to run both against a single small Flask app right now, would become worth it once the codebase spans more than one language, like if the FastAPI compliance service from the backlog gets built.

**Considered OSV-Scanner for SCA**, decided against it for now since Dependabot already covers the same ground and running both would be redundant without a strong enough reason yet.

## Pinning GitHub Actions to a commit SHA instead of a version tag

Wrote the `azure/login` step in `terraform.yml` referencing a full commit hash (`azure/login@8c334a195...`) instead of the usual version tag (`azure/login@v2`), and didn't actually understand why at first, it's just what got pasted in.

Simple version: a version tag like `v2` can be moved. The repo owner (or anyone who compromises their account) can point `v2` at a totally different commit tomorrow, and every workflow using `@v2` would silently start running that new code on its next run, no changes needed on my end. A commit SHA can't be moved. It's a permanent fingerprint of one exact snapshot of code, forever. Pinning to the SHA means the workflow runs that exact code no matter what happens to the tag later.

This is exactly the Trivy situation from earlier today. Attackers force-pushed 75 of 76 version tags on `aquasecurity/trivy-action`, so anyone referencing `@v0.28.0` (or almost any tag) got silently redirected to compromised code the next time their pipeline ran. Nobody had to change a line of their own workflow file, the tag just started pointing somewhere else. If those pipelines had pinned to a commit SHA instead of a tag, the attack wouldn't have touched them.

Also cleared up a mix-up: pinning the *action's* version has nothing to do with my *own* Terraform code changes. `azure/login@<sha>` locks down which version of the login action itself runs, not my repo. Every push to `terraform/**` still triggers the workflow fresh, `actions/checkout` still pulls my latest code every time. Same idea as pinning `Flask==3.1.3` in `requirements.txt`, I'm not freezing my own app, I'm freezing which version of a dependency I trust.

**Getting the SHA correctly with `git ls-remote`.** First attempt pasted the full browser URL straight off GitHub's website, `https://github.com/hashicorp/setup-terraform/releases/tag/v4.0.1`, as if it were one argument. That's wrong, `git ls-remote` isn't a browser, it only understands actual git refs, not GitHub's site navigation paths. The command only ever takes two plain parts: the repo URL by itself (`https://github.com/<owner>/<repo>`, nothing after it) and the ref name by itself (`v4.0.1`, no surrounding path). Correct form:

```bash
git ls-remote https://github.com/hashicorp/setup-terraform v4.0.1
```

Mental check going forward: if the string has `/releases/`, `/tree/`, or `/blob/` in it, that's a website path, not a git ref, strip it back down to just the tag before using it with any `git` command.

## Pipeline structure

Two separate GitHub Actions workflows, `terraform.yml` and `app-deploy.yml`, triggered independently on path-based filters (`terraform/**` for one, `app/**` and `Dockerfile` for the other), not chained automatically. Reasoning: Terraform has to succeed first since ACR, the Container App, and the identity's role assignment all need to exist before anything can be pushed or deployed, but forcing every code change to also trigger an infrastructure run (or vice versa) doesn't match how most teams actually want this to behave. Documenting in the README that a fresh environment needs `terraform.yml` run before `app-deploy.yml` will succeed.

Once on the right subscription, `plan` ran clean: 15 resources to add, 0 errors. The `data` block correctly read the manually-created resource group, and `resource_group_id` resolved properly into every module and output that referenced it, including all three policy assignments. This confirms the OIDC bootstrap pattern actually works end to end, Terraform can read a resource group it doesn't own and wire everything downstream off of it without ever threatening to create or destroy that resource group itself.

## Wiring the Root Module

This is where all five modules actually get connected. Root `main.tf` reads the resource group first (it's a `data` source after the OIDC bootstrap change, so Terraform never creates or deletes it), then calls each module in dependency order: storage first (no dependencies), identity next (needs storage's `acr_output` for the role assignment scope), compute last (needs both storage's ACR outputs and identity's identity id), with network and policy running independently since nothing downstream currently consumes their outputs.

**The VNet decision.** Network module exists and works, but Container Apps isn't actually deployed inside it, no `infrastructure_subnet_id` wiring into the Container App Environment. That means the app currently has public ingress by default. This was a deliberate call, not an oversight, flagged it directly in a `main.tf` comment and in every network-related output's description so it reads as a documented tradeoff instead of a hole nobody noticed. Real reasoning: finishing the full pipeline end-to-end mattered more right now than gold-plating the network layer. If this were going to production, or if I wanted to defend it in an interview, the honest answer is "this is a known gap, here's what I'd do to close it" rather than pretending it's not there.

**Root outputs mirror the same honesty pattern.** Every output that isn't actually consumed by another module (`vnet_id`, `subnet_id`, `nsg_id`, all three policy ids) says so directly in its description, "not currently consumed by compute" or "not consumed by other modules, exposed for visibility via terraform output", instead of looking like unfinished wiring.

Built out `environments/dev/terraform.tfvars` with real values across all five modules, this is the first point where every validation block written today (location, ACR name regex, ACR sku/environment pairing, AcrPull-only role, PerGB2018-only workspace sku, single revision mode, cpu/memory ratio) actually gets tested against real input instead of just existing in isolation.

## First terraform plan

Ran `terraform plan -var-file=environments/dev/terraform.tfvars` for the first time. First attempt just prompted for `acr_name` interactively instead of reading the tfvars file, turned out I'd forgotten to actually save the file, so Terraform had nothing to read and fell back to asking one variable at a time.

Once the file had real content in it, plan surfaced two real bugs:

**Subnet output bug.** `network/outputs.tf` was trying to call `.id` directly on `azurerm_virtual_network.azappsec-vnet.subnet`, but that's a set, not a single object, so `.id` doesn't work on it. This is the exact thing I'd flagged earlier when writing the network module and decided to test live instead of switching to a separate `azurerm_subnet` resource since I couldn't find registry docs confirming the inline syntax. Terraform confirmed it directly at plan time: wrapped it in `tolist(...)[0].id`, same fix already used correctly for the NSG association, just hadn't been applied to this output yet.

**Wrong resource type for policy assignments.** `azurerm_policy_assignment` doesn't exist as a resource type in the `azurerm` provider, that was the generic name from the example I'd based the policy module on originally. The provider actually splits policy assignment by scope: `azurerm_resource_group_policy_assignment`, `azurerm_subscription_policy_assignment`, `azurerm_management_group_policy_assignment`. Since I'd already deliberately scoped this project's policies to the resource group, swapped in `azurerm_resource_group_policy_assignment` and renamed the `scope` argument to `resource_group_id` to match what that specific resource type actually expects.

After both fixes, `terraform plan` ran clean: 16 resources to add, 0 to change, 0 to destroy, no errors. Every validation block, every least-privilege scoping decision, every SRP split written across all five modules got checked against real Azure API schemas and passed.

**Worth noting from the plan output:** `public_network_access_enabled = true` on the ACR confirms the VNet decision documented earlier, this is expected, not a surprise. Container App shows `min_replicas = 0`, meaning it can scale to zero when idle, that's the Container Apps default and works fine for a project like this.

Next: `terraform apply` to confirm everything actually deploys as planned, then `terraform destroy` right after to tear it down and avoid leaving billable resources running.

## Finishing v1

By this point the modules worked and `plan` was clean, but nothing actually deployed. `app-deploy.yml` was an empty file, there was no detection rule, and the to-do list felt bigger than the project. I had Claude draft the remaining pieces (both workflows, the monitoring module, the app and Dockerfile hardening, the README) as one patch. I applied it, rebuilt the Azure side from nothing, and ran it end to end. Everything below is me going back through why each piece is built the way it is, because I need to be able to explain all of it without notes.

### Bugs in my branch that would have broken the first run

Worth writing down, since every one of these would have failed in a different confusing way.

- **Backend auth used `use_msi = true`.** That only works on something that has a managed identity, like an Azure VM. A GitHub runner doesn't have one, so `terraform init` would have failed. Switched to `use_oidc = true` plus `use_azuread_auth = true`, which logs into the state storage with the same OIDC token as everything else.
- **`plan` had no `-var-file`.** Same mistake as my first local plan, it would have sat there waiting for input that never comes. `TF_INPUT=false` now makes it fail fast instead of hanging.
- **`terraform fmt -check` would have failed on 10 files.** Misaligned `=` signs. It's the first step of the pipeline, so nothing after it would have run.
- **Contributor can't create role assignments or policies.** Contributor explicitly excludes `Microsoft.Authorization/*/Write`. My Terraform creates both, so the first apply would have died halfway through.
- **Jobs that use `environment: dev` send a different OIDC subject.** The subject becomes `repo:<repo>:environment:dev`, not `ref:refs/heads/main`. Azure matches the subject as one exact string, so the gated jobs needed their own federated credential.
- **The Container App had no `ingress` block.** No ingress means no URL, so nothing could reach `/health`.
- **`dockerfile` was lowercase** and the workflow path filter said `Dockerfile`. Linux cares about case, so changing the Dockerfile would never have triggered a build.
- **The action group needs location `global`**, and my own location policy only allowed `eastus`. My guardrail would have blocked my own alerting. Added `global` to the allowed list.

### terraform.yml

Three jobs: `scan`, `plan`, `apply`.

`scan` runs `fmt -check`, `validate`, tflint and Checkov. None of that needs Azure, so this job doesn't get `id-token: write`. Only the jobs that actually log into Azure can ask GitHub for an OIDC token. Same least-privilege idea as scoping AcrPull to one registry, just applied to the pipeline.

`plan` runs on every PR and every push to main, and writes the plan into the job summary so I can read exactly what's about to change before approving.

`apply` only runs on main, and it uses `environment: dev`. That environment has me as a required reviewer, so the job pauses until I click approve. It re-runs `plan` instead of downloading the plan file from the previous job. Plan files can contain sensitive values, and on a public repo anyone signed into GitHub can download workflow artifacts.

**Concurrency group.** Two runs can't touch the same state at the same time. The blob lease on the state file is the second layer, this stops the second run from even starting.

**The Discord webhook comes in as `TF_VAR_discord_webhook_url`** from a GitHub secret, so it never lands in a tfvars file in the repo.

### app-deploy.yml

Also three jobs: `test-and-scan`, `build`, `deploy`.

`test-and-scan` runs pytest, Bandit and Gitleaks. Gitleaks needs `fetch-depth: 0` or it only sees the latest commit, and a secret committed three commits ago and then deleted is still in the history. Turned off its artifact upload too. On a public repo the findings report would publish the exact secret it just caught.

`build` builds the image, then Grype scans it **before** it can reach ACR. A vulnerable image never lands in the registry. On main it pushes, tagged with the full commit SHA instead of `latest`. Every running container traces back to one commit.

`deploy` is gated by the same `dev` environment. It points the app at the new image, then curls `/health` up to six times, 20 seconds apart. The retries exist because the app scales to zero, so the first request has to wake it up.

### Who owns the image, Terraform or the pipeline?

This one took me a minute. On the very first `terraform apply`, ACR is empty, so there's no image of mine to run yet. Terraform creates the Container App with a public placeholder image (`mcr.microsoft.com/k8se/quickstart`, port 80). After that, `app-deploy.yml` swaps in the real image and switches ingress to port 5000.

The problem: the next `terraform apply` would see the image doesn't match the code and roll it back to the placeholder. Fixed with `lifecycle { ignore_changes }` on the image and the target port. Terraform owns the infrastructure, the pipeline owns which image runs. Each tool has one job.

### App changes so there's something to detect

The detection needs events to look for, so the app now logs `not_found` (404) and `method_not_allowed` (405) as JSON, with the client IP, path and method. Six pytest tests cover the endpoints and the log format.

**Client IP comes from the last value in `X-Forwarded-For`, not the first.** The client can put anything it wants in that header. Container Apps ingress appends the real IP at the end, so the last value is the only one I can trust. Taking the first value would let an attacker pick which IP shows up in Sentinel.

**User-agent gets cut to 200 characters** before it's logged, so nobody can stuff huge strings into my logs.

**`# nosec B104` on `host="0.0.0.0"`.** Bandit flags binding to every interface. Inside a container that's exactly what has to happen (same reason as Phase 1), so the comment tells Bandit this one is deliberate.

The Dockerfile now runs as a non-root `appuser`. If someone breaks out of the app, they land as a normal user instead of root inside the container.

### Sentinel detection (monitoring module)

Sentinel isn't its own resource you deploy, it gets switched on over the Log Analytics workspace the compute module already creates.

The rule (`web-recon-probing`) runs every 5 minutes. It counts 404 and 405 responses per client IP and fires when one IP hits 10 or more. That's what directory brute forcing, vulnerability scanners and HTTP method tampering look like. Mapped to MITRE Reconnaissance and Discovery, with the IP mapped as an entity so it shows up properly in the incident.

**The empty `datatable` in the query.** `ContainerAppConsoleLogs_CL` doesn't exist until the app writes its first log line, and Sentinel refuses to save a rule that queries a missing table. `union isfuzzy=true` with an empty datatable lets the rule save on day one.

**Discord is optional.** If the webhook secret is empty, Terraform skips the Logic App, the action group and the alert entirely. The `count` uses `nonsensitive(var.discord_webhook_url != "")`, which only reveals true or false, never the URL.

### Pipeline permissions: four roles instead of one

| Role | Scope | Why |
|---|---|---|
| Contributor | resource group | create and manage the resources |
| Role Based Access Control Administrator, with a condition | resource group | create role assignments, but only AcrPull and only for service principals |
| Resource Policy Contributor | subscription | policy definitions always live at subscription level |
| Storage Blob Data Contributor | the `tfstate` container only | read and write the state file with Entra ID, no storage keys |

The condition on the RBAC admin role is what makes it safe. Without it, that role could grant itself Owner. With it, the only thing it can hand out is AcrPull. Followed Microsoft's "Constrain ACR management" example for the condition.

## Rebuilding from scratch

I'd deleted everything after the first apply to stop paying for it, including the resource group. So the whole bootstrap ran again from zero: register the resource providers, resource group, state storage with shared key access turned off, pipeline identity, three federated credentials, four roles, then the `dev` environment and secrets in GitHub.

**Checked the OIDC subject format first this time.** My repo was created May 2, 2026, before GitHub's July 15 cutoff, so it's still on the classic `repo:owner/repo:...` format. If I ever rename or transfer the repo it switches to the immutable format, and all three credentials have to be recreated.

**Registering providers by hand.** The pipeline identity only has rights inside one resource group, and registering a resource provider is a subscription-level action. So the provider config has `resource_provider_registrations = "none"`, and I register them once during bootstrap instead.

## First real pipeline run

Opened the PR. `scan` and `plan` both passed on the first try, which meant OIDC, all four roles and the state backend worked. That was the part I was most worried about.

**Grype failed the build.** That was the scanner doing its job. Every High and Critical finding was in Alpine's OS packages, not my code: `krb5-libs`, `libssl3`/`libcrypto3`, and a Critical in `zlib`. All of them had a fixed version available, the base image was just a few weeks behind. Fixed with:

```dockerfile
RUN apk upgrade --no-cache
```

Also upgraded pip in the same build and bumped Werkzeug from 3.1.8 to 3.1.9 for a Medium finding. The `python` rows were all Medium or Low with fixes only in Python 3.13 and up, and the pipeline only fails on High or above, so those don't block.

**Tradeoff I want to remember:** `apk upgrade` makes builds less reproducible, because the result depends on the day you build. The stricter version is pinning the base image by digest and letting Dependabot bump it.

After that everything was green. Merged, read the plan in the job summary, approved the apply. App deploy failed at the push step on its first main run because ACR didn't exist yet, which is exactly what the README warns about. Re-ran it once the apply finished, approved the deploy, smoke test passed.

## Testing the detection

Ran the README's curl loop: ten requests to paths that don't exist (`.env`, `wp-login.php`, `.git/config`...) and one POST to `/health`. Got ten 404s and a 405. Logs showed up in `ContainerAppConsoleLogs_CL` within a few minutes.

Two things I learned while waiting on the incident:

**Sentinel already runs scheduled rules five minutes late on purpose,** to give logs time to arrive. My query also has its own `where TimeGenerated > ago(5m)` inside it, on top of the rule's 5-minute lookback. That inner filter is redundant at best. If the incident never shows up, it's the first thing to remove.

**The way my Container Apps environment sends logs is deprecated.** Pointing the environment at a workspace with `log_analytics_workspace_id` uses the legacy HTTP Data Collector API, and its support ended September 14, 2026. It still ingests, but only gets critical security fixes. The current way is the Azure Monitor logging destination plus a diagnostic setting. The table then becomes `ContainerAppConsoleLogs` (no `_CL`) and the column becomes `Log` instead of `Log_s`, so the detection query has to change with it. Adding this to known gaps.

**Result: the incident showed up.** The rule fired on the 11 probes and Sentinel opened an incident for `web-recon-probing`. So the redundant `ago(5m)` didn't cause a miss this time. It's still a risk worth cleaning up (a burst that lands right on a window edge could slip through), but I'm not going to claim it's a bug I hit.

## One workspace or two

Opened Sentinel in the portal and saw two of them. The other one is for my homelab, and my first thought was to combine everything into one workspace. Decided to keep them separate for now. If this project's Terraform managed the shared workspace, `terraform destroy` would wipe my homelab's logs with it. And someone cloning the repo should be able to deploy it from scratch without needing a workspace that only exists in my subscription.

The clean version for later is an optional `existing_workspace_id` variable. If it's set, Terraform looks the workspace up with a `data` source (same trick as the resource group). If it's empty, it creates its own like it does now.

## Errors hit

1. Committed the Terraform scaffold on main locally and tried to push but GitHub rejected it because of branch protection.

2. Created a GitHub Issue to track the Terraform work. Issues are how teams track what needs to be done. Attaching a branch to an issue links the work to the task. **MAKE SURE WHEN CHECKING OUT A BRANCH YOU INCLUDE THE `-b` FLAG!!**

3. Created a terraform branch but couldn't switch to it because I had uncommitted local changes that would've been overwritten. Git protects me from losing work.

4. Ran `git reset HEAD~1` which undid my last commit but kept the file changes locally. This put me back to a clean state to switch branches.

5. Tried `git stash` to temporarily save my changes and it threw an error because after the reset there was nothing staged to stash.

6. Switched to the terraform branch, made my changes there, and committed.

7. Git rejected the push because the local branch wasn't linked to a remote branch yet, that's the `--set-upstream` error. Running `git push --set-upstream origin terraform` tells Git "this local branch lives at origin/terraform."

8. GitHub blocked the push because my commits had my real email in them. Fixed with `git config`.

9. Terraform uses `/` as a separator.

10. `git am` failed with "previous rebase directory .git/rebase-apply still exists". An earlier attempt had stopped halfway and left its state behind (my prompt showed `AM 1/1`). `git am --abort` cleared it and put the branch back the way it was.

11. On Windows the patch failed with "Dockerfile: already exists in working directory". Windows file names ignore case, so renaming `dockerfile` to `Dockerfile` looks like creating a file that already exists. Applied the patch with `--exclude=Dockerfile --exclude=dockerfile`, then did the rename in two steps through a temporary name: `git mv dockerfile Dockerfile.tmp`, then `git mv Dockerfile.tmp Dockerfile`.

12. Same patch also failed on `terraform.tfvars`, because I had an untracked local copy sitting there. Moved it aside, let the patch add the committed version, then compared the two.

13. `az login` crashed with `[WinError 5] Access is denied` on `.azure\cliextensions\account`. A broken CLI extension folder, nothing to do with my code. Deleted the folder and az worked again.

14. Deleting the old federated credential failed with `ResourceGroupNotFound`. I'd deleted the whole resource group earlier and forgot. Nothing left to delete, so I moved straight to rebuilding.

15. My terminal (MSYS2 / Git Bash on Windows) rewrites anything starting with `/` into a Windows path, so `--scope "/subscriptions/..."` would have turned into `C:/Program Files/...`. Ran `export MSYS_NO_PATHCONV=1` before the bootstrap commands and checked the printed scope started with `/subscriptions/`.

## References
- [How to Move Changes to Another Branch in Git](https://www.howtogeek.com/devops/how-to-move-changes-to-another-branch-in-git/)
- [Moving changed files to another branch for check-in](https://stackoverflow.com/questions/7217894/moving-changed-files-to-another-branch-for-check-in)
- [git stash throws error No local changes to save](https://stackoverflow.com/questions/38200616/git-stash-throws-error-no-local-changes-to-save)
- [Resolving GitHub push declined due to email privacy restrictions](https://medium.com/@python-javascript-php-html-css/resolving-githubs-push-declined-due-to-email-privacy-restrictions-issue-c346a9cf1da0)
- [Azure Container Registry Microsoft Entra permissions and role assignments overview](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-rbac-built-in-roles-overview?tabs=registries-configured-with-rbac-registry-abac-repository-permissions)
- [Workload profiles in Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/workload-profiles-overview#consumption-profile-details)
- [Terraform: How to Concatenate Variables (With Examples)](https://nulldog.com/terraform-how-to-concatenate-variables-with-examples)
- [Constrain ACR management (Microsoft Learn, delegating role assignments with conditions)](https://learn.microsoft.com/azure/role-based-access-control/delegate-role-assignments-examples#example-constrain-acr-management)
- [Azure Container Apps security baseline (why Defender for Containers doesn't cover it)](https://learn.microsoft.com/security/benchmark/azure/baselines/azure-container-apps-security-baseline#posture-and-vulnerability-management)
- [Monitor logs in Azure Container Apps with Log Analytics](https://learn.microsoft.com/azure/container-apps/log-monitoring)
- [Change Azure Container Apps logging from Log Analytics to Azure Monitor](https://learn.microsoft.com/azure/container-apps/migrate-logs-azure-monitor)
- [Handle ingestion delay in scheduled analytics rules (Sentinel)](https://learn.microsoft.com/azure/sentinel/ingestion-delay)
- [Scheduled analytics rules in Microsoft Sentinel](https://learn.microsoft.com/azure/sentinel/scheduled-rules-overview)