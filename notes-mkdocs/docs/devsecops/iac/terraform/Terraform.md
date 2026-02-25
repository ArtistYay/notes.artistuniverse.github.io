---
tags:
  - AWS
  - Azure
Keyword: IaC
---
- The terraform command accepts a variety of subcommands.

- terraform version finds the version.

- terraform -chdir=<path_to/tf> <subcommand>.

- terraform init initializes the working directory that contains your Terraform code. It downloads modules and plugins.

- terraform plan creates an execution plan.

- terraform apply applies the changes.

- terraform destroy get’s rid of the infrastructure.

- terraform plan -out <plan_name> outputs the plan to a file.

- terraform plan -destroy output a destroy plan.

- terraform apply <plan_name> apply a specific plan.

- terraform apply -target=<resource_name> only apply changes to a targeted resource.

- terraform apply -var my_variable=<variable>pass a variable via the command line.

- terraform providers get provider info used in configuration.

- Main purpose is declare resources.

- Blocks are containers for objects like resources.

- Arguments assign a value to a name.

- Expressions represent a value.

- Modules are a collection of .tf and/or .tf.json files kept together in a directory. A module consists of only the top-level config files in the directory. A nested directory is treated as a separate module and may not automatically included.

- Identifiers are things like argument names, block type names, resources, input variables, and etc.

- You can add comments with the #, //, and /* */ characters.

- Resource blocks describe infrastructure objects like virtual networks, compute instances, or components like DNS records.

- We have three resource types:
    
    - Providers which are plugins for Terraform that offers a collection of resource types.
    
    - Arguments which are specific to the selected resource type.
    
    - Documentation which every provider uses to describe its resource types and arguments.
    

- Meta arguments can be used with any resource type to change the behavior of the resource.
    
    - depends_on specify hidden dependencies that Terraform can’t automatically infer.
    
    - count creates multiple resource instances according to a count.
    
    - for_each creates multiple instances according to a map or a set of strings.
    
    - provider select a non-default provider configuration.
    
    - lifecycle set lifecycle customizations.
    
    - provisioner and connection take extra actions after resource creation.
    

- timeouts are nested block arguments that allow for customization of how long certain operations are allowed to take before they are deemed failed.

![screenshot](../../../images/Screenshot_2022-10-26_163854.png)

- Terraform keeps track of all the resources and their details in a “state” file.

- Three variable base types are string, number, bool. Complex types are list, set, map, object, tuple.

- [https://docs.microsoft.com/en-us/azure/developer/terraform/create-avd-log-analytics-workspace](https://docs.microsoft.com/en-us/azure/developer/terraform/create-avd-log-analytics-workspace)