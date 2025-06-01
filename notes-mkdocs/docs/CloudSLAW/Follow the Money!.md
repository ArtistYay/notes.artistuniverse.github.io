# The Lesson

- Unexpected charges often signal an attack or misconfiguration. In cloud security, cost monitoring through billing alerts is an additional layer of detection that can help you identify cryptomining activities, denial of service attacks, or resource mismanagement.
- By leveraging CloudWatch, AWS users can monitor resource utilization, performance, and billing metrics in one centralized location. It enables proactive security and operational management, helping to reduce risk and avoid surprise bills.
- SNS plays a critical role in cloud security alerting. By configuring alerts to notify administrators via email (or other protocols), teams can ensure they are always aware of potential security incidents or billing anomalies.
# The Lab

1. Signed into 'Root' to enable IAM admin user access to billing information.
		By default, IAM users do not have permission to view billing data. Allowing your non-root admin user to access billing data ensures that security professionals or administrators can monitor unexpected charges and act quickly to mitigate risks.
2. Enabled CloudWatch Billing Alerts
		CloudWatch is AWS’s monitoring service, which can track a wide range of metrics, including billing data. By enabling CloudWatch billing alerts, you can monitor your spending in real-time and create alarms for specific thresholds.
3.  Created a Billing Alarm with a $25 threshold
		Setting up a billing alarm is critical for detecting unexpected or anomalous charges. For example, cryptomining or resource misconfigurations could result in significant bills. These alarms act as a safety net to alert you before costs spiral out of control.
4. Associate the Alarm with SNS Topic
		By linking the alarm to an SNS topic, you ensure that you are notified through an email or other communication channels when the threshold is exceeded. This is crucial for taking immediate action to address any suspicious activity or misconfigurations.
5. Subscribe to the SNS Topic
		Subscribing to the SNS topic is the final step to ensure that you get notified when the billing alert is triggered. Prompt notifications allow you to take swift action to mitigate any unwanted charges or security issues, such as stopping a cryptomining attack or addressing a misconfigured service.