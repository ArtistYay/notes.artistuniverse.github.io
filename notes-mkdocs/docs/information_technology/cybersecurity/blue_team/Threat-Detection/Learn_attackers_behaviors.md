---
tags:
  - Cybersecurity
  - Defensive Security
---

That's where the ['*Pyramid of Pain*'](https://detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html) and ['*MITRE ATT&CK Framework*'](https://attack.mitre.org/) come in. These two help a lot with creating detections in enterprise environments.

Attacks can be really sophisticated or just a simple misconfiguration. Having a good understanding of attack vectors helps when you're writing detection rules, and knowing how to use ATT&CK to focus on TTPs is best practice.

## How to read the MITRE ATT&CK framework

Before we get into the matrix we have to understand TTPs:

- Tactics: what's the goal of the attack? Are they trying to get initial access, or do they want to move laterally?
- Techniques: how are they going to get initial access or move laterally? Are they going to use compromised credentials or phishing?
- Procedures: the exact steps they take to pull off those tactics and techniques. Are they going to email an employee a malicious link that asks for their credentials?

I'll use the [Windows Matrix](https://attack.mitre.org/matrices/enterprise/windows/)

## How does the '*MITRE ATT&CK Framework*' link to the '*Pyramid of Pain*'?

The MITRE ATT&CK framework provides the detailed "what" (TTPs, tactics, techniques, procedures) of an attack, while the Pyramid of Pain provides the "why" (the cost and effort for an adversary to evade detection) for defenders to prioritize their efforts. Defenders can map ATT&CK TTPs to the Pyramid of Pain to identify which behaviors are most difficult for attackers to change and focus their defensive strategies and detection efforts on these higher-level, more impactful areas.

One way to annoy an attacker is to learn how brute forcing works. Brute forcing isn't cheap, and having a timeout/lockout after failed attempts can really annoy people (trust me). When I set up account lockouts, I'm not just blocking one attack, I'm forcing the attacker to abandon their entire brute force strategy. This is exactly what the Pyramid of Pain means by 'painful' indicators. TTPs (like brute force methodology) are at the top because changing them requires significant effort and expertise.

Here are some examples from different levels:
- Level 1 (Low Pain): Attacker uses different IP → I block new IP → Cat and mouse game continues.

- Level 2 (Medium Pain): I implement rate limiting → Attacker slows down attempts → Still using same strategy.

## Links

https://www.reddit.com/r/cybersecurity/comments/1i3dosy/how_do_you_use_the_pyramid_of_pain/
