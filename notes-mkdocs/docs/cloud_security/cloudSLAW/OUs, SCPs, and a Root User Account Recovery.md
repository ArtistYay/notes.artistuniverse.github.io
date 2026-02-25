# The Lesson

1. Why move the SCP off the root?
    - To create an Exceptions OU that temporarily allows root access.
2. Why do we need an Exceptions OU?
    - Some administrative actions, like changing the root email, require root access.
3. Why can’t we modify the root account directly?
    - The SCP `ProtectRootAndOrg`restricts root actions, preventing critical changes.
4. Why does this matter for security?
    - Controlled, temporary exceptions ensure governance while allowing necessary administrative tasks.
# The Lab

1. Attached SCP `ProtectRootAndOrg` to all OUs expect the `Exceptions` OU
2. Detach the same SCP from the `Root` account.
		If we left it on then it would still protect the `Exceptions`.
3. Moved the `SecurityAudit` account to the `Exceptions` OU to change the root email and change the name to `LogArchive`.
		"Securely" recovered the Root User Account for `SecurityAudit`
		![screenshot](../../../images/Pasted image 20250312145912.png)
4. Put `LogArchive` account back to `Security` OU and created a `SecurityAudit` account in the same OU.