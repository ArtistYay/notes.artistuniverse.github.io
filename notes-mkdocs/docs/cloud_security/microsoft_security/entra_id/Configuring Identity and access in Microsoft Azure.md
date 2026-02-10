---
tags:
  - Azure
  - Questions
Date: 2023-08-10
---
1. A security principal with a custom RBAC definition is able to regenerate the keys of a Service Bus namespace , but cannot read the connection string. None of the security principal's other actions are affected. What might be causing this?
    
    The custom RBAC definition is missing “Microsoft.ServiceBus/namespaces/authorizationRules/listkeys/action” from the Actions property.
    

1. Which sign-in method in Azure AD allows you to leverage modern cloud-grade features while storing user passwords only on-premises?
    
    Pass-through authentication
    

1. You want to create dynamic groups in Azure AD for users belonging to each department in your company. You start with a new Security Group with the membership type Dynamic User for the Sales team. What should you write in the Dynamic membership rules blade?
    
    ```JavaScript
    user.department -ep “Sales”
    ```
    

1. What is a risk of assigning the Application Administrator directory role to a user in Azure AD?
    
    The user can impersonate an application identity.
    

1. You want to delegate the Owner role to a user in a resource group in Microsoft Azure. Given this request, what would you do to assign time-bound access to this role using start and end dates?
    
    Enable Privileged Identity Management (PIM) and grant the user eligibility to the owner on the resource group.
    

1. Which method in JSON is used to read the properties and relationships of a Service Principal Object in App Registration?
    
    ```JavaScript
    Get servicePrincipal
    ```
    

1. For each account from your organization, the per-user Azure Multi-Factor Authentication is enabled. When users are enabled individually, they perform multi-factor authentication each time they sign-in. What is an exception to this default behavior?
    
    When users sign in from a trusted IP addresses.
    

1. While investigating a suspected security incident, you see that access was used at a suspicious time. How would you clarify if the usage of a privileged identity was legitimate?
    
    Check the Azure PIM audit history and review the reason and time for the elevated request.
    

1. Your organization runs a quarterly access review on all users with privileged roles. When the access review's quarter is closing, what actions should you take?
    
    Review the access review in the Azure Portal and apply it.
    

1. In comparison to other methods, which sign-in method in Azure AD needs more resources to be deployed for operation on-premises?
    
    Federated authentication
    

1. Which Azure AD feature allows password changes made on the cloud to be reflected on-premises?
    
    Password writeback
    

1. Which Azure Active Directory (AAD) licenses are required to enable Privileged Identity Management (PIM)?
    
    Azure AD Premium P2, Enterprise Mobility + Security E5, or Microsoft 365 M5
    

1. You are working with an application running in Azure App Service that uses an Azure Key Vault to store secrets. How can you securely access the key vault?
    
    Enable System assigned managed identity on the App Service, then grant the Reader role scoped to Key Vault to the newly created App Service identity.
    

1. Which snippet would you use to get a list of users who are external to the Azure AD tenant?
    
    ```JavaScript
    Get-AzureADUser -Filter “UserType eq ‘Guest’ “ -All $true
    ```