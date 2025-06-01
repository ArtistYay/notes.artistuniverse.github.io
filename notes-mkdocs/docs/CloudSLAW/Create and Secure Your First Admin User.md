# The Lab

1. Logged into AWS using the root account.
		The root account has unrestricted access to the AWS environment, making it a high-risk target. Best practices dictate using it sparingly and securing it with MFA. This step is necessary only for initial setup before transitioning to a lower-privilege account.
2. Created an IAM Group ("Administrators")
		IAM groups enable centralized permission management, reducing the risk of excessive privilege allocation. Attaching policies at the group level instead of directly to users follows the principle of least privilege (PoLP) and makes permission management scalable.
3. Created a IAM user and assigned it to the Administrators group
		IAM users allow better access control compared to using the root account. This ensures that administrative actions can be logged, audited, and revoked if necessary. Using a group-based policy enforces consistency and prevents misconfigurations.
4. Enabled Multi-Factor Authentication (MFA) for the IAM User
		MFA significantly strengthens authentication security by requiring an additional verification factor beyond just a password. This mitigates the risk of credential theft and unauthorized access.

# The Lesson

## Why is IAM Important?

- IAM **controls access** to all cloud resources. Every request, whether from a human or a machine, must pass through IAM.
- Since **AWS is accessible via the internet**, IAM is the first and most important security layer in protecting cloud environments.
- The **biggest cloud security breaches** often originate from **misconfigured IAM policies, exposed credentials, or overly permissive access**.
- A common security mantra is **"Identity is the new perimeter."** Unlike traditional networks, where firewalls and VPNs defined the perimeter, cloud security is now centered around IAM.
### Key Concepts in IAM

1. **Entity:** A person, device, or system that needs access to AWS.
2. **Identity:** A unique representation of an entity (e.g., an IAM user, role, or federated identity).
3. **Identifier:** A way to prove an identity, usually tied to cryptographic tokens or credentials.

AWS IAM structures permissions around **identities** and **policies**:

- The **root user** is tied to an **email address** and has unrestricted control.
- **IAM users** exist within an AWS account but are less privileged than the root user.
- **IAM roles and policies** define **who** can access **what** and **how**.

## Bonus

ARMs uniquely identify resources across AWS, preventing accidental privilege inheritance due to name reuse. Recognizing the significance of ARNs helps in managing permissions, logging, and securing resources.