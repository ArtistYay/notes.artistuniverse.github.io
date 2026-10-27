---
tags:
  - Microsoft Azure
  - Cybersecurity
---

- Microsoft Sentinel is a SIEM (security information and event management, a tool an organization uses to collect, analyze, and run security operations on its systems) and a SOAR (security orchestration, automation, and response, which coordinates and automates tasks between people and tools in one platform). It's cloud native and pulls in other Azure services to do its job.

- It collects security data across your whole environment, detects threats, helps you investigate incidents (with AI help), and responds with automation.

- Sentinel lives in the Microsoft Defender portal now. After March 31, 2027, it won't be supported in the Azure portal at all, and anyone still using it there gets redirected to Defender. New customers since July 2025 already get onboarded straight to the Defender portal.

- Main features

    - Data connectors: connect to a bunch of data sources, Microsoft and third party.

    - Analytics rules: analyze your data and create alerts and incidents for suspicious activity.

    - Workbooks: dashboards built on Azure Monitor workbooks. Every tile in a workbook is just a KQL query underneath.

    - Automation: automation rules and playbooks. Playbooks are built on Azure Logic Apps.

    - Hunting: go looking for threats in your data before an alert ever fires.

    - Notebooks: Jupyter notebooks for deeper analysis. With the Sentinel data lake you can also run them from VS Code.

    - It's built on top of a Log Analytics workspace that holds all the data. Data connectors send data into the workspace first, and everything else queries it from there.

- You query everything with KQL (Kusto Query Language).

- Alerts come from analytics rules. You can start from Microsoft's rule templates (they come with solutions in the Content hub) or write your own.

- Rule types

    - Scheduled: the most common one. A KQL query runs on a schedule over a lookback window and creates an alert if the results pass a threshold.

    - NRT (near-real-time): a limited kind of scheduled rule that runs every minute.

    - Anomaly: uses machine learning to learn a baseline and flag behavior outside of it. You can't edit the built-in ones, but you can duplicate one, tune it in Flighting mode, and compare it against the original. Anomalies don't create alerts on their own, they go to the `Anomalies` table so you can use them in hunting and other rules.

    - Microsoft security: creates Sentinel incidents from alerts in other Microsoft security products.

    - Threat intelligence: matches your logs against Microsoft's threat intel indicators. Only one rule allowed.

    - Fusion (advanced multistage attack detection): correlates lots of low-fidelity alerts into one high-fidelity incident. Logic is hidden and only one rule is allowed.

    - ML behavior analytics: Microsoft's own machine learning for weird SSH and RDP logins. Logic is hidden and not customizable.

!!! note "What changes in the Defender portal"
    Once Sentinel is onboarded to the Defender portal (or Defender XDR incident integration is on), the Microsoft security rules and Fusion rules get turned off. Defender XDR creates and correlates the incidents instead. Microsoft is also pushing custom detections as the main way to write new rules across Sentinel and Defender XDR.

[Documentation | Microsoft Learn](https://learn.microsoft.com/azure/sentinel/overview)

[Documentation | Microsoft Learn](https://learn.microsoft.com/azure/sentinel/threat-detection) - Types of analytics rules

[Documentation | Microsoft Learn](https://learn.microsoft.com/azure/sentinel/microsoft-sentinel-defender-portal) - Sentinel in the Defender portal
