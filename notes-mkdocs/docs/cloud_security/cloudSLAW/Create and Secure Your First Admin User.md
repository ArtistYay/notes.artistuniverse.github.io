---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lab

1. Logged into AWS using the root account.

    The root account has unrestricted access to everything in the account, which makes it a big target. Only use it when you have to and always protect it with MFA. We only needed it here for the first setup before switching to a lower-privilege account. AWS actually requires MFA on root users now.

2. Created an IAM group ("Administrators").

    IAM groups let you manage permissions in one place. Attaching policies to a group instead of to each user keeps permissions consistent and a lot easier to manage as more people get added.

3. Created an IAM user and added it to the Administrators group.

    Using an IAM user instead of root means admin actions can be logged, audited, and revoked if needed. Getting permissions through the group keeps things consistent so you don't end up with one-off misconfigurations.

4. Turned on MFA for the IAM user.

    MFA adds another factor on top of the password, so a stolen password alone isn't enough to get in.

!!! note "What AWS recommends now"
    This lab uses an IAM user to get started, but AWS's current guidance is that people (human users) should sign in through federation with IAM Identity Center and get temporary credentials, not long-term IAM users. The later SSO labs switch over to that.

## The Lesson

### Why is IAM Important?

- IAM controls access to every cloud resource. Every request, from a person or a machine, has to go through IAM.
- Since AWS is reachable from the internet, IAM is the first and most important security layer you have.
- The biggest cloud breaches usually come from misconfigured IAM policies, exposed credentials, or way too much access.
- You'll hear "identity is the new perimeter" a lot. In traditional networks, firewalls and VPNs were the perimeter. In the cloud, it's IAM.

### Main Concepts in IAM

1. Entity: a person, device, or system that needs access to AWS.
2. Identity: a unique representation of an entity (like an IAM user, role, or federated identity).
3. Identifier: a way to prove an identity, usually tied to credentials or cryptographic tokens.

AWS IAM is built around identities and policies:

- The root user is tied to an email address and has unrestricted control.
- IAM users live inside an AWS account and have less privilege than root.
- IAM roles and policies define who can access what, and how.

## Bonus

ARNs (Amazon Resource Names) uniquely identify resources across AWS, so a new resource that reuses an old name doesn't accidentally inherit someone's old permissions. Understanding ARNs helps a lot with writing permissions, reading logs, and securing resources.
