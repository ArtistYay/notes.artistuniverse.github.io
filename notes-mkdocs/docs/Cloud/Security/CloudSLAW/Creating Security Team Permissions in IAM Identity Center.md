# The Lesson

- To avoid using full administrative privileges at all times, assigning different permission sets (read-only, full admin, and IAM administration) in IAM Identity Center can minimize the impact of accidental or malicious actions by limiting permissions based on tasks.
# The Lab

1. Assigned the `AdminstratorAccess` permission set to the Admin group for accounts `IAM, SecurityAudit, SecurityOperations, and TestAccount1`
		Having this available to incident responders in case they need to “break glass” and jump into an account under active attack.
2. Created more groups `SecurityAdministrators, IAM Administrators`
3. Created permissions sets `ReadOnly and IdentityCenterAdministrator` 
		`IdentityCenterAdministrator` has the AWS managed policy of `AWSSSOMemberAccountAdministrator`