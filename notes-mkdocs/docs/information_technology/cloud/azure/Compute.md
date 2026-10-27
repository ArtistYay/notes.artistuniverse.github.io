---
tags:
  - Microsoft Azure
  - Compute
---

- `Set-AzRecoveryServicesVaultContext` must run before `Get-AzRecoveryServicesBackupJob`.

- The initial VM recovery point takes longer than subsequent ones.

- `New-AzResourceGroupDeployment` uses `-TemplateParameterFile` to pass parameter values.

- `az deployment group create` deploys resources using an ARM template.

- An inbound NSG rule for a web VM on port 80 needs a priority between 100 and 4096 (custom rules can't go outside that range). Lower number = higher priority, and any custom rule beats the default rules, which sit at 65000 to 65500.

- `cspsconfigtool` creates management accounts on the Configuration Server for Site Recovery migrations. (That's the classic VMware-to-Azure setup. The modernized experience uses the Azure Site Recovery replication appliance instead.)

- ARM data disk syntax needs a `"lun"` (logical unit number) value.

- After failover completion, choose "Complete Migration" on the Jobs page.

- `Test-AzDnsAvailability -DomainNameLabel contoso -Location centralus` checks DNS name availability.

- `Add-AzVMDataDisk -CreateOption Attach -Lun 0 -VM $vm -ManagedDiskId $disk.Id` attaches an existing managed disk.

- `Get-AzLocation | Select-Object DisplayName` lists region display names.

Tips from the community:
 
- Adam Bertram, a Microsoft Cloud and Datacenter Management MVP, flags a gotcha that's easy to miss: even with Geo-Redundant Storage turned on, you can't restore directly from the secondary region. You have to explicitly enable Cross-Region Restore ahead of time if you want that option available during a regional outage.
  [Azure Backup: Pricing, Best Practices, & Common Pitfalls to Avoid](https://n2ws.com/blog/microsoft-azure-cloud-services/azure-backup-basics)
