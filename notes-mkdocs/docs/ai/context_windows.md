---
tags:
  - Generative AI
---

## What is the context window?

The context window is basically the LLM's working memory. It's the max number of tokens the model can look at in one request, and that includes everything: the system prompt, the conversation history, any documents you pasted in, tool results, and the answer the model writes back. Input and output share the same budget.

Something that surprised me: the model doesn't remember anything between requests. Every time you send a message, the app re-sends the whole conversation. The "memory" you see in a chat app is just the app stuffing the history back into the context window each time.

## What happens when you exceed it?

I used to think the model starts "replacing" old text on its own. That's not quite it. If you send a raw API request that's over the limit, it just fails. Azure OpenAI sends back a 400 error and the model never sees it.

The replacing happens in the app around the model (the harness). Chat apps and agent tools like Claude Code or the Azure OpenAI Assistants API trim older messages or summarize them to make room. So my database buffer pool comparison still works, just one layer up. The app is the buffer manager deciding what gets evicted, not the model.

Also, being under the limit doesn't mean the model pays equal attention to everything. Stuff buried in the middle of a really long context is more likely to get missed (researchers call it "lost in the middle"). A bigger context window doesn't automatically mean better answers.

[Documentation | Microsoft Learn](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/assistants#context-window-management) - How the Assistants API truncates to fit.

## Why does this matter when building AI tools?

- Agents pile up tokens on every loop, because each tool call result gets added to the context.
- MCP tool definitions (the JSON that describes each tool) load into the context before you even ask anything. Connect a bunch of MCP servers and you've eaten space and money before any real work starts.
- Big documents need to be chunked, summarized, or pulled in with RAG instead of pasted in whole.

Deciding what goes into the context window, when, and how much of it is called context engineering. It's a real skill, and it's most of what separates an agent that works from one that falls apart halfway through a task.
