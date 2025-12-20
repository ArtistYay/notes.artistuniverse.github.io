### Group Membership

In Active Directory you can create groups which holds multiple users but have the something in common. Weather it's the permissions your going to give, the location of the user, the department they are in, etc. Groups are the easiest way to organize. You can apply permissions to said group, for example, in AWS you can create a group and give a group a custom role or and AWS managed role which grants permissions to certain resources.

[Course | Server Academy](https://serveracademy.com/courses/active-directory-identity-with-windows-server/understanding-groups-and-memberships/)

[Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-groups#group-scope)
### ACLs

When I think of ACLs I think of firewalls. A set of rules that denies or grants access based on what is specified. For example, let's say Jake, Karen, and Natalie all work in the same department. Karen sends a folder that has set an ACL on said folder that specifics only Jake and Karen can access the folder. If Natalie try's to access the folder she gets a denied message even though she works in the same department as Jake and Karen. ACLs can be messy and hard to keep up with causing admin overhead.
### Discretionary Access Control (DAC)

It's when the user who made the resource is the main one you gives access to that resources. Since the user is the owner, they are able to control who is privilege to read, write, list, etc. on that resources.

[Article | NordLayer](https://nordlayer.com/learn/access-control/discretionary-access-control/)
### Role-Based Access Control (RBAC)

With RBAC you can attach a role to a user. That role has specific permissions like what it can do (read, write, list) and what resource it can access (files, applications, etc.) A lot more easy to keep up with than ACLs.

[Article | frontegg](https://frontegg.com/guides/rbac-vs-acl)

!!! youtube "Access Control Models"
	<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/Kn41z3fl_UY?si=PRw-ef0QSjh3S8aq" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>