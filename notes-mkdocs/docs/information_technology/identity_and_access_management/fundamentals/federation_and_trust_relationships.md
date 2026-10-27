---
tags:
  - Cybersecurity
  - Identity & Access Management
---

## Federation

Let's say you have users that aren't part of your organization, but you want them to use the applications you host in your environment (B2C). Let's also say your users don't want to make an account for every app, they want to log into all of them with the same Google account. Well, that's where federation comes in.

It's a trust relationship between two or more domains. A collection of IdPs and SPs that agree to work together and trust each other to make that happen.

So what exactly is a trust relationship?

[Article | Oracle](https://docs.oracle.com/cd/E19575-01/820-3740/ggyyh/index.html)

[Forum | Stack Exchange](https://security.stackexchange.com/questions/218193/difference-between-trust-and-federation)

## Trust Relationship

This relationship is like a partnership. There are agreements and contract obligations between the partners that build the trust for the federation. On the technical side, the trust is usually the two sides exchanging metadata and signing certificates, so each one can verify the other's messages.

!!! youtube "Old Professor Messer Video"
	<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/78gbVmjFGcs?si=eDdlaH99mOYtr4Wd" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
