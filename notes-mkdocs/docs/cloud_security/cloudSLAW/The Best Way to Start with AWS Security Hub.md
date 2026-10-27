---
tags:
  - Amazon Web Services
  - Cybersecurity
---

!!! note "Security Hub changed"
    At the end of 2025, AWS launched a new, unified AWS Security Hub that correlates signals from GuardDuty, Inspector, and CSPM checks and adds exposure findings and attack path visualization. The original Security Hub I used in this lab (security standards and controls) is now called AWS Security Hub CSPM. The lessons below still apply, the names just moved around.

## The Lesson

- Security Hub collects findings from almost _every other AWS security service_ in one place and normalizes them into a standard format.
- Security Hub (now Security Hub CSPM) works as a cloud security posture management (CSPM) tool. Think of CSPM as a vulnerability scanner for your cloud configuration. It checks how you have things set up, like your S3 buckets, and flags problems like a public bucket.
- In Security Hub, the sets of rules it checks are called _security standards_.
- CloudTrail tells us most of what's going on in our account (at least the API calls), and GuardDuty uses threat detection to find possibly malicious activity like cryptomining and brute force attacks.
- Inspector looks for vulnerabilities in EC2 instances, container images, and Lambda functions.
- The security standards use AWS Config behind the scenes, and Config can get expensive.

## The Lab

1. Turned on Security Hub in us-east-1.

    Disabled the security standards (they were on by default).

    Delegated Security Hub administration to the SecurityAudit account.

    Turned on Security Hub only for findings aggregation, not the full security scanning.

2. Configured Security Hub in the SecurityAudit account.

    Checked and disabled the security standards again.

    Started central configuration and made sure the home region stayed N. Virginia (us-east-1).

    Picked "Customize my Security Hub configuration" so AWS didn't automatically turn on extra security features.

    Disabled the AWS Foundational Security Best Practices standard to keep costs low.

## Questions I Ask Myself

1. Why do we always have to turn on security services in the management account? In this lab, we signed into the management account, turned on Security Hub, and delegated it to SecurityAudit. Why couldn't we just turn it on in SecurityAudit?

    If you turn a security service on in the SecurityAudit account by itself, it only covers that one account. Turning it on from the management account (and delegating from there) is what sets it up to cover every account in the organization.
