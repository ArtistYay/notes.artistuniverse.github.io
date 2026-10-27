---
tags:
  - Generative AI
---

## Why does a model need outside knowledge?

An LLM only knows what it was trained on. That has a cutoff date and it definitely doesn't include your company's private docs. Prompting, RAG, CAG, and fine-tuning are all ways to get the model what it's missing.

## What's the difference between fine-tuning, RAG, and prompting, and when do you reach for each?

Microsoft's guidance is to start with prompting, add RAG when you need your own data, and only fine-tune after you've measured that the first two aren't cutting it. They aren't either/or, a lot of real apps use all three together.

Prompting: being specific in your request and giving the model the context, examples, and format you want back. This is always step one because it's free and you can change it in seconds. Reach for it when the model already knows enough and just needs direction, like "write a KQL query against SigninLogs that only returns failed sign-ins from the last 24 hours."

RAG (retrieval-augmented generation): a separate library the model can look through. When you ask a question, the app searches your documents (company docs, runbooks, policies), grabs the most relevant chunks, and puts them in the context window next to your question. The model answers from those chunks. Reach for it when the answer depends on private or up-to-date data, or when you need to show where the answer came from. Example: an internal assistant that answers questions from your security policies and runbooks.

Fine-tuning: training a base model more on a set of example inputs and correct outputs so it learns a style, a format, or a narrow task. Reach for it when prompting can't get the behavior consistent (like always returning the same JSON structure), or when you want a smaller, cheaper model to do one specific job as well as a big one. Microsoft's example is fine-tuning a small model to turn plain English questions into SQL for their specific schema.

!!! note "What I got wrong"
    I originally wrote that fine-tuning is "feeding all the data that matters to you." It can add domain knowledge, but for facts that change or need access controls, RAG is the better fit. Fine-tuned facts are baked in until you retrain, and the model can't tell you which document it got them from. Fine-tuning on bad data also makes the model worse, and a deployed fine-tuned model in Azure OpenAI charges hosting by the hour even when nobody is using it.

[Fine-Tuning vs Prompting vs RAG: When to Use What - Beginners in AI](https://beginnersinai.org/fine-tuning-vs-prompting-vs-rag/#When_to_use_fine-tuning)

[Documentation | Microsoft Learn](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/customizing-llms)

## What's the security catch with RAG?

Two things:

1. RAG has to respect permissions. If the search step pulls a document the user isn't allowed to see, the model will happily summarize it for them. The retrieval has to filter by the user's access before anything goes into the context window.
2. Every document you retrieve is a way in for indirect prompt injection. If someone plants instructions in a doc your RAG pipeline reads, the model reads them too (more on that in [AI Flaws](ai_flaws.md)).

## What is CAG?

Cache-augmented generation (CAG) skips the search step. You load the whole knowledge base into the context window up front, and the provider caches it (prompt caching) so you're not paying full price or waiting on it every request. It's faster and simpler than RAG, but it only works when the data is small enough to fit and doesn't change much. RAG is still the default when you've got a lot of data.

## What are vector databases and grounding?

A vector database stores [embeddings](tokens_and_embeddings.md) so you can search by meaning instead of by exact keywords. "Find me docs similar to this idea" instead of "find me docs containing these words." Azure AI Search, Cosmos DB, Azure SQL, PostgreSQL with pgvector, Pinecone, and Weaviate can all do this.

Grounding means tying the model's answer to real data you handed it, and RAG is the most common way to do it. Grounding cuts down on hallucinations but doesn't get rid of them, since the model can still misread or overstate what's in the doc.
