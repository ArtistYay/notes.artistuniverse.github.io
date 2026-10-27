---
tags:
  - Cybersecurity
  - Identity & Access Management
---

LDAP (Lightweight Directory Access Protocol) is the protocol apps use to look up data in a directory. When you search for a coworker in Outlook, or an app needs to check which group you're in, it speaks LDAP. You can authenticate with LDAP (called an "LDAP bind"), but its main superpower is querying the database. Plain LDAP on port 389 isn't encrypted, so use LDAPS (port 636) or LDAP signing so credentials don't fly across the network in the clear.

Active Directory is the database; LDAP is the language used to read that database.

[Forum Post | Reddit](https://www.reddit.com/r/devops/comments/e89spr/what_is_ldap_and_why_i_should_use_it_in_my_auth/)
