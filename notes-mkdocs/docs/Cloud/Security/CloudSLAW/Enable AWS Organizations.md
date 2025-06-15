# The Lab

1. Enabled AWS Organizations
		Enabling AWS Organizations allows you to manage multiple AWS accounts centrally, which is a best practice for large-scale environments. It provides a clear path for managing resources across different business units, regions, or security domains.
2. Created an OU (Organizational Units) named 'Security' and moved the 'LogArchive' account under it.
		Organizational Units (OUs) are containers for AWS accounts, allowing you to group accounts logically based on business requirements or security needs.
		Using OUs enhances security by allowing you to apply **Service Control Policies (SCPs)**, which govern the permissions and actions allowed within each OU.

![screenshot](../../../images/20250309111741.png)

# The Lesson

- **OrganizationAccountAccessRole** allows the management account to access the new account as an administrator. This role is automatically created when you add an account to AWS Organizations and is crucial for administering accounts without having to manage separate IAM users or credentials in each account. In other words allow anything or anyone from management account to use this role
 - **Service Control Policies (SCPs)** provide critical security benefits by enforcing restrictions on what actions are allowed in each account, protecting sensitive resources.
- The account you turn AWS Organizations will be your management account, DO NOT DEPLOY WORKLOADS IN THAT ACCOUNT.
- _Consolidated Billing_ accounts roll up their charges to the management account but are still otherwise independent.