---
tags:
  - Microsoft Azure
---

## Questions

1. Which PowerShell cmdlet must execute prior to using `Get-AzRecoveryServicesBackupJob`?

    `Set-AzRecoveryServicesVaultContext`

2. Which statement regarding Azure VM backups is correct?

    The initial VM recovery point takes longer than subsequent ones.

3. A backed up item contains the following data:

    Resource Group: MyRG
    Subscription Id: 00000000
    Vault Name: demoVault
    API version: 2022-04-20

4. How would you validate the operation for this item?

    `POST https://management.azure.com/resourceGroups/myRG/ subscriptions/00000000/providers/Microsoft.RecoveryServices/ vaults/demoVault/backupValidateOperation?api-version=2022-04-20` the subscription always goes first.

5. Which `New-AzResourceGroupDeployment` cmdlet parameter passes the template’s parameter values?

    `-TemplateParameterFile`

6. Which Azure CLI command prefix deploys resources using an ARM template?

    `az deployment group create`

7. You must fetch a list of recovery points using Azure Site Recovery. You must fetch the points using a replication protected `item` object. How can you do this using PowerShell?

    `**Get-AzRecoveryServicesAsrRecoveryPoint -ReplicationProtectedItem $item**`

8. You are using Powershell to fetch Azure backup jobs for a vault. Which Powershell cmdlet will you run?

    `Get-AzRecoveryServicesBackupJob`

9. You created a virtual machine (VM) that's configured to serve web requests on the standard Transmission Control Protocol (TCP) port 80. What priority value is allowed while creating an inbound security rule?

    A value that is less than 65,500 and higher in priority than the default catch-all deny inbound rule

10. You have downloaded and installed the Microsoft Azure Site Recovery Unified Setup for migration of on-premises physical machines to Azure. Which command creates management accounts on the Configuration Server?

    cspsconfigtool

11. Your Azure Resource Manager (ARM) template must specify a single data disk added to newly deployed virtual machines. What is missing from the following ARM template syntax?

    ```JSON
    "dataDisks": [{
                  "diskSizeGB": 1023,
                  "createOption": "Empty"
                }
    ```
    `"lun": 1,`

12. You have failed over an on-premises virtual machine for migration to Azure. After verifying the failover completion on the Jobs page, what should you do next?

    Choose the “Complete Migration” option

13. You must specify a Domain Name System (DNS) domain name for a virtual machine network interface. How can you confirm the availability of `contoso.centralus.cloudapp.azure.com`?

    `Test-AzDnsAvailability -DomainNameLabel contoso -Location centralus`

14. You must add an existing managed data disk to an existing Azure virtual machine. Which PowerShell statement will accomplish this?

    `$vm = Add-AzVMDataDisk -CreateOption Attach -Lun 0 -VM $vm -ManagedDiskId $disk.Id`

15. Which PowerShell cmdlet deploys an Azure Resource Manager (ARM) template?

    `New-AzArmResourceGroupDeployment`

16. Which Powershell cmdlet results in the following output?

```powershell
DisplayName
----------
East Asia
Southeast Asia
Central US
East US
East US 2
West Us
North Central US
South Central US
North Europe
West Europe 
```

`Get-AzRegion | select DisplayName`
