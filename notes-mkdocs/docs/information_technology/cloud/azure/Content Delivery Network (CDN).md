---
tags:
  - Microsoft Azure
  - Computer Networking
---

- It is a distributed network of servers that can deliver web content close to users.

- You can use geo-filtering to limit the access that client hosts in specific geographies have to Azure CDN content.

Tips from the community:
 
- Manoj, a Microsoft MVP who blogs as "The Code Blogger," has a walkthrough of geo-filtering for Standard-tier profiles. One detail from it: Standard Microsoft profiles don't support path-based geo-filtering at all. That used to need the Akamai or Verizon (Edgio) tiers, but both of those are retired now. In Azure Front Door, you'd do this with WAF geo-match rules.
  [Azure CDN: Adding Restrictions by Region | The Code Blogger](https://thecodeblogger.com/2020/12/23/azure-cdn-adding-restrictions-by-region/)

- This one changes the long-term guidance: "CDN Standard from Microsoft (classic)" retires on September 30, 2027, and it hasn't allowed new profiles since August 15, 2025. Azure Front Door Standard/Premium is the replacement.
  [Azure Content Delivery Network | Microsoft Azure](https://azure.microsoft.com/en-us/products/cdn)