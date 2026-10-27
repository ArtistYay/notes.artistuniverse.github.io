---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lesson

- IAM Identity Center lets you manage user access centrally, so you don't have to create separate IAM users in every AWS account.
- Federation lets one identity source (like Microsoft Entra ID or Okta) manage access across a bunch of AWS accounts and services.
- Identity Provider (IdP): where you log in. The IdP is home to the _user pool_ or _directory_ where you set up user accounts, groups, etc. We sometimes call it the _authoritative source_ because it's the final word on who you are and what groups and roles you have.
- Relying Party: where you do things. The relying party... relies... on the IdP for authentication, so it can focus on authorization.
- Users get created in the IdP and assigned _attributes_ like group, role, and email address.
- Admins set up a _trust relationship_ between the IdP and the relying party. This is usually an exchange of metadata that defines the relationship, the signing certificate(s), and the URLs they use to talk to each other.

![screenshot](../../../images/Pasted image 20250309195059.png)

- A user logs into the IdP. When they go to log into a relying party, they provide the IdP's address or some other identifier so the relying party knows where to send them (this is usually hidden from the user).
- The IdP then makes an _assertion_: a digitally signed statement that the user is who they say they are, plus whatever _attributes_ it sends over (like a group, or whether they used MFA).
- The user gets a token that represents the session. That token has a Time To Live (TTL) before it expires. The user just shows the token to the relying party, and the relying party decides what they're allowed to do.
- When the token expires, the user has to log in again or get a refreshed token with a new TTL.

## The Lab

1. Deployed AWS IAM Identity Center (it used to be called AWS SSO).
2. Turned on MFA for every sign-in under settings.
3. Created a user and an Administrator group, and added the user to the group.
