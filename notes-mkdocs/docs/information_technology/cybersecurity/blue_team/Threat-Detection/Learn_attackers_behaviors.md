That's where the ['*Pyramid of Pain*'](https://detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html) and ['*MITRE ATT&CK Framework*'](https://attack.mitre.org/) comes in. These two sources help with creating detections in enterprise environments.

Attacks can range from being sophisticated to a very simple mis configuration. Having a good understanding of attack vectors can help in the threat detection process of making rules. Knowing how to use ATT&CK to focus on TTPs is best practice. 

# How to read the MITRE ATT&CK framework

Before we get into the matrix we have to understand TTPs:
	Tactics: what is the goal attack? are they trying to achieve initial access or do they want to do lateral movement?
	Techniques: how are they going to achieve initial access or lateral movement? Are they going to leverage compromised credentials or phishing? 
	Procedures: the steps they use to achieve their tactics & techniques, are they going to send an email to an employee to click a malicious link asking for their credentials?

I will use the [Windows Matrix](https://attack.mitre.org/matrices/enterprise/windows/) 

# How does the '*MITRE ATT&CK Framework*' link to the '*Pyramid of Pain*'?

The MITRE ATT&CK framework provides the detailed "what" (TTPs, tactics, techniques, procedures) of an attack, while the Pyramid of Pain provides the "why" (the cost and effort for an adversary to evade detection) for defenders to prioritize their efforts. Defenders can map ATT&CK TTPs to the Pyramid of Pain to identify which behaviors are most difficult for attackers to change and focus their defensive strategies and detection efforts on these higher-level, more impactful areas. 

An example to annoy an attacker is learn the strategies of brute forcing, doing that is not cheap and having a time/lockout whenever a failed attempt is made can annoy people (trust me). When I set up account lockouts, I'm not just blocking one attack, I'm forcing the attacker to abandon their entire brute force strategy. This is exactly what the Pyramid of Pain means by 'painful' indicators. TTPs (like brute force methodology) are at the top because changing them requires significant effort and expertise.

Here's some other examples from each level:
- Level 1 (Low Pain): Attacker uses different IP → I block new IP → Cat and mouse game continues.
    
- Level 2 (Medium Pain): I implement rate limiting → Attacker slows down attempts → Still using same strategy.

# Links

https://www.reddit.com/r/cybersecurity/comments/1i3dosy/how_do_you_use_the_pyramid_of_pain/