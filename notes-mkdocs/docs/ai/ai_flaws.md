---
tags:
  - Generative AI
---

## Why do models hallucinate, and what kinds of hallucinations are dangerous?

A hallucination is when the model says something wrong with full confidence. Not a typo. More like making up a citation, a CVE, or a PowerShell cmdlet that doesn't exist.

Part of what I first wrote is right. Training data has wrong stuff in it, and when the model doesn't have the answer it still answers anyway. The bigger reason is how LLMs work. They predict the most likely next token, not the true one. If a made-up answer fits the pattern better than "I don't know," the made-up answer wins.

Training also tends to reward guessing over admitting it doesn't know. It's like a multiple choice test where leaving it blank is a guaranteed zero but guessing might get you points. OpenAI's 2025 paper "Why Language Models Hallucinate" makes that argument.

The dangerous ones for security work:

- Fake packages. The model suggests a pip or npm package that doesn't exist, and attackers register those names with malware in them ("slopsquatting"). Copy-paste the install command and you just ran their code. That's a supply chain attack (OWASP A03:2025).
- Wrong queries and commands. KQL that runs fine but quietly misses events, so your detection has a blind spot you don't know about. Or an `az` command with the wrong flags.
- Made-up CVEs and compliance requirements. Now you're remediating the wrong thing or giving an auditor the wrong answer.
- Fake citations. Lawyers in Mata v. Avianca (2023) got sanctioned for filing a brief with court cases ChatGPT made up.

The scary hallucinations are the ones that look right and don't fail loudly. Check anything that matters against the real source (Microsoft Learn, NVD, the package registry) before you use it. OWASP lists this as LLM09:2025 Misinformation.

[Tim and Moby Explains](https://youtu.be/oiLcc9RSfCE?si=DPIEba4AuuniD8_z)

## What is a system prompt and why is it not a security boundary?

A system prompt is the hidden message the app sends before your chat that sets the model's role, rules, and behavior. Something like "You're a SOC assistant. Only answer security questions."

!!! note "What I got wrong"
    I originally wrote that a system prompt is "not instructions." It is instructions. The point is that nothing enforces them.

The system prompt is just text sitting in the same context window as everything else. The only thing making it work is the model choosing to follow it. No code checks it, and the model can't reliably tell the developer's instructions apart from the user's message or text inside a document. That means:

1. It can be overridden. Good prompt injection can get the model to ignore it.
2. It can leak. Users can often get the model to repeat it back, so never put secrets, API keys, or internal URLs in a system prompt.
3. It's not access control. "Don't show salary data to non-HR users" in a system prompt doesn't stop anything. The app has to check permissions before the data ever gets to the model.

A system prompt is like an "Employees Only" sign on a door. The badge reader is the actual security boundary.

I also said this topic was too new to have much research. That's outdated. OWASP lists it as LLM07:2025 System Prompt Leakage, and Microsoft's own guidance is to design your system assuming prompt injection will happen.

[System Prompt Leakage: Why Your "Secret Prompt" Isn't a Security Boundary ~ Davinder Tutorials](https://www.davindertutorials.com/2026/09/system-prompt-leakage-why-your-secret.html)

[Documentation | OWASP](https://genai.owasp.org/llm-top-10/) - OWASP Top 10 for LLM Applications 2025.

## What is prompt injection?

Prompt injection is tricking the model into following an attacker's instructions instead of yours. OWASP has it at the top of the list as LLM01:2025.

There are two kinds:

- Direct: the user types it in themselves. "Ignore previous instructions and..."
- Indirect: the instructions are hidden in something the AI reads, like an email, a web page, a PDF, a ticket description, or white text on a white background. The user might have no idea. This is the scary one for agents, because an agent that reads a malicious email might then use its tools (send mail, run a query, change a setting) on the attacker's behalf.

The attack surface isn't only the model, it's the whole system built around it. Microsoft's defense-in-depth approach layers a few things because none of them are 100% on their own:

- Prompt Shields in Microsoft Foundry scan prompts and documents for injection attempts.
- Spotlighting marks outside content as untrusted so the model treats it as data, not instructions.
- Least privilege and human approval on agent tools, so a successful injection can't do much.
- Validating the model's output before your code acts on it.

For Microsoft 365 Copilot, jailbreak and injection detections show up as alerts in the Defender portal and Purview audit logs, which means you can hunt on them in Sentinel.

[Documentation | Microsoft Learn](https://learn.microsoft.com/security/zero-trust/sfi/defend-indirect-prompt-injection)

[Documentation | Microsoft Learn](https://learn.microsoft.com/microsoft-365/copilot/copilot-prompt-defense-in-depth)
