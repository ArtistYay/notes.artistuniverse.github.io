---
tags:
  - Microsoft Azure
  - Computer Networking
---

- Manages the requests that clients send to web apps hosted on a pool of web servers. For example, if a request is for `/videos`, it can send it to the servers that handle videos. It's basically an advanced (layer 7) load balancer.

- It looks at the HTTP request itself (like the URL path or host name) instead of just the IP address and port, so traffic for a specific web address can go to a specific set of servers.

- Application Gateway provides features such as load balancing HTTP traffic, web application firewall, and support for TLS/SSL encryption of traffic between users and an application gateway, and between application servers and an application gateway.

- Health probes allow the application gateway to determine which hosts in the back-end pool are no longer responding.

- Connection draining lets you remove an instance from a back-end pool so that it doesn't receive any new traffic. Connection draining is useful in maintenance scenarios during which you want to gracefully remove traffic from a node.

- Supports autoscaling, end-to-end encryption, zone redundancy, and multi-site hosting (the v2 SKU).
