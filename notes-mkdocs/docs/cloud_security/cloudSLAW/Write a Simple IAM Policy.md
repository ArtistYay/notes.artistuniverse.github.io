# The Lesson

- The ARN uniquely identifies AWS resources, allowing precise specification in IAM policies. In cloud security, knowing the exact resource is vital to restrict or grant access properly. Properly defining the resource scope ensures that access is given only to specific entities (like logs in this case), preventing unnecessary exposure to other resources.
- **Inline** **policies** attach directly to the user/group/role and only work for the thing they are attached to. You write them for that user and cannot reuse them anyplace else.
- **Managed policies** are central policies you write once and can attach wherever you want. If you update a managed policy, that change applies instantly to everything using it. There are two types of managed policies:
    - **AWS managed policies** are standard ones AWS writes and maintains, which customers can use.
    - **Customer managed policies** are ones you write yourself, which only exist in your AWS Account.

![screenshot](../../../images/Pasted image 20250309110124.png)

# The Lab

1. Created a Custom Policy for read (s3:GetObject) and write (s3:PutObject) to our CloudTrail bucket
		IAM policies define what actions users, roles, and services can perform. Writing policies allows for granular control. The Visual Policy Editor simplifies policy creation by providing an easy-to-understand interface.

```
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
 - **Version:** This defines the policy language version. "2012-10-17" is the current version; this is required.
- **Statement:** This is the main element of the policy. It’s an array of multiple policy statements. (Anything in [] is an array). Each statement must have an effect, action, and resource.
- **Effect:** Whether the statement results in an allow or a deny.
- **Action:** Lists the specific actions (API calls) allowed or denied. In this policy:
    - "s3:GetObject": Grants permission to retrieve objects from the specified bucket.
    - "s3:PutObject": Allows the user to upload or modify objects in the bucket.
- **Resource:** Specifies the resources the statement covers.
    - Here, "arn:aws:s3:::rmogull-slaw/<asterisk>" means the policy applies to all objects (/*) in the rmogull-slaw bucket.
    - An ARN (Amazon Resource Name) uniquely identifies AWS resources. In this case it specifies my S3 bucket.