---
tags:
  - Microsoft Azure
---

- Azure Kubernetes Service let’s you organize containers, replicate container architectures, and have global reach.

- Automating, managing, and interacting with a large number of containers is known as orchestration.

- K8s is an open source container orchestration system for automating application deployment, scaling, and management.

- Azure Container Registry (ACR) keeps track of current valid container images, manages files and artifacts for containers, feeds container images to ACI and AKS.

**Tips from the community:**

- Dave R, an Azure & AI MVP, makes a good "don't overthink it" point: even AKS running on unusual infrastructure, like Azure Local bare metal, is still just a first-class AKS cluster. No separate console, no different operational model. It shows up right alongside your cloud clusters in Fleet Manager.
  [Azure Linux on AKS: What Changes When Microsoft Owns the Node OS – ITNEXT](https://itnext.io/azure-linux-on-aks-what-changes-when-microsoft-owns-the-node-os-a17eb82e18e0)

- A couple of debugging tricks worth stealing: `kubectl debug node/<node-name> -it --image=ubuntu` gets you a shell on the underlying node itself, even though AKS is managed. And when something looks like a Kubernetes problem, check the whole request path first, one team spent a while debugging inside the cluster before realizing a reverse proxy sitting in front of it was the real source of a recurring timeout.
  [Beyond the AKS Basics: Practical Tips – Jumping Rivers](https://www.jumpingrivers.com/blog/beyond-azure-kubernetes-service-basics/)
