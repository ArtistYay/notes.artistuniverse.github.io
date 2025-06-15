# The Lab

1. Assumed the `OrganizationAccountAccessRole` 
		Have to input the account ID # of the account you wish to sign into with the role (SecurityAudit) and the role name (OrganizationAccountAccessRole)
2.  Deployed an S3 bucket in the SecurityAudit account for centralized logging.
		Centralizing logs is a crucial part of any cloud security strategy. By keeping logs in a centralized location, security teams can more easily perform investigations and monitor for suspicious activities across all accounts.
# The Lesson

- _AWS does not allow you to assume roles from your root user account — you need to use an IAM user or another role._
- AWS provides AWS Security Token Service (AWS STS) as a web service that enables you to request temporary, limited-privilege credentials for users.

![screenshot](../../../images/20250309124139.png)