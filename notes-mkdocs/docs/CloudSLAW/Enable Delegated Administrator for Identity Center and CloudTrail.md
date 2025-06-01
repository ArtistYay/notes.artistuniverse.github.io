# The Lesson

- Delegated administration allows us to assign control of certain AWS services to other accounts, reducing security risks and enforcing least privilege. This approach minimizes the exposure of the management account and distributes administrative responsibilities securely.
		The management account has broad administrative capabilities across all AWS accounts in an organization. Many AWS services require access from the management account to be configured, leading to frequent usage. If compromised, an attacker could gain full control over AWS resources.
# The Lab

1. Delegated IAM Identity Center to the `IAM` account under the `Security` OU.
		Identity Center is a critical service for managing authentication and authorization. Delegating its management ensures that day-to-day administration does not require management account access.
2. Delegated CloudTrail to the `SecurityAudit` account.
