# The Lesson

- Resource-Based Policies (bucket polices) are used when you need to control access to resources that can be directly accessed from outside your AWS account (e.g., the public internet). This is a key aspect of securing resources that might otherwise be vulnerable to unauthorized access.
- By adding conditionals like `aws:SourceArn` and `s3:x-amz-acl`, you reduce the risk of unauthorized access or misuse. This practice of adding conditions ensures that only the intended service or user can interact with your resources, effectively preventing malicious actions (e.g., data exfiltration).
- Using the **deny** override behavior effectively prevents unwanted actions from taking place, even if other policies allow them.
# The Lab

1. Customized Given Bucket Policy and Applied it to the Logging Bucket
```
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
            "Resource": "<bucket ARN>/AWSLogs/<Management AccountID>/*",
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

The first statement grants the CloudTrail service permission to retrieve the bucket access control list (ACL) of the specified bucket, but only when the API call originates from the Trail in the management account.

The second statement allows the CloudTrail service to write objects to the S3 bucket under the `/AWSLogs/` path, using the management account's ID, but only if the action enforces `bucket-owner-full-control` and originates from the management account’s Trail.

The final statement permits the CloudTrail service to write objects to the same bucket, but this time under a path associated with the organization ID, ensuring that the log files originate from the primary Trail in the management account.