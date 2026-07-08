---
tags:
  - Infrastructure as Code
  - DevOps
---

## Variables, Outputs & Locals

### Input Variables

A `variable` block supplies a parameter to your configuration. All three common arguments are technically optional, but each earns its place:

```hcl
variable "aws_region" {
  type        = string
  description = "AWS region to use for resources"
  default     = "us-east-1"
}
```

- **`type`** — the data type expected. Gives you error checking for free: pass a list where a number is expected, and Terraform stops you before it ever touches a provider.
- **`description`** — explains the variable's purpose. Cheap to write, and it's the first thing a teammate (or future you) reads when a variable throws an error.
- **`default`** — a fallback value. Without one, Terraform requires a value to be supplied some other way at plan time, or it will prompt you interactively for one.

Reference a variable's value with `var.<name>`. For a collection, the same indexing rules apply as the underlying type: `var.aws_regions[0]` for the first element of a list, `var.instance_sizes.small` or `var.instance_sizes["small"]` for a map key. See the [main Terraform overview](overview.md) for the full rundown of base and complex variable types (string/number/bool, list/set/map/object/tuple).

### The Six Ways to Set a Variable's Value

Terraform accepts values from several sources, and if the same variable is set in more than one place, precedence decides which value wins. From **lowest to highest precedence**:

1. **`default`** in the variable block itself.
2. **Environment variables**, named `TF_VAR_<variable_name>`.
3. **`terraform.tfvars`**, automatically loaded from the working directory if present.
4. **`terraform.tfvars.json`**, if present (wins over `terraform.tfvars` for any variable defined in both).
5. **`*.auto.tfvars`** / **`*.auto.tfvars.json`** files, auto-loaded in lexical (alphabetical) filename order. Later files win for the same variable.
6. **`-var` and `-var-file` command-line flags**, processed in the order given, with later flags winning. These have the highest precedence of all.

If no value is supplied anywhere and there's no default, Terraform prompts you at the command line. All variables need a value at plan time, one way or another.

A common point of confusion: `TF_VAR_*` environment variables sit *below* tfvars files in precedence, not above them. A `terraform.tfvars` value will silently win over an environment variable set for the same variable, which surprises people who assume "explicitly exported" beats "in a file."

### Output Values

An `output` block is how you extract information after a run.

```hcl
output "web_server_public_dns" {
  value       = aws_instance.web_server.public_dns
  description = "Public DNS host name of the EC2 instance"
}
```

- `value` is the only required argument, and it can be any valid expression.
- `description` is optional but helpful, especially for outputs that return something complex, like a whole object.
- Outputs print to the terminal after `apply` and are stored in state for later retrieval (see the [State Management](state_management.md) notes on the `terraform output` command).
- Outputs are also how a child module passes information back up to whatever's calling it.

### Local Values

A `locals` block defines computed values you can reference throughout the rest of the configuration. Think of it as an internal scratchpad, useful anytime you need to use the same derived value more than once, or want to transform data (combine strings, merge maps) in one place instead of repeating the logic everywhere it's used.

```hcl
locals {
  instance_prefix = "${var.project}-${var.environment}"

  common_tags = {
    company       = var.company_name
    project       = var.project
    environment   = var.environment
    billing_code  = var.billing_code
  }
}
```

- No block labels needed, just the `locals` keyword.
- Each key inside is a local value's name; the value can be a literal, a reference to another object, or a function call.
- Reference a local with `local.<name>` (for example, `local.instance_prefix`), the same dot-indexing rules apply for collections (`local.common_tags.company`).
- You can have multiple `locals` blocks in a configuration, but every local name still has to be unique overall.

The `${...}` syntax above is **string interpolation**: it tells Terraform to evaluate whatever's between the braces and render the result as part of the surrounding string. It's the same mechanism used any time you build a dynamic string from variables or other references.

### Variables vs. Locals, at a Glance

| | Variables | Locals |
|---|---|---|
| Purpose | External input, supplied by the caller | Internal computed value |
| Set from outside the configuration? | Yes (tfvars, CLI, env vars) | No, only ever computed inside |
| Typed? | Yes, via `type` | No explicit type argument |
| Good for | Anything that should differ per environment or deployment | Derived values you don't want to repeat (naming prefixes, merged tag maps) |

### Tips from the Community

- **A `terraform.tfvars` value overrides a `TF_VAR_*` environment variable for the same variable, not the other way around.** This trips people up constantly, since exporting an environment variable feels like the more "explicit" or recent action. Precedence doesn't care about that intuition, files beat environment variables here.
  Source: [How to Understand Variable Precedence in Terraform – OneUptime](https://oneuptime.com/blog/post/2026-02-23-how-to-understand-variable-precedence-in-terraform/view)

- **Leftover `.auto.tfvars` files from testing silently override your real values.** Because any file matching `*.auto.tfvars` loads automatically with no flag needed, a forgotten scratch file from an earlier experiment can quietly change what a later `plan` or `apply` actually does. Worth a periodic check of your working directory for stray `.auto.tfvars` files you didn't mean to keep.
  Source: [How to Understand Variable Precedence in Terraform – OneUptime](https://oneuptime.com/blog/post/2026-02-23-how-to-understand-variable-precedence-in-terraform/view)

- **Name `.auto.tfvars` files with a numeric or alphabetic prefix if load order matters.** Since these files load in lexical order and the last one loaded wins for any shared variable, something like `00-defaults.auto.tfvars` and `90-overrides.auto.tfvars` makes the precedence visible from the file name itself, instead of leaving it to alphabetical accident.
  Source: [How to Pass Variables via .auto.tfvars Files in Terraform – OneUptime](https://oneuptime.com/blog/post/2026-02-23-how-to-pass-variables-via-auto-tfvars-files-in-terraform/view)

- **Don't hide a required decision behind a convenient default.** A default like `database_password = "changeme"` looks harmless in a variable block, but it means someone can deploy without ever being forced to think about the password. For anything sensitive or safety-critical, skip the default and mark the variable `sensitive` instead, forcing an explicit value every time.
  Source: [Terraform Variable Precedence: A Complete Guide – Medium](https://medium.com/@fnizi.ayoub/terraform-variable-precedence-a-complete-guide-ffa4ce65c4f4)

- **Use `terraform console` to check which value actually won, rather than guessing.** When a variable is set in several places and the result isn't what you expected, dropping into `terraform console` and evaluating `var.<name>` shows you the value Terraform is actually using, no need to reason through the whole precedence chain by hand. See [Functions & Expressions](functions_and_expressions.md) for more on the console.
  Source: [Terraform Variable Precedence: A Complete Guide – Medium](https://medium.com/@fnizi.ayoub/terraform-variable-precedence-a-complete-guide-ffa4ce65c4f4)