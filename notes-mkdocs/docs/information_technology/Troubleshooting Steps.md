---
tags:
  - Fundamentals
---

## Step 1: Identify

First, figure out what the problem actually is, or at least what the symptoms are that brought it to your attention. Was it a ticket saying the server is down? Someone calling because the order-entry app isn't saving entries? When someone tells you "the internet is down," the internet is almost never down. They just can't connect to it. So now you need more data.

## Step 2: Collect

Once you know the problem (or the symptoms), dig in and collect data. Ask a lot of questions:

- When did it last work?
- What changed?
- When did it stop working?
- Are there any errors?
- Is more than one person having this issue? If so, are they all in one location or spread out?
- Do the affected users have anything in common?
- Are any other workloads having problems? Are they on the same instance, the same Availability Zone, and so on?

Grab diagnostic data, log files, trace data, and whatever your observability and monitoring tools captured (if they were set up before the incident started). Can you reproduce the issue? Get as much info as you can here, because it points you in the right direction when you start investigating.

## Step 3: Analyze

Now that you can define the issue and you've collected data, sort through it to find the root cause. If you can reproduce the issue, that usually narrows things down a lot. If there's an error, search the logs for anything related to it. If you know the last time it worked and the first time the error showed up, focus on that time window. The smaller you can make the area or time frame you're looking at, the easier it is to figure out when (and maybe why) it started.

Once you find the issue, come up with a plan to fix it. The fix could be as simple as restarting a stopped instance, or something bigger like tracking down a route change or a security group change.

!!! note "Test and implement your solution"
    For bigger issues, you might need a separate dev environment to test the fix first. Other times you might have to test it in production to get the system back up faster. Either way, once the fix is in, test and retest to make sure it actually worked.

After everything is back up, meet with the team to go over the incident. Understanding what caused the problem helps everyone know what happened, what it took to fix it, and what to do next time.

A root cause analysis (RCA) figures out what happened, how, and why. Was a change made? Did it go through change control? Was it specific to this workload or environment? Are the instances running and sized right for the workload? Asking questions like the _five whys_ helps you find improvements to your process or your environment. RCA is part of the AWS Well-Architected Framework too.

The post-incident review is also a good time to talk about improving observability. How could you detect and isolate this kind of issue faster next time? Is there other data you could collect, or alarms and notifications you could set up ahead of time? This is where you ask how to improve your processes and monitoring so it doesn't happen again.

## Step 4: Document the solution

Writing down the issue and how you fixed it builds a knowledge base your team can look back on days, months, or even years later. A lot of the time it's the first place people look when something breaks. If the same (or a similar) incident is already documented, you fix it faster, and you can tell whether it's part of a bigger recurring pattern or a one-off. It also helps a ton if teammates leave, the company changes owners, or the team suddenly grows, since new people can use it for onboarding and reference.
