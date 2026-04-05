---
tags:
  - Microsoft Azure
  - Cybersecurity
  - Compute
---

## What is a Logic App?

Cloud-based service provided by Microsoft Azure that allows us to create and run automated workflows and integrate various applications, systems, and services. 

[Logic Apps](https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-overview)

## Discovery and Reconnaissonce

### IDOR Vulnerability 

IDOR, or Insecure Direct Object Reference, is a type of security vulnerability that occurs when an application provides direct access to objects based on user-supplied input. In simpler terms, it means that an attacker can manipulate input, such as URLs or form parameters, to gain unauthorized access to data.

`https://prod-32.southeastasia.logic.azure.com/workflows/676a2e295ed14be5a5ac394fc9cec59a/triggers/manual/paths/invoke/{name}?api-version=2018-07-01-preview&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=HGJxpIcv9207MyWGWJLYSR5tHgUQkpx8ER7U94uz9cg`

> In the name parameter I can change it to admin and if the Logic App have the IDOR vulnerability in it's code, it can output back sensitive data.

#### Prevention

1. Never use a URL parameter for verification, it should come from an authenticated token. [Secure Logic Apps](https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-securing-a-logic-app?tabs=azure-portal#secure-action-parameters)

Use OAuth 2.0/Entra ID authentication on your Logic App trigger.

2. You can restrict who calls the trigger (in this case [request](https://learn.microsoft.com/en-us/azure/connectors/connectors-native-reqres?tabs=consumption#add-a-request-trigger)).
    A. A required Shared Access Signature (SAS) token
    B. Whitelist specific Entra ID service principals in the "Authorization" section of the Logic App.
    C. Integrate with [Azure API Management (APIM)](https://learn.microsoft.com/en-us/community/content/secure-integration-workflows-azure-logic-apps-api-management) to enforce auth policies before the Logic App ever runs.

## HTTP Method Tampering

Make sure you are providing a whitelist to your endpoints on what HTTP request is allowed and not allowed. Use Azure API Management (APIM) in front of your Logic App. APIM lets you define policies that restrict which HTTP methods are allowed per endpoint, and rejects non-conforming requests before they ever hit your Logic App.

![screenshot](../../../images/http_tampering.png)
> In this image you can see I change the HTTP request in the developer tools which granted me the flag.


## Reads From The Wild

- [Managed Identity Attack Paths, Part 2: Logic Apps](https://specterops.io/blog/2022/06/07/managed-identity-attack-paths-part-2-logic-apps/?source=rss----f05f8696e3cc---4)