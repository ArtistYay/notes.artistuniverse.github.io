### AI Basics

1.  What is a token, and why does it cost money?

Tokens are not letters, words, are phares but how a LLM process text sent to it. The reason why it’s so costly is because of the computation. Processing tokens require GPU operations to do mathematical operations (Byte Pair Encoding).

[AI Tokens Explained: What They Are and Why They Cost Money - Beginners in AI](https://beginnersinai.org/ai-tokens-explained/)

[Tech in Five - Tokens & Tokenomics - YouTube](https://www.youtube.com/watch?v=PbngY1n4Awc&t=2s)

2.  What is the context window and what happens when you exceed it?

Context window is basically the LLM’s memory. Once that gets fill the agent starts “replacing” old text/phrases/ etc. Reminds me of a database’s buffer pool.

3.  What does temperature actually change?
4.  What is an embedding and how is it different from a token?
5.  What's the difference between fine-tuning, RAG, and prompting, and when do you reach for each?

Fine-tuning – taking a base model and feeding all the data that matters to you so it can learn your style and specialty. You would need it when a specific use case like an application chat bot for a product.

RAG – is a separate library the model can look through. I can have company documents, sensitive files, etc. to feed the model more context. An example to use RAG is making an internal LLM model for a model and may need sensitive documents for context.

Prompting – being specific in your request for the model. When you need certain information specific to what your doing is an example of using prompting.

[Fine-Tuning vs Prompting vs RAG: When to Use What - Beginners in AI](https://beginnersinai.org/fine-tuning-vs-prompting-vs-rag/#When_to_use_fine-tuning)

6.  What is a system prompt and why is it not a security boundary?

A system prompt is not instructions but an invisible message you give the LLM to set it’s role and behavior. A system prompt is not enforced by guardrails, or code nor is it monitored. It can also be changed with some good prompt injection.

Topic is still new so there isn’t too much research or findings out there.

[System Prompt Leakage: Why Your “Secret Prompt” Isn’t a Security Boundary ~ Davinder Tutorials](https://www.davindertutorials.com/2026/09/system-prompt-leakage-why-your-secret.html)

7.  Why do models hallucinate, and what kinds of hallucinations are dangerous?

Models get trained with all sorts of data, sometimes said data can be fake or untrue. Sometimes the LLM doesn’t have the data the user is asking for and makes sure it answers the prompt, it makes things up on the fly.

[Tim and Moby Explains](https://youtu.be/oiLcc9RSfCE?si=DPIEba4AuuniD8_z)