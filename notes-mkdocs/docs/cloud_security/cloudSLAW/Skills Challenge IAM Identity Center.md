---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lab

1. Made a customer managed policy.

    The policy lets the IAM admins create, list, get, update, and delete IAM policies.

## Errors

I got a `404 status error: Not supported policy` message when I tried to attach the `ManagePoliciesForIdentityCenter` policy to the IAM permission set. I Googled it and found this [solution](https://repost.aws/questions/QUGSZ_CZ1BT_KTiD7bIrdXFA/404-status-error-not-supported-policy-but-duplicated-policy-works). It looked like I had to create the same policy in the IAM account before it could attach to the permission set.

Then I saw why I got the error... I was creating and adding the permission set in my management account instead of my IAM account with the admin access role. Customer managed policies in a permission set have to exist (with the same name) in every account you assign the permission set to.
