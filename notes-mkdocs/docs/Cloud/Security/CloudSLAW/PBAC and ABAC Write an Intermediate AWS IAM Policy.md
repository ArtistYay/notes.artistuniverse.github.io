# The Lesson

- _Access controls map to objects (like files or systems), authorizations map to actions (like AWS API calls), and entitlements are when you assign either to an identity._
- Role-Based Access Control (RBAC): Assigns roles to identities, which define permissions.
- Attribute-Based Access Control (ABAC): Uses attributes like tags and IP addresses to control access.
- Policy-Based Access Control (PBAC): Encodes both RBAC and ABAC rules within policies.

![[Pasted image 20250322183348.png]]

- **Statements**: Define permissions (Effect: allow/deny actions).
- **Actions**: Specific API operations permitted or denied.
- **Resources**: AWS resources the policy applies to.
- **Conditions**: Additional rules based on attributes.
- Conditionals in IAM policies have two main components:
		1. Condition Keys apply across anything (e.g., aws:SourceIp) or apply to particular services (e.g., `s3:ResourceTag`).
			a. https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html?utm_source=slaw.securosis.com&utm_medium=referral&utm_campaign=pbac-and-abac-write-an-intermediate-aws-iam-policy
		2. Condition operators are logical conditions like StringEquals, IpAddress, Booleans.
			a. https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition_operators.html?utm_source=slaw.securosis.com&utm_medium=referral&utm_campaign=pbac-and-abac-write-an-intermediate-aws-iam-policy
# The Lab

1. Wrote and deleted an IAM policy were you can stop or start an instance based on the IP address that's making the API call.