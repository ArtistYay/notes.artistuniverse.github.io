---
tags:
  - Generative AI
---

## What's the difference between a chatbot and an agent?

Autonomy. A chatbot is reactive. You send a message, it answers, it waits. You're driving every step.

An agent gets a goal, some tools, and a loop. It decides what to do, does it, looks at the result, and decides again until the task is done or it hits a stopping point. You give it the destination and it figures out the route.

## How does an agent actually use tools?

Through function calling (also called tool calling). The model can't run anything itself, it only outputs text. So the app hands it a list of tools with descriptions, the model replies with a structured request like "call `search_signin_logs` with these arguments," and the app is the one that actually runs it. The result goes back into the context window and the model keeps going.

The more an agent gets to pick its own tools and act without checking with you first, the more agentic it is.

On the Microsoft side, Microsoft Agent Framework is the SDK for building agents now. It's the successor to Semantic Kernel and AutoGen and it's made by the same teams.

[Documentation | Microsoft Learn](https://learn.microsoft.com/agent-framework/overview/)

## What is MCP?

The Model Context Protocol (MCP) is an open standard Anthropic released in November 2024 for connecting AI apps to tools and data. Before MCP, every app needed its own custom integration for every tool. Now a tool gets wrapped as an MCP server once, and any MCP client (Claude Code, VS Code, Microsoft Foundry agents) can use it. Kind of like USB-C for AI tools.

The security catch is that an MCP server is just code running with whatever access you give it. A sketchy one can leak tokens or hide instructions in its tool descriptions (tool poisoning). OWASP has a whole MCP Top 10 for this.

[Documentation | Model Context Protocol](https://modelcontextprotocol.io/)

[Documentation | OWASP](https://owasp.org/www-project-mcp-top-10/)

## Why does this matter for security?

The agent loop (get goal, plan, act, check result, repeat) is what Security Copilot agents, Claude Code, and SOAR-style automations all run on. It's also the risk. An agent with tools can do real damage if it gets tricked, and that's exactly what prompt injection goes after (see [AI Flaws](ai_flaws.md)). OWASP calls this LLM06:2025 Excessive Agency.

Microsoft's guidance lines up with what we'd do for any service account:

- Least privilege: give the agent only the permissions it needs, and only for as long as it needs them.
- Human in the loop: anything risky (deleting, sending, changing permissions) gets approved by a person first.
- Logging: every tool call should be logged so you can actually investigate when something goes wrong.

[Documentation | Microsoft Learn](https://learn.microsoft.com/security/zero-trust/sfi/defend-indirect-prompt-injection)
