---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lesson

- Surprise charges are often a sign of an attack or a misconfiguration. Billing alerts are an extra layer of detection that can catch cryptomining, denial of service attacks, or resources someone forgot about.
- CloudWatch lets you watch resource usage, performance, and billing metrics in one place, so you can catch problems early and avoid surprise bills.
- SNS is a big part of security alerting. Sending alerts to admins by email (or other ways) means the team actually finds out about security incidents or weird billing.

## The Lab

1. Signed into root to turn on IAM access to billing information.

    By default, IAM users can't see billing data. Letting your non-root admin see it means the people watching security can spot unexpected charges and act fast.

2. Turned on CloudWatch billing alerts.

    CloudWatch is AWS's monitoring service and it can track a lot of metrics, including billing. Once billing alerts are on, you can set alarms for specific spending thresholds. (Billing metrics only live in `us-east-1`.)

3. Created a billing alarm with a $25 threshold.

    This is your safety net for unexpected charges. Cryptomining or a misconfigured resource can run up a huge bill, and the alarm tells you before it gets out of control.

4. Connected the alarm to an SNS topic.

    Linking the alarm to SNS is what actually sends you an email (or another notification) when the threshold gets crossed.

5. Subscribed to the SNS topic.

    The last step, so the notification actually reaches you. Getting told right away is what lets you stop a cryptomining attack or fix a misconfigured service before it costs you more.

!!! tip
    AWS Budgets and Cost Anomaly Detection are worth turning on too. Budgets can alert on forecasted spend, and Cost Anomaly Detection uses machine learning to flag spending that doesn't match your normal pattern.
