---
tags:
  - Microsoft Azure
  - Compute
---

- Azure Functions are basically Azure's version of AWS Lambda: serverless code that runs when something triggers it.

- Functions are commonly used when you need to perform work in response to an event, timer, or message from another Azure service.

- Functions can be either stateless or stateful. When they're stateless (the default), they behave as if they're restarted every time they respond to an event. When they're stateful (called Durable Functions), a context is passed through the function to track prior activity.

- Logic apps are similar to functions. Both enable you to trigger logic based on an event. Where functions execute code, logic apps execute _workflows_ that are designed to automate business scenarios and are built from predefined logic blocks.

Tips from the community:
 
- Mark Heath, an Azure MVP, documents (without fully endorsing) a workaround people use for cold starts on the Consumption plan: a timer-triggered function pinging the app every 15-20 minutes to keep it warm. He's upfront that this is more of a hack exploiting a gap in consumption pricing than a real fix.
  [Avoiding Azure Functions Cold Starts | Mark Heath](https://markheath.net/post/avoiding-azure-functions-cold-starts)

- The officially recommended fix is different: use Flex Consumption or Premium, which both reduce cold starts while keeping dynamic scaling. Flex Consumption is Microsoft's recommended serverless plan now, and hosting on Linux in the old Consumption plan retires on September 30, 2028.
  [Azure Functions best practices | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-functions/functions-best-practices)
  
- Visual Studio & Development Technologies MVP Tamir Dresher wrote a clear early explainer of Durable Functions' orchestrator/activity model that's still a good plain-language intro.
  [Creating distributed workflows with Azure Durable Functions | Microsoft Learn (MVP Award Blog archive)](https://learn.microsoft.com/en-us/archive/blogs/mvpawardprogram/azure-durable-functions)
