---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lesson

- AWS has a lot of regions to help with regulatory compliance, disaster recovery, and performance.
- Security settings have to be set up per region, and developers might deploy stuff in a region that doesn't have your security controls without realizing it.
- Attackers love under-protected regions for things like cryptomining, since nobody's watching them.
- Every region AWS launched before March 2019 is turned on by default in every account, and you can't turn those off. Newer regions are opt-in. Either way, an SCP is how you actually block the regions you don't use.
- We use double negatives in AWS policies because they let us say "block everything except this." That keeps us safe even when AWS adds new services, actions, or regions.

## The Lab

1. Attached the `RegionLockout` SCP at the root level.

```json
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
            }
        }
    ]
}
```

- The `NotAction` denies everything *except* the actions in that list. Those are global services, and if you block them everything breaks. [Documentation | AWS](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_examples_general.html?utm_source=slaw.securosis.com&utm_medium=referral&utm_campaign=notwhat-lock-out-regions-with-a-double-negative-scp). _But why?_ Instead of denying thousands of actions one by one, we list the small set of actions to let through.

- The condition means: if an API call is NOT going to one of these two regions, block it.

- Before deploying this SCP, check which regions you actually use with the Billing console and IAM Access Advisor. Test it on a test OU before rolling it out everywhere.
