---
tags:
  - Microsoft Azure
  - Compute
---

- `Set-AzRecoveryServicesVaultContext` must run before `Get-AzRecoveryServicesBackupJob`.

- The initial VM recovery point takes longer than subsequent ones.

- `New-AzResourceGroupDeployment` uses `-TemplateParameterFile` to pass parameter values.

- `az deployment group create` deploys resources using an ARM template.

- Inbound security rule priority for a web VM on port 80 needs a value under 65,500 and higher priority than the default catch-all deny rule.

- `cspsconfigtool` creates management accounts on the Configuration Server for Site Recovery migrations.

- ARM data disk syntax needs a `"lun"` value specified.

- After failover completion, choose "Complete Migration" on the Jobs page.

- `Test-AzDnsAvailability -DomainNameLabel contoso -Location centralus` checks DNS name availability.

- `Add-AzVMDataDisk -CreateOption Attach -Lun 0 -VM $vm -ManagedDiskId $disk.Id` attaches an existing managed disk.

- `Get-AzRegion | select DisplayName` lists region display names.

**Tips from the community:**
 
- Adam Bertram, a Microsoft Cloud and Datacenter Management MVP, flags a gotcha that's easy to miss: even with Geo-Redundant Storage turned on, you can't restore directly from the secondary region. You have to explicitly enable Cross-Region Restore ahead of time if you want that option available during a regional outage.
  [Azure Backup: Pricing, Best Practices, & Common Pitfalls to Avoid](https://n2ws.com/blog/microsoft-azure-cloud-services/azure-backup-basics)
