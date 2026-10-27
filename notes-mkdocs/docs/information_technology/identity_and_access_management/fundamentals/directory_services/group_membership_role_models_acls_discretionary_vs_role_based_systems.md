---
tags:
  - Cybersecurity
  - Identity & Access Management
---

## Group Membership

In Active Directory you can create groups that hold multiple users who have something in common, whether it's the permissions you're going to give them, their location, their department, etc. Groups are the easiest way to organize. You can apply permissions to the group. For example, in AWS you can create an IAM group and attach a custom (customer managed) policy or an AWS managed policy to it, which grants permissions to certain resources.

[Course | Server Academy](https://serveracademy.com/courses/active-directory-identity-with-windows-server/understanding-groups-and-memberships/)

[Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-groups#group-scope)

## ACLs

When I think of ACLs I think of firewalls. A set of rules that denies or grants access based on what is specified. For example, let's say Jake, Karen, and Natalie all work in the same department. Karen shares a folder with an ACL on it that says only Jake and Karen can access it. If Natalie tries to open the folder she gets an access denied message, even though she works in the same department as Jake and Karen. ACLs can be messy and hard to keep up with causing admin overhead.

## Discretionary Access Control (DAC)

It's when the user who made the resource is the one who decides who gets access to it. Since the user is the owner, they control who's allowed to read, write, list, etc. on that resource. NTFS file permissions on Windows are a classic example.

[Article | NordLayer](https://nordlayer.com/learn/access-control/discretionary-access-control/)

## Role-Based Access Control (RBAC)

With RBAC you can attach a role to a user. That role has specific permissions like what it can do (read, write, list) and what resource it can access (files, applications, etc.) A lot easier to keep up with than ACLs.

[Article | frontegg](https://frontegg.com/guides/rbac-vs-acl)

!!! youtube "Access Control Models"
	<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/Kn41z3fl_UY?si=PRw-ef0QSjh3S8aq" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
