---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lesson

1. Why move the SCP off the root?
    - So we can have an Exceptions OU that's allowed to use root temporarily.
2. Why do we need an Exceptions OU?
    - Some admin tasks, like changing the root email, need the root user.
3. Why can't we just change the root user directly?
    - The `ProtectRootAndOrg` SCP blocks root actions, so those changes would get denied.
4. Why does this matter for security?
    - Controlled, temporary exceptions keep governance in place while still letting you do the admin tasks you have to do.

## The Lab

1. Attached the `ProtectRootAndOrg` SCP to every OU except the `Exceptions` OU.
2. Detached the same SCP from `Root`.

    If we left it on Root, it would still apply to `Exceptions` because SCPs inherit down.

3. Moved the `SecurityAudit` account into the `Exceptions` OU so I could change its root email and rename it to `LogArchive`.

    "Securely" recovered the root user for `SecurityAudit`.

    ![screenshot](../../../images/Pasted image 20250312145912.png)

4. Moved `LogArchive` back into the `Security` OU and created a new `SecurityAudit` account in the same OU.

!!! note
    AWS has centralized root access management now. Instead of the Exceptions OU dance, the management account (or a delegated admin) can remove root credentials from member accounts and run root-only tasks with short-term root sessions.
