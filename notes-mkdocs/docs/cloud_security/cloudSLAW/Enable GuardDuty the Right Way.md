---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lesson

- GuardDuty is basically an IDS (intrusion detection system) for AWS. It looks at a bunch of telemetry sources to find possible threats.
- GuardDuty charges based on how much data it analyzes, so it's cheap to turn on in every region, even ones you don't use.
- Out of the box it watches CloudTrail management events, VPC Flow Logs, and DNS query logs. You don't have to turn those logs on yourself. There are also extra protection plans (S3, EKS, Runtime Monitoring, Malware Protection, RDS, Lambda) you can add.
- A lot of security frameworks require continuous threat monitoring, and GuardDuty is the AWS-native way to check that box.

## The Lab

1. Turned on GuardDuty in the primary region (us-east-1).

    GuardDuty is a regional service, so you have to turn it on separately in every region you care about.

2. Did the same in the secondary region (us-west-2).

    Best practice is to turn GuardDuty on in every region, even ones you don't use. It costs almost nothing in a region with no activity (and our SCP blocks people from deploying there anyway).

    We also delegated GuardDuty administration to the `SecurityAudit` account.

3. Set GuardDuty to auto-enable for accounts in the organization.

    In the delegated admin account you choose `New` (only accounts that join from now on), `All` (every account, including the ones already in the org), or `None`. If you pick `New`, you still have to add your existing accounts as members yourself.
