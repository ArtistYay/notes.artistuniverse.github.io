# The Lab

1. Enable Service Control Policies (SCPs)
		This creates an allow all SCP called `FullAWSAccess` to all OUs and accounts. Allows full access to all AWS services and resources within an account, effectively providing unrestricted permissions.
		Even though the `FullAWSAccess` Service Control Policy (SCP) exists, users still need to be granted **IAM permissions** in order to actually use the services and perform actions within those services.
2. Made a Custom SCP to Protect Root Account and Prevent Leaving AWS Organization
		`ProtectRootAndOrg` applied a `Deny` effect to the `organizations:LeaveOrganization` action and restricted root user actions.
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "organizations:LeaveOrganization"
      ],
      "Resource": "*",
      "Effect": "Deny"
    },
    {
      "Action": "*",
      "Resource": "*",
      "Effect": "Deny",
      "Condition": {
        "StringLike": {
          "aws:PrincipalArn": [
            "arn:aws:iam::*:root"
          ]
        }
      }
    }
  ]
```

3. Applied the SCP to the 'Root' level
		Prevented any account from being able to remove itself from the organization or use the root account inappropriately.
# The Lesson

- SCPs set the boundaries for what actions can be performed in an account. They act as a filter for IAM policies, restricting access at the organizational level. However, SCPs do not directly grant permissions to perform actions; they only allow or deny the actions defined in the IAM policies that are attached to users or roles.
- In AWS, an **explicit deny** always takes precedence over an **allow**, even if the SCP would otherwise allow the actions.