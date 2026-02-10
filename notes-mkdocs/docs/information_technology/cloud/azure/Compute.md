---
tags:
  - Azure
Keyword: Compute
---
- Questions
    
    1. Which PowerShell cmdlet must execute prior to using `Get-AzRecoveryServicesBackupJob`?
        
        1. `Set-AzRecoveryServicesVaultContext`
        
    
    1. Which statement regarding Azure VM backups is correct?
        
        1. The initial VM recovery point takes longer that subsequent ones.
        
    
    1. **A backed up item contains the following data:**
        
        **Resource Group: MyRG**
        
        Subscription Id: 00000000
        
        Vault Name: demoVault
        
        API version: 2022-04-20
        
        How would you validate the operation for this item?
        
        1. `POST https://management.azure.com/resourceGroups/myRG/ subscriptions/00000000/providers/Microsoft.RecoveryServices/ vaults/demoVault/backupValidateOperation?api-version=2022-04-20` the subscription always goes first.
        
    
    1. Which `New-AzResourceGroupDeployment` cmdlet parameter passes the template’s parameter values?
        
        1. `-TemplateParameterFile`
        
    
    1. Which Azure CLI command prefix deploys resources using an ARM template?
        
        1. `az deployment group create`
        
    
    1. You must fetch a list of recovery points using Azure Site Recovery. You must fetch the points using a replication protected `item` object. How can you do this using PowerShell?
        
        1. `**Get-AzRecoveryServicesAsrRecoveryPoint -ReplicationProtectedItem $item**`
        
    
    1. You are using Powershell to fetch Azure backup jobs for a vault. Which Powershell cmdlet will you run?
        
        1. `Get-AzRecoveryServicesBackupJob`
        
    
    1. You created a virtual machine (VM) that's configured to serve web requests on the standard Transmission Control Protocol (TCP) port 80. What priority value is allowed while creating an inbound security rule?
        
        1. A value that is less than 65,500 and higher in priority than the default catch-all deny inbound rule
        
    
    1. **You have downloaded and installed the Microsoft Azure Site Recovery Unified Setup for migration of on-premises physical machines to Azure. Which command creates management accounts on the Configuration Server?**
        
        1. cspsconfigtool
        
    
    1. **Your Azure Resource Manager (ARM) template must specify a single data disk added to newly deployed virtual machines. What is missing from the following ARM template syntax?**
    
    ```Plain
    "dataDisks": [{
                  "diskSizeGB": 1023,
                  "createOption": "Empty"
                }
    ```
    
    1. `"lun": 1,`
    

1. You have failed over an on-premises virtual machine for migration to Azure. After verifying the failover completion on the Jobs page, what should you do next?
    
    1. Choose the “Complete Migration” option
    

1. You must specify a Domain Name System (DNS) domain name for a virtual machine network interface. How can you confirm the availability of `contoso.centralus.cloudapp.azure.com`?
    
    1. `Test-AzDnsAvailability -DomainNameLabel contoso -Location centralus`
    

1. You must add an existing managed data disk to an existing Azure virtual machine. Which PowerShell statement will accomplish this?
    
    1. `$vm = Add-AzVMDataDisk -CreateOption Attach -Lun 0 -VM $vm -ManagedDiskId $disk.Id`
    

1. Which PowerShell cmdlet deploys an Azure Resource Manager (ARM) template?
    
    1. `New-AzArmResourceGroupDeployment`
    

1. Which Powershell cmdlet results in the following output?

```Plain
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

1. `Get-AzRegion | select DisplayName`