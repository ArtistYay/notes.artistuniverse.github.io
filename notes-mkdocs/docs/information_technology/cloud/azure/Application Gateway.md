---
tags:
  - Azure
Keyword: Networking
---
- Manages the request that client applications send to web apps that are hosted on a pool of web servers. For example, if your client sends videos it will go to a server that deals with videos. It’s an advanced load balancer.

- Works on the HTTP request of the traffic, instead of the IP address and port. Traffic from a specific web address can go to a specific machine.

- Application Gateway provides features such as load balancing HTTP traffic, web application firewall, and support for TLS/SSL encryption of traffic between users and an application gateway, and between application servers and an application gateway.

- Health probes allow the application gateway to determine which hosts in the back-end pool are no longer responding.

- Connection draining allows you to deregister an instances in a back end pool so that it doesn’t receive any new traffic. Connection draining is useful in maintenance scenarios during which you wan to gracefully remove traffic from a node.

- Supports auto-scaling, end to end encryption, zone redundancy and multi site hosting.