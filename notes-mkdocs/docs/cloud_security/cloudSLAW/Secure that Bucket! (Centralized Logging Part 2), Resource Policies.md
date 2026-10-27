---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lesson

- Resource-based policies (like bucket policies) are attached to the resource itself instead of to an identity. You need them when something outside your account (another account, an AWS service, or even the public internet) has to reach the resource, so getting them right is a big deal.
- Adding conditions like `aws:SourceArn` and `s3:x-amz-acl` makes sure only the service or user you intended can touch your resource. That helps stop things like data exfiltration or another account's trail writing into your bucket.
- A deny always overrides an allow, so you can use deny statements to block actions even if some other policy allows them.

## The Lab

1. Customized the given bucket policy and applied it to the logging bucket.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AWSCloudTrailAclCheck20150319",
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "cloudtrail.amazonaws.com"
                ]
            },
            "Action": "s3:GetBucketAcl",
            "Resource": "<Bucket ARN>",
            "Condition": {
                "StringEquals": {
                    "aws:SourceArn": "<Trail ARN>"
                }
            }
        },
        {
            "Sid": "AWSCloudTrailWrite20150319",
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "cloudtrail.amazonaws.com"
                ]
            },
            "Action": "s3:PutObject",
            "Resource": "<Bucket ARN>/AWSLogs/<Management AccountID>/*",
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-acl": "bucket-owner-full-control",
                    "aws:SourceArn": "<Trail ARN>"
                }
            }
        },
        {
            "Sid": "AWSCloudTrailOrganizationWrite20150319",
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "cloudtrail.amazonaws.com"
                ]
            },
            "Action": "s3:PutObject",
            "Resource": "<Bucket ARN>/AWSLogs/<organizationID>/*",
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-acl": "bucket-owner-full-control",
                    "aws:SourceArn": "<Trail ARN>"
                }
            }
        }
    ]
}
```

The first statement lets the CloudTrail service read the bucket's access control list (ACL), but only when the request comes from the trail in the management account.

The second statement lets CloudTrail write objects into the bucket under the `/AWSLogs/<Management AccountID>/` path, but only if the write sets `bucket-owner-full-control` and comes from the management account's trail.

The last statement lets CloudTrail write into the same bucket, but under the organization ID path, which is where the org trail puts logs for every account.
