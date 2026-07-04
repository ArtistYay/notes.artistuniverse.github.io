---
tags:
  - Microsoft Azure
  - Computer Networking
---

- It is a distributed network of servers that can deliver web content close to users.

- You can use geo-filtering to limit the access that client hosts in specific geographies have to Azure CDN content.

**Tips from the community:**
 
- Manoj, a Microsoft MVP who blogs as "The Code Blogger," has a walkthrough of geo-filtering specifically for Standard-tier profiles, including a detail worth adding: Standard Microsoft profiles don't support path-based geo-filtering at all. You need Standard Akamai or Verizon for that.
  [Azure CDN – Adding Restrictions by Region – The Code Blogger](https://thecodeblogger.com/2020/12/23/azure-cdn-adding-restrictions-by-region/)

- Worth flagging directly in this file since it changes long-term guidance: "CDN Standard from Microsoft (classic)" is on a retirement path for September 30, 2027, with Azure Front Door as its replacement.
  [Azure Content Delivery Network – Microsoft Azure](https://azure.microsoft.com/en-us/products/cdn)