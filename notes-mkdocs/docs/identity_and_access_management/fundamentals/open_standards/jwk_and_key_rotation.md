### JWK

JSON Web Keys are a set of public keys used to digitally sign JSON Web Tokens (JWTs) that have been dispatched from the Identity Provider (IdP).

It is used in tandem with the RS256 signing algorithm. In technical terms "A JSON object that represents a cryptographic key. The members of the object represent properties of the key, including its value."

### Key Rotation

Making sure a JWK is rotated often minimize the impact of potential key compromise. If a key has been compromised an attacker can forge valid JSON Web Tokens (JWTs), allowing them to impersonate users, bypass authentication, access sensitive data, and tamper with system integrity, leading to severe security breaches like unauthorized access, data theft, and potential regulatory fines. Compromise usually happens via server misconfigurations (leaking private keys), insecure storage, or vulnerabilities like [JKU Injection](https://www.vaadata.com/blog/jwt-json-web-token-vulnerabilities-common-attacks-and-security-best-practices/#jku).