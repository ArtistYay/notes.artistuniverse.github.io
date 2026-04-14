---
tags:
  - Infrastructure as Code
  - DevOps
---

# Terraform: Writing DRY Code with Modules and `for_each`

## The Problem: Repetition

When you copy/paste a block of infrastructure code and only change 1–2 words (e.g., `ebs` to `rds`), that's your signal to refactor.

**Risks of repetition:**
- Forgetting to update one copy when things change
- Adding a third resource means another copy-paste
- Bugs get fixed in one place but not the other

---

## The Solution: Two Concepts Working Together

### 1. Modules: "the reusable template."

A **module** is just a folder containing `.tf` files that you treat like a function. Instead of hardcoding specific values, you define **variables** as placeholders.

```hcl
# modules/kms_key/main.tf

variable "name" {}        # placeholder for "ebs-encryption-key", etc.
variable "description" {} # placeholder for "EBS encryption key", etc.
variable "tags" {}

resource "aws_kms_key" "main" {
  description = var.description  # uses the placeholder
  tags        = var.tags
}

resource "aws_kms_alias" "main" {
  name          = "alias/${var.name}"  # uses the placeholder
  target_key_id = aws_kms_key.main.key_id
}

output "key_id" {
  value = aws_kms_key.main.key_id
}

output "alias_name" {
  value = aws_kms_alias.main.name
}
```

> **Mental model:** A module is like a cookie cutter, It defines the *shape*, and the caller provides the *ingredients*.

---

### 2. `for_each`: "stamp it out multiple times."

Instead of calling the module twice manually, use `for_each` to loop over a map and call it once per entry.

```hcl
module "kms_key" {
  for_each = {
    ebs = "EBS"   # key = used in resource names, value = used in descriptions
    rds = "RDS"
  }

  name        = "${var.name_prefix}-${each.key}-encryption-key"
  description = "${each.value} encryption key"
  tags = merge(var.extra_tags, {
    Name               = "${var.name_prefix}-${each.key}-encryption-key"
    component          = "kms"
    dataclassification = "low"
  })
}
```

- `each.key` → `"ebs"` or `"rds"` (left side of the map)
- `each.value` → `"EBS"` or `"RDS"` (right side of the map)

**Terraform creates independent resource sets per map entry:**
```
module.kms_key["ebs"].aws_kms_key.main
module.kms_key["ebs"].aws_kms_alias.main
module.kms_key["rds"].aws_kms_key.main
module.kms_key["rds"].aws_kms_alias.main
```

> Adding `s3 = "S3"` to the map later creates a third set without touching the existing two.

---

### Accessing Outputs from the Calling Module

```hcl
module.kms_key["ebs"].key_id
module.kms_key["ebs"].alias_name
module.kms_key["rds"].key_id
module.kms_key["rds"].alias_name
```

---

## The Mental Checklist: When Should I Use This Pattern?

| Question | If YES → consider module + `for_each` |
|---|---|
| Am I copy-pasting a block and only changing 1–2 words? | ✅ |
| Will I likely need a 3rd or 4th version of this later? | ✅ |
| Do these resources always travel together (e.g., key + alias)? | ✅ module groups them |
| Are the differences between copies just *data*, not *structure*? | ✅ |
| Is the structure itself fundamentally different between copies? | ❌ Keep them separate |

---

## The Mental Model to Remember

| Concept | Role | Answer |
|---|---|---|
| **Module** | Reusable template | *What* gets created |
| **`for_each`** | Loop | *How many* times |
| **The map** | Data that makes each instance unique | *With what values* |

> Any time you can reduce "copy/paste with minor edits" into "one template + a list of differences", that's your opportunity to apply this pattern.