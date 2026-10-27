---
tags:
  - Cybersecurity
  - Identity & Access Management
---

A JSON Web Key (JWK) is a key written as JSON. The Identity Provider (IdP) signs JSON Web Tokens (JWTs) with its private key, then publishes the matching public keys as a JWK Set (JWKS) so apps can verify the signature on every token they get.

You'll usually see it with the RS256 signing algorithm (ES256 is common too). In technical terms "A JSON object that represents a cryptographic key. The members of the object represent properties of the key, including its value."

## Key Rotation

Making sure a JWK is rotated often minimizes the impact of potential key compromise. If a key has been compromised an attacker can forge valid JSON Web Tokens (JWTs), allowing them to impersonate users, bypass authentication, access sensitive data, and tamper with system integrity, leading to severe security breaches like unauthorized access, data theft, and potential regulatory fines. Compromise usually happens via server misconfigurations (leaking private keys), insecure storage, or vulnerabilities like [JKU Injection](https://www.vaadata.com/blog/jwt-json-web-token-vulnerabilities-common-attacks-and-security-best-practices/#jku).
