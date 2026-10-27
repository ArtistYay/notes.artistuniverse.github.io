---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lesson

- IAM roles are how you manage permissions for services and users in AWS. Roles are more secure than users because they use temporary credentials.
- A persona is how an identity shows up in a certain context. It's basically a role a user can assume to get a temporary set of permissions for a session.

![screenshot](../../../images/Pasted image 20250309104408.png)
![screenshot](../../../images/Pasted image 20250309104421.png)

## The Lab

1. Created a new IAM role for EC2 instances to assume so they can talk to SSM (Systems Manager).

    The trusted entity is who's allowed to assume the role.

    The permissions policies define what the role can do. Here it lets the EC2 instance run SSM commands for system management and not much else, which is least privilege.

    Why it matters: using an IAM role for EC2 to work with Systems Manager means you don't need SSH keys or long-lived API credentials, which are dangerous if they get leaked.
