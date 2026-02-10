# The Lesson

- Permissions are granted using something called a _Permission Set_. A permission set is a collection of up to 10 IAM policies.
- To provide access to an account, you assign a user/group a permission set and accounts. It’s a 3 part equation: group + permission set + account = what you can do.
- Users and groups can be assigned multiple permission sets per account.
- When you assign a permission set, that creates an IAM role in the account with the IAM policies you defined. It then sets the role trust policy to allow the identity provider (IAM Identity Center) to assume the role.

![screenshot](../../../images/another_me_p2.png)
# The Lab

1. Created an AdminstratorAccess permission set.
		**Relay state,** is just a fancy way of saying “when the user logs in with this permission set, put them into this part of the console”.
2. Assigned the Group to have AdminstratorAccess to the SecurityAudit and management account.
		Must select the accounts then click on 'assign users and groups'
3.  Reviewed the 'AWSReservedSSO_AdministratorAccess' role
![[Pasted image 20250309200237.png]]
4. This is the ARN of the _Identity provider_ which Identity Center/Organizations created in the account. You can see it if you look under **Identity providers**. An AWS Organization can have more than one of these.
5. This gives the role permission to use the [**AssumeRolewithSAML**](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithSAML.html) API call, which is a bit different than **AssumeRole** but very similar.
6. This lets the IdP tag the session when you assume the role. This is very valuable for tracking, because it adds a session name which aligns with the user assuming the role.
7. The last is a condition that **only** allows this when using the signing portal, and **only** the AWS one. You can’t assume this role from any other origin.