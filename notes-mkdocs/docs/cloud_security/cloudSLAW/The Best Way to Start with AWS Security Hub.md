# The Lesson

 - Security Hub collects events and results from nearly _any other AWS security service,_ all in one place. Normalizes findings from those services into a standard format.
 - Security Hub can work as a Cloud Security Posture Management (CSPM) tool. Think of CSPM as a vulnerability scanner for your cloud. These tools assess how you have things configured, such as your S3 buckets, and identify problems like public S3 buckets.
 - In Security Hub the rules to check are called _Security Standards._
 - **CloudTrail** tells us most of what’s going on in our account (at least in terms of API calls), and **GuardDuty** uses threat detection capabilities to identify potential malicious activity, like cryptocurrency mining and brute force attacks.
 - Can use **Inspector** to look for vulnerabilities in virtual machines and containers.
 - The _Security Standards_ uses AWS **Config** on the back end which is expensive.
# The Lab

1. Enabled Security Hub in us-east-1
		**Disabled Security Standards** (which were enabled by default).
		**Delegated administration** of Security Hub to the **SecurityAudit account**.
		Enabled Security Hub **only for findings aggregation**, not full security scanning.
2. Configured Security Hub in the SecurityAudit Account
		Checked and **disabled Security Standards again**
		**Started Central Configuration**. Ensured the **Home Region remained Virginia**.
		Selected **"Customize my Security Hub configuration"** to prevent AWS from automatically enabling additional security features.
		**Disabled AWS Foundational Best Practices security standard** to keep costs low.
# Question
1. Why do we always have to enable security solutions in the management account. For example, in this lab, we SSO into our management account, enabled Security Hub, and delegated it to our SecurityAudit account. Why couldn't we just turn it on in our SecurityAudit account?
		If you enable a security service in the SecurityAudit account, it only protects that single account. By enabling it in the management account (or delegating from there), you set it up to protect all accounts in the organization. 