---
tags:
  - Infrastructure as Code
  - DevOps
---

# Mutable vs. Immutable Infrastructure (in Terraform)

## The Core Idea

- **Mutable** — you take an existing server and change it in place. Patch it, install a new package, restart a service.
- **Immutable** — you never change a running resource. You build a brand new one from an updated definition, validate it, cut traffic over, and destroy the old one.

**Mental model:** mutable is renovating your house while you're still living in it. Immutable is building a new house next door and moving in once it's finished, then tearing down the old one.

## Why Mutable Gets Risky at Scale

Say you're running a web server on Apache and want to move to a newer version, or switch to a different web server entirely. In a mutable world, a configuration management tool (Chef, Puppet, Ansible) runs against the live server to bring it up to date.

The problem shows up when the upgrade doesn't finish cleanly:

- A network blip, a broken repo mirror, a half-applied patch, any of these can leave the box in a state that's neither the old version nor the new one.
- That in-between state was never tested. Nobody validated what "half-upgraded" looks like, because nobody planned to be there.
- At the scale of one machine this is an annoyance. At the scale of a thousand machines, each failing slightly differently, it turns into a fleet spread across a continuous, poorly understood range of versions instead of two clean, known ones.

## How Immutable Avoids That

With immutable infrastructure, you only ever have two valid states: the old version (still running, already validated) or the new version (freshly built, validated before it takes traffic). There's no middle ground, because you never modify the running resource, you replace it.

- If the new version fails to build or fails validation, you throw it away and keep serving from the old one.
- Rollback is simple: point traffic back at the version that's still there, unchanged.
- The trade-off is state. If an app writes data to local disk, you can't just delete the machine. Stateful components generally need to be externalized (a managed database, network-attached storage) so tearing down compute doesn't lose data. This is also why databases themselves are often left mutable, or handled as a hybrid: immutable compute in front of persistent, externalized storage.

## How This Looks in Terraform

You don't SSH into a box and upgrade Apache in place. You change the source the resource is built from, usually a machine image (AMI, VM image, container image), and let Terraform handle the replacement.

```hcl
resource "aws_instance" "web" {
  ami           = var.ami_id       # points at a pre-built image
  instance_type = "t3.micro"

  lifecycle {
    create_before_destroy = true
  }
}
```

Because `ami` is an attribute that forces replacement on `aws_instance`, changing `var.ami_id` tells Terraform to build a new instance from the new image and destroy the old one, rather than patch the running instance. The new Apache version doesn't get installed by Terraform directly, it gets baked into the image ahead of time with a tool like Packer, and Terraform's job is just to deploy instances of that image.

A few practical notes:

- **`create_before_destroy`** is the setting that makes this safe. Without it, Terraform destroys the old resource first, which usually means downtime. With it, the new resource is created and validated before the old one is torn down.
- Not every attribute forces replacement. Whether a change updates a resource in place or replaces it entirely depends on the resource type and provider, check the provider docs.
- If your instance sits behind a load balancer or in an Auto Scaling Group, the ASG's rolling update behavior handles shifting traffic to new instances before removing old ones.
- Config management tools (Ansible, Chef, Puppet) aren't wrong, they're just the mutable approach, with the partial-failure and drift risks described above. Some teams use them deliberately, especially for things that change rarely, like the base image build itself.

## Mental Checklist

| Question | Leans toward |
|---|---|
| Does a failed mid-update leave you in an untested, ambiguous state? | Immutable |
| Do you need zero-downtime cutover, with an easy rollback if validation fails? | Immutable |
| Is the resource stateful and hard to externalize? | Mutable (or hybrid) |
| Does this change happen so rarely that drift risk is low? | Mutable is often fine |

## Tips from the Community

- **Immutability pairs naturally with Terraform's declarative model.** Your `.tf` files describe the exact desired state, not the steps to reach it. If you enforce immutability, that description stays the one source of truth: any manual edit or hotfix gets overwritten on the next `apply` instead of quietly drifting the fleet apart.
  Source: [Immutability in Terraform: Preventing Drift and Ensuring Infrastructure Reliability – Hoop.dev](https://hoop.dev/blog/immutability-in-terraform-preventing-drift-and-ensuring-infrastructure-reliability)

- **`name_prefix` instead of `name` matters for `create_before_destroy`.** If a security group (or similar named resource) uses a fixed `name`, Terraform can't create the replacement while the original still exists, the name collision fails the create step. Using `name_prefix` lets AWS generate a unique suffix so both copies can exist briefly during the cutover.
  Source: [How to Use Lifecycle Rules with create_before_destroy – OneUptime](https://oneuptime.com/blog/post/2026-02-23-how-to-use-lifecycle-rules-with-create-before-destroy/view)

- **A layered image pipeline keeps rebuilds cheap.** Rather than baking one monolithic AMI, build a base image (OS-level config), a middleware image (runtime dependencies), and an application image (your code) as separate layers. When only the app changes, you only rebuild the top layer instead of the whole stack.
  Source: [How to Create AMIs with Packer and Deploy with Terraform – OneUptime](https://oneuptime.com/blog/post/2026-02-23-how-to-create-amis-with-packer-and-deploy-with-terraform/view)

- **`replace_triggered_by` closes a gap `create_before_destroy` doesn't cover.** Sometimes a dependency changing should force a resource to be replaced even though the resource's own configuration hasn't changed, for example, forcing an EC2 instance to rebuild whenever the security group it references changes. `replace_triggered_by` links that dependency explicitly, which is useful for enforcing immutability end-to-end rather than just at the resource you edited directly.
  Source: [Mastering Terraform's Lifecycle Meta-arguments – DEV Community](https://dev.to/ekefan/level-up-your-infrastructure-mastering-terraforms-lifecycle-meta-arguments-4d8g)

- **Never SSH into a production box to debug.** If you need to see what's going wrong, deploy a new instance with debug tooling attached, or lean on centralized logging, rather than reaching into a running instance. The moment you SSH in and fix something by hand, you've quietly gone mutable and the image no longer matches what's actually running.
  Source: [How to Configure Immutable Infrastructure – OneUptime](https://oneuptime.com/blog/post/2026-01-24-configure-immutable-infrastructure/view)