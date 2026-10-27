---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lesson

- Keeping every log forever can turn into a big bill, even if it starts small.
- Security logs should be managed on purpose. Retention should balance what compliance needs with what storage costs.
- A lifecycle policy decides what to keep, what to move to cheaper storage, and what to delete.
- S3 versioning keeps previous versions of objects, which makes it a lot harder for an attacker to permanently delete data. Attackers delete or change logs to cover their tracks.
- You can block delete operations on critical logs with IAM policies or an SCP.
- Why didn't we use versioning in this lab? It increases storage costs. For real ransomware protection though, versioning + SCPs are highly recommended. S3 Object Lock is the feature that actually makes objects immutable (write once, read many).
- S3 Glacier storage classes are cheap for long-term storage, but some of them are slow to get data back from. Glacier Flexible Retrieval can take minutes to hours, and Glacier Deep Archive can take 12 hours or more. During an investigation you need logs fast, so that wait might not work. (Glacier Instant Retrieval is the exception, it's milliseconds.)

## The Lab

1. Signed into `LogArchive` with the `AdministratorAccess` role through SSO and turned on an S3 lifecycle policy for the CloudTrail bucket for 90 days.

    90 days of retention keeps logs around for incident response and audits.
