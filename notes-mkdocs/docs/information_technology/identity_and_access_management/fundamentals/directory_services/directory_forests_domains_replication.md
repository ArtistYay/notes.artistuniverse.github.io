---
tags:
  - Cybersecurity
  - Identity & Access Management
---

## Domains

Before we understand what a domain is, we have to understand what an object is. An object can be a user, a group, a computer, or an organizational unit (OU). You can think of a domain as a box that holds all these objects.

A common Active Directory structure is the forest at the top level, then the domain (e.g. artistuniverse.tech), and then organizational units (OUs) that hold 'objects' like computers and users.

[Article | Tech Target](https://www.techtarget.com/searchwindowsserver/definition/Active-Directory-domain-AD-domain)

## Forests

A tree is a group of domains that share the same namespace, like `artistuniverse.tech` with a child domain `lab.artistuniverse.tech`. A forest is the top-level container that holds one or more trees, and it's the real security boundary in AD. Even if you only have one domain, it still lives inside a forest. Separate forests don't trust each other unless you set up a forest trust.

## Replication

High availability (HA) is a big deal for a business. Imagine Sally can't sign into her account to do finance work because the one DC in the environment is down. One way to get HA is replication with the Directory Replication Service (DRS) across your DCs (domain controllers). AD uses multi-master replication, so you can reset a user's password on DC A and add a user on DC B, and the two DCs compare notes and copy the changes into each other's AD database.

[Article | Jumpcloud](https://jumpcloud.com/it-index/what-is-the-directory-replication-service-drs#:~:text=Updated%20on%20September%2011%2C%202025,changes%20on%20any%20domain%20controller.)
