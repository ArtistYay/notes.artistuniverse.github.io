# The Lesson

- In cloud security, real-time events provide immediate signals about system activities, which differ from traditional log files that require time to process.
- Logs are retrospective—they require collection, storage, and analysis, which can introduce delays in threat detection. Events, however, enable immediate responses, reducing the time between detection and action.
- Attackers can exploit gaps in security monitoring if alerts are delayed. Using events allows security teams to act in near real-time, preventing or mitigating potential threats before damage is done.
- **Why can’t we just process logs faster?** Log storage and analysis introduce infrastructure and computational overhead.
- **What is EventBridge?** A service that allows AWS resources to react to event patterns in real time.
- **Why is it useful?** Security Hub findings, GuardDuty alerts, and CloudTrail logs generate security events that can be acted upon immediately when routed through EventBridge.
- Events are like salmon jumping out of a river: if you don’t catch them when they appear, they’re gone (ephemeral).
# The Lab

1. Deployed an SNS that will notify us via email.
		Don't forget to subscribe to the SNS.
2. Created an EventBridge rule 
		Whenever a new finding is imported into Security Hub an alert goes off.