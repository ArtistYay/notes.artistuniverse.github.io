# The Lesson

- IAM Identity Center allows organizations to manage user access **centrally**, reducing the need to create individual IAM users in each AWS account. 
- Federation enables a **single identity source** (e.g., Microsoft Entra ID, Okta) to manage access across multiple AWS accounts and services.
- **Identity Provider (IdP):** This is where you log in. The identity provider is the home of the _user pool_ or _directory_ where you set up user accounts, groups, etc. We sometimes call this the _authoritative source_ because it’s the ultimate decider of who you are and your groups & roles.
- **Relying Party:** This is where you do things. The relying party… relies… on the IdP for authentication, so it can focus on authorization.
- Users are created in the Identity Provider and assigned _attributes_ such as group, role, and email address.
- Administrators create a _trust relationship_ between the identity provider and the relying party. This is usually an exchange of metadata to define the relationship and cryptographic signing certificate(s), and includes the URLs for communications.
![[Pasted image 20250309195059.png]]

- A user logs into the IdP. When they go to log into a relying party, they provide the address of the IdP or some other identifier so the relying party knows who they are (this is usually hidden from the user).
- The IdP then makes an _assertion_: a digitally signed statement that the user is who they say they are, including whatever _attributes_ they send over (like a group or whether they used MFA).
- The user is issued a digital token which represents the session. That token has a Time To Live (TTL) before expiration. The user only needs to present the token to the relying party, which then decides what the user is allowed to do.
- When the token expires, the user needs to log in again, or ask for a refreshed token with a new TTL.
# The Lab

1. Deployed the AWS IAM Identity Center (SSO)
2. Enforced MFA on every sign on under settings
3. Created a user and Administrator group and added the user in that group