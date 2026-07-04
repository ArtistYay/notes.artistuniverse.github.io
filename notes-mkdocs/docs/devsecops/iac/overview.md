---
tags:
  - Infrastructure as Code
---

## What is Infrastructure as Code?

Infrastructure as Code (IaC) is the practice of provisioning and managing infrastructure through configuration files instead of a GUI or manual CLI commands. You describe your servers, networks, and databases in code, then let a tool build them for you, the same way you'd manage application code.

**Why it matters:**

- **Consistent** — the same code produces the same environment every time.
- **Trackable** — infrastructure changes live in version control, so you get a real history of who changed what and when.
- **Repeatable** — spin up one environment or a thousand with the same definition.
- **Shareable/reusable** — teams reuse patterns instead of re-inventing them per project.

Before cloud APIs, infrastructure was provisioned by filing a ticket and having someone log into a console to click through the setup. That worked fine when infrastructure lived for months or years and didn't change much. Cloud changed the math: infrastructure is API-driven, spun up and torn down constantly, and scaled out across many small instances instead of a few big ones. Manually managing that at scale doesn't hold up, so the process itself gets codified.

## Declarative vs. Imperative

- **Imperative** — you tell the software the exact steps to take. Get the shell, add the beans, add the cheese, add the lettuce, in that order.
- **Declarative** — you tell the software what you want the end result to be, and it figures out the how. "I want a taco with beans, cheese, and lettuce."

Most IaC tools, Terraform included, are declarative. You describe the desired state, and the tool calculates the steps needed to get there.

## Idempotence

Idempotence means running the same operation twice produces the same result as running it once. If someone already has a taco and asks for a taco again, an idempotent process recognizes they already have one and does nothing. IaC tools track the current state of your infrastructure and only make changes when your configuration and that state don't match.

## Mutable vs. Immutable Infrastructure

This is one of the more important mental shifts when moving from manual infrastructure management to IaC.

- **Mutable** — you update existing infrastructure in place (patch the server, upgrade the package, restart the service).
- **Immutable** — you never update in place. You build a new version from scratch, validate it, cut traffic over, then destroy the old version.

Mutable changes carry partial-failure risk: if an in-place upgrade fails halfway, you're left with an undefined, untested state that's neither the old version nor the new one. At scale, across hundreds or thousands of machines, that turns into a fleet where every machine might be in a slightly different, poorly understood state.

Immutable infrastructure avoids this by only ever having two well-defined states: the old version, still running and validated, or the new version, freshly built and validated. There's no in-between. The trade-off is that anything stateful (like a database written to local disk) needs to be externalized first, since you can't just throw away a machine and its data.

IaC tooling naturally leans toward the immutable model: because your infrastructure is defined as versioned, declarative code, "build new from definition" is a more natural fit than "patch what exists." See the Terraform-specific breakdown in the notes below for how this plays out with resource replacement.

## The Infrastructure Lifecycle

Infrastructure is rarely a one-and-done deployment. It's useful to think about it in stages:

- **Day 0** — foundational setup: cloud accounts, landing zones, core networking, guardrails.
- **Day 1** — initial deployment of your actual application infrastructure.
- **Day 2+** — ongoing care and feeding: patching, right-sizing, scaling, compliance, cost management, architecture changes. This is where infrastructure spends most of its life.

Because IaC captures all of this as code, day 2+ work (patch a base image, resize a database, add a new environment) becomes a matter of changing the definition and re-running the tool, rather than a one-off manual task.

## Policy as Code

As infrastructure changes get automated, you also want automated guardrails. Policy as code lets you inspect a proposed change (a plan) before it's applied and block it if it violates a rule, such as opening a firewall to the entire internet, disabling encryption, or removing the last redundant instance behind a load balancer. This keeps cost, security, and compliance checks in the same automated pipeline as the infrastructure changes themselves, instead of relying on someone remembering to check manually.