### Domains

Before we understand what a domain is, we have to understand what an object is. An object can range from a user, organizational unit (OU), or a computer. You can think of a domain as a boxes to hold all these objects. To give you a visual:

![screenshot](../../../images/ad_structure.png)

A common structure of an Active Directory environment is the forest at the top level (not shown in the picture), then we have the domain (e.g. artistuniverse.tech), thirdly we have organizational units (OUs) that holds 'objects' like computers and users.

[Article | Tech Target](https://www.techtarget.com/searchwindowsserver/definition/Active-Directory-domain-AD-domain)
### Forests

When you have multiple domains on a DC a forest is likely made which is just holding the domains. When you have multiple forests, you make up a tree.

### Replication

Having high availability (HA) in your environment is crucial to a business. Imagine Sally not able to sign into her account for financial purposes because the one DC in the environment is down. A way to achieve HA is with the Directory Replication Service (DRS) across your DCs (Domain Controllers). We currently use Multi-Master Replication, you can reset a users password on DC A and add a user on DC B and the two DCs will compare notes and cache everything in their memories.

[Article | Jumpcloud](https://jumpcloud.com/it-index/what-is-the-directory-replication-service-drs#:~:text=Updated%20on%20September%2011%2C%202025,changes%20on%20any%20domain%20controller.)