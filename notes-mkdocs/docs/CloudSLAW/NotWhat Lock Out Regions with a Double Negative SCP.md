# The Lesson

- AWS provides multiple regions to enhance regulatory compliance, disaster recovery, and performance.
- Security configurations must be applied per region and developers might unknowingly deploy resources in less secured regions.
- Attackers exploit under-protected regions to launch attacks such as crypto mining.
- AWS also enables new regions automatically without corresponding security controls.
- We use double negatives in AWS policies because they enable us to say “block everything except this”. This keeps us secure when new services, permissions (e.g., IAM user policies), actions, or regions are added.
# The Lab

1. Attaching the `RegionLockout` SCP to the root level
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DenyAllOutsideRegions",
            "Effect": "Deny",
	        "NotAction": [
	        "a4b:*",
	        "acm:*",
	        "aws-marketplace-management:*",
	        "aws-marketplace:*",
	        "aws-portal:*",
	        "budgets:*",
	        "ce:*",
	        "chime:*",
	        "cloudfront:*",
	        "config:*",
	        "cur:*",
	        "directconnect:*",
	        "ec2:DescribeRegions",
	        "ec2:DescribeTransitGateways",
	        "ec2:DescribeVpnGateways",
	        "fms:*",
	        "globalaccelerator:*",
	        "health:*",
	        "iam:*",
	        "importexport:*",
	        "kms:*",
	        "mobileanalytics:*",
	        "networkmanager:*",
	        "organizations:*",
	        "pricing:*",
	        "route53:*",
	        "route53domains:*",
	        "route53-recovery-cluster:*",
	        "route53-recovery-control-config:*",
	        "route53-recovery-readiness:*",
	        "s3:GetAccountPublic*",
	        "s3:ListAllMyBuckets",
	        "s3:ListMultiRegionAccessPoints",
	        "s3:PutAccountPublic*",
	        "shield:*",
	        "sts:*",
	        "support:*",
	        "trustedadvisor:*",
	        "waf-regional:*",
	        "waf:*",
	        "wafv2:*",
	        "wellarchitected:*"
      ],
      "Resource": "*",
 "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": [
            "us-east-1",
            "us-west-2"
          ]
        }
```

- The `NotAction` denies everything except these actions in the list, these actions are Global services and if it's blocked then everything breaks. https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_examples_general.html?utm_source=slaw.securosis.com&utm_medium=referral&utm_campaign=notwhat-lock-out-regions-with-a-double-negative-scp. Why? Instead of explicitly denying thousands of actions, we specify a small list of actions to allow.
- Condition translate to if an API call does NOT come from these two regions, then a block kicks in.
- Before deploying the SCP, audit active regions using AWS Billing Console & Access Advisor. Apply the SCP to a test OU before deploying widely.