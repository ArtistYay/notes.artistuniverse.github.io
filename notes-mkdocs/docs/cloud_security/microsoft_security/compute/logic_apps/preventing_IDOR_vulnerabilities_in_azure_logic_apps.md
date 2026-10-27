---
tags:
  - Microsoft Azure
  - Cybersecurity
  - Compute
---

## What is a Logic App?

A cloud-based service in Azure that lets us build and run automated workflows that connect different apps, systems, and services together. Sentinel playbooks are Logic Apps too.

[Documentation | Microsoft Learn](https://learn.microsoft.com/azure/logic-apps/logic-apps-overview)

## Discovery and Reconnaissance

### IDOR Vulnerability

IDOR (Insecure Direct Object Reference) is a vulnerability where an app gives you direct access to objects based on input you control. In simple terms, an attacker can change something like a URL or a form parameter and get to data they're not supposed to see.

```text
https://prod-32.southeastasia.logic.azure.com/workflows/<workflow-id>/triggers/manual/paths/invoke/{name}?api-version=2018-07-01-preview&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=<SAS-signature>
```

> In the name parameter I can change it to admin, and if the Logic App has an IDOR vulnerability in its logic, it can send back sensitive data.

!!! warning "The sig is a secret"
    The `sig` value at the end of a Logic App trigger URL is a SAS signature. Anyone who has the full URL can call the trigger, so treat it like a password and don't post it anywhere.

#### Prevention

1. Never trust a URL parameter to decide who someone is. That should come from an authenticated token. Use OAuth 2.0 with Entra ID authentication on your Logic App trigger. [Documentation | Microsoft Learn](https://learn.microsoft.com/azure/logic-apps/logic-apps-securing-a-logic-app?tabs=azure-portal#secure-action-parameters)

2. You can restrict who calls the trigger (in this case the [Request trigger](https://learn.microsoft.com/azure/connectors/connectors-native-reqres?tabs=consumption#add-a-request-trigger)):
    1. Require a Shared Access Signature (SAS) token.
    2. Only allow specific Entra ID service principals in the authorization policy of the Logic App.
    3. Put [Azure API Management (APIM)](https://learn.microsoft.com/community/content/secure-integration-workflows-azure-logic-apps-api-management) in front of it so auth policies get enforced before the Logic App ever runs.

## HTTP Method Tampering

Make sure your endpoints have an allowlist of which HTTP methods are allowed and which aren't. Put Azure API Management (APIM) in front of your Logic App. APIM lets you write policies that restrict which HTTP methods each endpoint accepts, and it rejects anything else before it ever hits your Logic App.

![screenshot](../../../images/http_tampering.png)
> In this image you can see I changed the HTTP method in the developer tools, which got me the flag.

## Reads From The Wild

- [Managed Identity Attack Paths, Part 2: Logic Apps](https://specterops.io/blog/2022/06/07/managed-identity-attack-paths-part-2-logic-apps/?source=rss----f05f8696e3cc---4)
