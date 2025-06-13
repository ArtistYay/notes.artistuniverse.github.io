# The Lab

1. Made a customer managed policy 
		The policy is to let the IAM admins create, list, get, update, and delete IAM policies.
## Errors

I got an `404 status error: Not supported policy` message when I tried to attach the `ManagePoliciesForIdentityCenter` policy for the IAM permission set. I Googled and got to this solution [https://repost.aws/questions/QUGSZ_CZ1BT_KTiD7bIrdXFA/404-status-error-not-supported-policy-but-duplicated-policy-works](https://repost.aws/questions/QUGSZ_CZ1BT_KTiD7bIrdXFA/404-status-error-not-supported-policy-but-duplicated-policy-works) it seemed I had to create the same policy in the IAM account for the policy to be able to attach to the permission set.

I see why I got the error...I was creating and adding the permission set in my management account instead of my IAM account with the admin access role...