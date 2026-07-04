---
tags:
  - Microsoft Azure
  - Compute
---

- It’s a desktop and application virtualization service that runs on the cloud. It enables you to use a cloud-hosted version of Windows from any location.

**Tips from the community:**
 
- Matt McSpirit, a Microsoft Azure MVP, has a walkthrough of running AVD on Azure Stack HCI, on-premises. Worth a look if you ever need a hybrid or data-sovereignty angle.
  [How to run Azure Virtual Desktop on-premises – Microsoft Mechanics](https://techcommunity.microsoft.com/blog/microsoftmechanicsblog/how-to-run-azure-virtual-desktop-on-premises/4046698)

- Anoop C Nair, a Microsoft MVP, has extensive AVD + Intune management content, including a tips-and-tricks deck worth bookmarking.
  [AVD Management With Intune – HTMD Blog](https://www.anoopcnair.com/avd-management-with-intune-windows-virtual-desk/)
  
- A small but easy-to-miss operational detail: if you're deploying a new host pool in a different region using an existing image, that image has to be replicated to the new region first, via the Shared Image Gallery, before you can deploy session hosts from it.
  [Eight tips on how to manage Azure Virtual Desktop – Compete366](https://www.compete366.com/blog-posts/eight-tips-on-how-to-manage-azure-virtual-desktop-avd/)
