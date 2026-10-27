---
tags:
  - Amazon Web Services
  - Cybersecurity
---

## The Lesson

- In cloud security, real-time events tell you what's happening right now, which is different from log files that take time to process.
- Logs look backward. They have to be collected, stored, and analyzed, and all that adds delay before you detect anything. Events let you respond right away, so there's less time between detection and action.
- Attackers take advantage of gaps when alerts are slow. Using events lets the security team act in near real time and stop or limit a threat before it does damage.
- Why can't we just process logs faster? Storing and analyzing logs takes a lot of infrastructure and compute, so there's always some delay.
- What is EventBridge? A service that lets AWS resources react to event patterns in real time.
- Why is it useful? Security Hub findings, GuardDuty findings, and CloudTrail API activity all show up as events, and you can act on them right away by routing them through EventBridge.
- Events are like salmon jumping out of a river: if you don't catch them when they show up, they're gone (ephemeral).

## The Lab

1. Deployed an SNS topic that notifies us by email.

    Don't forget to subscribe to the topic.

2. Created an EventBridge rule.

    Whenever a new finding gets imported into Security Hub, an alert goes off.
