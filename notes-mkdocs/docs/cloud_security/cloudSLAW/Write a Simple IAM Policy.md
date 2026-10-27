---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lesson

- The ARN uniquely identifies an AWS resource, so you can point at exactly the right thing in an IAM policy. Getting the resource scope right means access only goes to what it should (like just the logs in this case) and nothing else gets exposed.
- Inline policies attach directly to a user, group, or role and only work for the thing they're attached to. You write them for that one identity and can't reuse them anywhere else.
- Managed policies are central policies you write once and attach wherever you want. If you update a managed policy, the change applies right away to everything using it. There are two kinds:
    - AWS managed policies are the standard ones AWS writes and maintains for customers to use.
    - Customer managed policies are ones you write yourself, and they only exist in your AWS account.

![screenshot](../../../images/Pasted image 20250309110124.png)

## The Lab

1. Created a custom policy for read (`s3:GetObject`) and write (`s3:PutObject`) on our CloudTrail bucket.

    IAM policies define what actions users, roles, and services can do, and writing your own gives you granular control. The visual policy editor makes it easier to build one if you're not comfortable with JSON yet.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::rmogull-slaw/*"
        }
    ]
}
```

- Version: the policy language version. `"2012-10-17"` is the current one and you should always include it.

- Statement: the main part of the policy. It's an array of statements (anything in [] is an array). Each statement needs an effect, an action, and a resource.

- Effect: whether the statement allows or denies.

- Action: the specific actions (API calls) being allowed or denied. In this policy:
    - `"s3:GetObject"`: lets you download objects from the bucket.
    - `"s3:PutObject"`: lets you upload or overwrite objects in the bucket.

- Resource: what the statement applies to.
    - Here, `"arn:aws:s3:::rmogull-slaw/*"` means the policy applies to all objects (`/*`) in the rmogull-slaw bucket.
    - An ARN (Amazon Resource Name) uniquely identifies an AWS resource. In this case it's my S3 bucket.
