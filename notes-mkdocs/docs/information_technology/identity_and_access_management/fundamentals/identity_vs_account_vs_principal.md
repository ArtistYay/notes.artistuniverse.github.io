---
tags:
  - Cybersecurity
  - Identity & Access Management
---

## Identity

It's who you are. For example, I am Artist. That's my identity.

## Account

An account is a digital identity, or a digital container of all the things you have access to. You get into your account with a username and password (and hopefully MFA as well).

## Principal

A principal is anything that can be authenticated and then given permissions: a user, a group, or a non-human identity. The one I deal with the most is a service principal (in Azure) or a role (in AWS), which is basically a special account your apps and resources use to do tasks, based on the permissions you've given it. It can change other resources (write), and it can also look up other resources in your environment (read).
