---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lesson

- _Access controls map to objects (like files or systems), authorizations map to actions (like AWS API calls), and entitlements are when you assign either one to an identity._
- Role-Based Access Control (RBAC): assigns roles to identities, and the roles define the permissions.
- Attribute-Based Access Control (ABAC): uses attributes like tags and IP addresses to decide access.
- Policy-Based Access Control (PBAC): writes both RBAC and ABAC rules into policies.

![screenshot](../../../images/Pasted image 20250322183348.png)

- Statements: define the permissions (Effect: allow or deny the actions).
- Actions: the specific API operations being allowed or denied.
- Resources: the AWS resources the policy applies to.
- Conditions: extra rules based on attributes.
- Conditions in IAM policies have two main parts:
    1. Condition keys, which either apply to everything (like `aws:SourceIp`) or to a specific service (like `s3:ResourceTag`). [Documentation | AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html?utm_source=slaw.securosis.com&utm_medium=referral&utm_campaign=pbac-and-abac-write-an-intermediate-aws-iam-policy)
    2. Condition operators, which are the logic like `StringEquals`, `IpAddress`, and `Bool`. [Documentation | AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition_operators.html?utm_source=slaw.securosis.com&utm_medium=referral&utm_campaign=pbac-and-abac-write-an-intermediate-aws-iam-policy)

## The Lab

1. Wrote (and then deleted) an IAM policy that lets you stop or start an instance only when the API call comes from a certain IP address.
