---
tags:
  - Microsoft Azure
  - Compute
---

- Azure Virtual Desktop (AVD) is a desktop and app virtualization service that runs in the cloud. You can use a cloud-hosted Windows desktop from anywhere.

Tips from the community:
 
- Matt McSpirit has a walkthrough of running AVD on-premises on Azure Stack HCI (now called Azure Local). Worth a look if you ever need a hybrid or data-sovereignty angle.
  [How to run Azure Virtual Desktop on-premises | Microsoft Mechanics](https://techcommunity.microsoft.com/blog/microsoftmechanicsblog/how-to-run-azure-virtual-desktop-on-premises/4046698)

- Anoop C Nair, a Microsoft MVP, has extensive AVD + Intune management content, including a tips-and-tricks deck worth bookmarking.
  [AVD Management With Intune | HTMD Blog](https://www.anoopcnair.com/avd-management-with-intune-windows-virtual-desk/)
  
- A small but easy-to-miss operational detail: if you're deploying a new host pool in a different region using an existing image, that image has to be replicated to the new region first, through Azure Compute Gallery (it used to be called Shared Image Gallery), before you can deploy session hosts from it.
  [Eight tips on how to manage Azure Virtual Desktop | Compete366](https://www.compete366.com/blog-posts/eight-tips-on-how-to-manage-azure-virtual-desktop-avd/)
