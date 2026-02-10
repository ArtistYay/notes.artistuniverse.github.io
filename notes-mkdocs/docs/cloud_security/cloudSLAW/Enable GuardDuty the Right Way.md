# The Lesson

- GuardDuty acts as an IDS (Intrusion Detection System) for AWS, analyzing multiple telemetry sources to identify potential threats.
- GuardDuty charges based on activity, making it affordable to enable across all regions, even unused ones.
- GuardDuty monitors CloudTrail, VPC Flow Logs, and DNS Logs automatically.
- Many security frameworks require continuous threat monitoring, and GuardDuty provides an AWS-native way to meet those requirements.
# The Lab

1. Enable GuardDuty in a Primary Region (us-east-1).
		GuardDuty is a regional service and must be activated separately in each required region.
2. Repeat for a Secondary Region (us-west-2).
		Security best practices recommend enabling GuardDuty in multiple regions, even if they are not actively used. GuardDuty costs nothing in inactive regions unless activity is detected (SCP blocks resources from being deployed).
		We also delegated administration to the `SecurityAudit` account.
3. Auto-Enable GuardDuty for All Future Accounts.
		This ensures that any newly created AWS accounts within the organization automatically have GuardDuty enabled. Auto-enable only applies to _new_ accounts, not existing ones.