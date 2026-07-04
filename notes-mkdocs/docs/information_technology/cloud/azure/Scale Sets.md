---
tags:
  - Microsoft Azure
---

- Let you create and manage a group of identical load balanced VMs.

- High Availability, if one VM fails or stops, the others in the scale set will keep working.

- Auto Scaling automatically matches demand by adding or removing VMs from the scale set.

- Run up to 1000 VMs in a single scale set.

- No added cost for using scale sets

**Tips from the community:**
 
- Nicolas Prigent, a Microsoft MVP in Cloud and Datacenter Management, frames it simply: building identical VMs by hand and then scaling them up or down manually doesn't hold up at any real scale. That management overhead is exactly what Scale Sets remove.
  [Understanding Azure Virtual Machine Scale Sets – BDRSuite](https://www.bdrshield.com/blog/virtual-machine-scale-sets-azure/)
  
- Flexible orchestration is now the recommended mode over Uniform. It gives you standard Azure VM APIs, so RBAC, resource tagging, Azure Backup, and Site Recovery all work normally, none of which fully work with Uniform-mode instances.
  [Orchestration modes for Virtual Machine Scale Sets – Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-orchestration-modes)
