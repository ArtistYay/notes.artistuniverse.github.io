1. Organized and Created OUs 
	- **Infrastructure** (Shared services and network resources)
	- **Workloads** (Application environments)
	- **Exceptions** (Temporary policy exemptions)
	- **Sandbox** (Developer experimentation)
    - **Onboarding** (Mergers/acquisitions)
    - **Nursery** (New accounts before deployment)
    - **Suspended** (Accounts marked for deprovisioning)
    - **IncidentResponse** (Accounts for active security incidents)
	https://github.com/primeharbor/org-kickstart/blob/main/ous.tf?utm_source=slaw.securosis.com&utm_medium=referral&utm_campaign=aws-lego-organizing-the-org
	#### **Applying the 5 Whys:**
	1. **Why separate OUs?** To organize accounts based on security and operational needs.
	2. **Why does organization matter?** It helps enforce access control and security policies effectively.
	3. **Why enforce strict access control?** To limit the blast radius of potential security breaches.
	4. **Why minimize the blast radius?** To reduce impact from compromised accounts or misconfigurations.
	5. **Why mitigate misconfigurations?** Misconfigurations are a leading cause of cloud security incidents.
2. Created two new AWS Accounts and moved them to the Security OU
	- **IAM** (Dedicated for Identity and Access Management operations)
	- **SecurityOperations** (Houses security tools with modification capabilities)
		Why?
		- IAM account separation prevents privilege escalation risks by isolating identity management.
		- The Security Operations account ensures security tools have a controlled environment.
    