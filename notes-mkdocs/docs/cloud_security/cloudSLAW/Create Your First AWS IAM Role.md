---
tags:
  - Amazon Web Services
---

# The Lesson

- IAM roles are central to managing permissions for services and users in AWS. Using roles rather than users for permissions enhances security by using temporary credentials.
- **Persona**, the expression of an identity, with attributes that indicate context, is a role a user can assume for a temporary set of permissions used for a session.

![screenshot](../../../images/Pasted image 20250309104408.png)
![screenshot](../../../images/Pasted image 20250309104421.png)

# The Lab

1. Created a new IAM Role for EC2 instances to assume to interact with SSM.
		Trusted Entity is who are allowed to assume the role.
		Permissions policies define what a role can do. In this case, it ensures the EC2 instance can execute SSM commands for system management, while limiting other actions. This follows the principle of least privilege.
		Use Case: using IAM roles to manage EC2 instances interacting with AWS Systems Manager minimizes the need for SSH keys or long-lived API credentials, which can be vulnerable if leaked or misused.