---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lesson

- CloudTrail is a central record of almost every admin action (API call) in an AWS account.
- Turn on multi-region trails so you're logging everywhere, not just one region.
- Store the logs in a private, encrypted S3 bucket. CloudTrail encrypts logs with SSE-S3 by default, and you can use your own KMS key (SSE-KMS) for more control over who can decrypt them.
- In this lab we skipped the custom KMS key to keep it simple, since it's one more thing to manage. In a real environment, SSE-KMS is worth it for your security logs.
- Make sure log file validation is on. It uses hashing and digital signatures so you can prove the logs weren't changed or deleted, which matters for forensics.
- Management events: admin actions (like IAM changes or EC2 changes).
- Data events: access to the resources themselves (like S3 object reads/writes). These cost extra.
- Insights events: flags unusual API activity. These cost extra too.
