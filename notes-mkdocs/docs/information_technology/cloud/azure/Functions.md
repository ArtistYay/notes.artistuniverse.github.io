---
tags:
  - Azure
Keyword: Compute
---
- Functions are something like AWS Lambda, it’s code running on your service.

- Functions are commonly used when you need to perform work in response to an event, timer, or message from another Azure service.

- Functions can be either stateless or stateful. When they're stateless (the default), they behave as if they're restarted every time they respond to an event. When they're stateful (called Durable Functions), a context is passed through the function to track prior activity.

- Logic apps are similar to functions. Both enable you to trigger logic based on an event. Where functions execute code, logic apps execute _workflows_ that are designed to automate business scenarios and are built from predefined logic blocks.