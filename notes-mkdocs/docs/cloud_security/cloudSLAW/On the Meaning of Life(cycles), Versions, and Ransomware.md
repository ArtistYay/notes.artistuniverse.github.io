# The Lesson

- Keeping all logs indefinitely can create large bills, even if the cost starts small.
- Security logs should be managed efficiently.  Retention should balance compliance needs with storage costs.
- A lifecycle policy helps determine what to retain and what to discard.
- S3 versioning is a data protection mechanism, keeps previous versions of objects, making it harder for attackers to delete data permanently. Attackers delete or modify logs to cover their tracks.
- You can block delete operations on critical logs via IAM or SCP.
- Why isn’t versioning used in this lab? versioning increases storage costs. In a real-world ransomware protection strategy, versioning + SCPs are highly recommended.
- AWS Glacier is also used for immutable storage but Glacier retrieval is slow and may not fit operational needs. Quick access is needed for investigations; waiting 12+ hours for Glacier retrieval may not be practical.
# The Lab 

1. Signed into the `LogArchive` with the `AdminstratorAccess` role via SSO and turned on S3 Lifecycle policy for the CloudTrail bucket for 90 days
		90-day retention ensures logs are available for incident response and auditing.