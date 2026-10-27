---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lesson

- CloudFormation lets you define infrastructure in declarative templates (infrastructure as code, IaC). IaC makes things consistent and repeatable, so there's less chance of a manual mistake turning into a security problem (like a misconfigured permission or exposed data).

## The Lab

- Pasted a template URL to create an SNS topic and named it "SecurityAlerts". Did this in `us-east-1`.

    Deploying SNS topics with IaC means your security alert notifications get set up the same way every time, so you can respond quickly when something happens.

    Always check where an IaC template came from and what's in it before you deploy it. Regular reviews and automated security checks (like scanning for hardcoded credentials) should be part of the process.

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Template to create a SNS topic named SecurityAlerts
Resources:
  SecurityAlertsTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: SecurityAlerts
```
> The _Resources_ block has everything you want it to build. _Type_ is what we're building, and _Properties_ are the configuration settings.

- To get alerts we _subscribe_ to a topic. Subscriptions can be text messages, emails, or fancier internal stuff for building event-driven notification systems for apps.
