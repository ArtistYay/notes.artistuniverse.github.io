# The Lesson

- CloudFormation allows you to define infrastructure using declarative templates. IaC enables consistency and repeatability in cloud environments, reducing the chance of manual errors that could lead to security vulnerabilities (e.g., misconfigured permissions, exposure of sensitive data).
# The Lab

- Pasted a template URL to create an SNS topic, and named it "SecurityAlerts". Did this in the `us-east-1`
		Deploying SNS topics through IaC ensures that your notifications (e.g., alerts for security events) are set up consistently, allowing for quick responses to security incidents.
		Always verify the source and content of IaC templates to ensure they are secure before deployment. Implementing processes for regular reviews and automated security checks (e.g., scanning for hardcoded credentials) is critical.

```
AWSTemplateFormatVersion: '2010-09-09'
Description: Template to create a SNS topic named SecurityAlerts
Resources:
  SecurityAlertsTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: SecurityAlerts
```
> The _Resources_ block includes all the things you want it to build. _Type_ is what we are building, and _Properties_ are configuration settings. 

- To get alerts we _subscribe_ to a topic. Subscriptions can be for text messages, emails, or fancy internal things to create complex event-driven notification buses for applications.
