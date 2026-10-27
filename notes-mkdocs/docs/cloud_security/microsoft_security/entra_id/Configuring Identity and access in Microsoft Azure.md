---
tags:
  - Microsoft Azure
  - Identity & Access Management
---

!!! note "Name changes"
    These are practice questions from an older course. Azure AD (Azure Active Directory) is Microsoft Entra ID now. I kept the old name in the questions and fixed the answers that changed.

1. A security principal with a custom RBAC role can regenerate the keys of a Service Bus namespace, but can't read the connection string. None of its other actions are affected. What might be causing this?

    The custom role is missing `Microsoft.ServiceBus/namespaces/authorizationRules/listkeys/action` from its Actions property.

1. Which Azure AD sign-in method lets you use modern cloud features while only storing user passwords on-prem?

    Pass-through authentication

1. You want to create dynamic groups in Azure AD for each department in your company. You start with a new security group with the membership type Dynamic User for the Sales team. What do you write in the dynamic membership rules?

    ```text
    user.department -eq "Sales"
    ```

1. What's a risk of giving someone the Application Administrator role in Azure AD?

    They can impersonate an application's identity. They can add credentials to apps, so if an app has more permissions than they do, they can use it to escalate.

1. You want to give a user the Owner role on a resource group, but only for a set time with a start and end date. What do you do?

    Use Privileged Identity Management (PIM) and make the user eligible for the Owner role on that resource group.

1. How do you read the properties and relationships of a service principal object?

    With Microsoft Graph:

    ```text
    GET https://graph.microsoft.com/v1.0/servicePrincipals/{id}
    ```

1. Per-user MFA is turned on for every account in your organization. When users are enabled individually, they do MFA every time they sign in. What's an exception to that?

    When they sign in from a trusted IP address. Per-user MFA is the legacy way of doing this though. Microsoft recommends Conditional Access policies now.

1. While investigating a possible incident, you see privileged access was used at a weird time. How do you check if using that privileged identity was legit?

    Check the PIM audit history and look at the reason and time for the activation request.

1. Your organization does a quarterly access review on everyone with privileged roles. When the quarter is closing, what should you do?

    Go over the access review results and apply them. You can also set it to auto-apply the results.

1. Compared to the other options, which Azure AD sign-in method needs the most stuff deployed on-prem?

    Federated authentication (AD FS needs its own servers and proxies).

1. Which Azure AD feature lets password changes made in the cloud show up on-prem?

    Password writeback

1. Which licenses do you need to use Privileged Identity Management (PIM)?

    Microsoft Entra ID P2 or Microsoft Entra ID Governance. You also get P2 with bundles like Microsoft 365 E5 or Enterprise Mobility + Security E5.

1. You have an app in Azure App Service that keeps its secrets in Azure Key Vault. How do you get to the key vault securely?

    Turn on a system-assigned managed identity for the App Service, then give that identity the Key Vault Secrets User role on the key vault (or a Get secrets access policy if the vault still uses access policies).

    I originally had the Reader role here, but that's wrong. Reader is control plane only, it can see the vault exists but it can't read any secret values.

1. How do you get a list of users who are external to the tenant (guests)?

    ```powershell
    Get-MgUser -Filter "userType eq 'Guest'" -All
    ```

    This used to be `Get-AzureADUser`, but the AzureAD PowerShell module is retired. Microsoft Graph PowerShell (`Get-MgUser`) is the replacement.
