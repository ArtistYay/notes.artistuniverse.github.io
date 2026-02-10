# **Step 1: Identify**

The first step in any situation is to identify the perceived problem, or identify what the symptoms are that brought this situation to your attention. Was it a ticket claiming that the server is down, or was it someone calling you because your order-entry workload wasn't saving entries. When someone tells you that the internet is "down," most likely the internet isn't down; they just can't connect to it. Now you need to gather more data.

# **Step 2: Collect**

When you've identified the problem or symptoms, the next step is to collect data with a thorough investigation. Ask probing questions to gather more data. When did it work last? What changes were made? When did it stop working? Are there any errors? Is more than one person having this issue? If so, are all the affected users in one location or spread out? Do the affected users have any commonalities? Are any other workloads impaired? Are the workloads on the same instance, the same Availability Zone, and so on.

Gather diagnostic data, log files, trace data, and data from your observability and monitoring tools, if you have them configured before the incident started. Can you reproduce the issue? Try to get as much information as you can at this stage to help guide you in the best direction to begin investigating.

[![SkillBuilder](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1686938400/y24IvGy6wTq2MbXF4e3RfQ/tincan/914789_1675985891_p1gos8kkf41c1h1tb11mkv1v4b1te34_zip/assets/q5Hxdbxh1firSd3j_b8wFXT1sFermzptD.jpg)](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1686938400/y24IvGy6wTq2MbXF4e3RfQ/tincan/914789_1675985891_p1gos8kkf41c1h1tb11mkv1v4b1te34_zip/assets/q5Hxdbxh1firSd3j_b8wFXT1sFermzptD.jpg)

[![SkillBuilder](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1686938400/y24IvGy6wTq2MbXF4e3RfQ/tincan/914789_1675985891_p1gos8kkf41c1h1tb11mkv1v4b1te34_zip/assets/mgg1BvN4BC9F7HKZ_5PEZxjlCPUdBWRQ6.jpg)](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1686938400/y24IvGy6wTq2MbXF4e3RfQ/tincan/914789_1675985891_p1gos8kkf41c1h1tb11mkv1v4b1te34_zip/assets/mgg1BvN4BC9F7HKZ_5PEZxjlCPUdBWRQ6.jpg)

# **Step 3: Analyze**

Now that you can define the issue and collected useful data, it's time to analyze and sort through the information to determine the root cause. If the issue is reproduceable, this often helps narrow your search. If you have an error, you can parse the logs and data for items pertinent to the error. If you know the last time it worked and the first time the error appeared, you can narrow your search to that specific time frame. Narrowing your focus to analyze smaller and smaller areas or time frames helps you identify when, and possibly why, the issue started.

**Step 4:**

When the issue is identified, you must develop a remediation strategy to make necessary changes to resolve the problem. The resolution could be as simple as restarting a stopped instance, or something larger like troubleshooting a route change or a change to a security group.

**Test and implement your solution.**

For larger issues, testing your solution might require a separate development environment to test the solution. Other times, you might have to test your solution in a production environment to expedite getting the system back online. After the solution is implemented, always test and retest to verify that the issue was successfully resolved.

[![SkillBuilder](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1686938400/y24IvGy6wTq2MbXF4e3RfQ/tincan/914789_1675985891_p1gos8kkf41c1h1tb11mkv1v4b1te34_zip/assets/fBs64M80b1t2Cjxx_PcCJT03H4ImHtg7C.jpg)](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1686938400/y24IvGy6wTq2MbXF4e3RfQ/tincan/914789_1675985891_p1gos8kkf41c1h1tb11mkv1v4b1te34_zip/assets/fBs64M80b1t2Cjxx_PcCJT03H4ImHtg7C.jpg)

[![SkillBuilder](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1686938400/y24IvGy6wTq2MbXF4e3RfQ/tincan/914789_1675985891_p1gos8kkf41c1h1tb11mkv1v4b1te34_zip/assets/5SiZbLDxrsyDPCNq_6QfRu223PvLVgghj.jpg)](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1686938400/y24IvGy6wTq2MbXF4e3RfQ/tincan/914789_1675985891_p1gos8kkf41c1h1tb11mkv1v4b1te34_zip/assets/5SiZbLDxrsyDPCNq_6QfRu223PvLVgghj.jpg)

**Step 5:**

After the situation is resolved and the environment is operational again, meet with the team to review the incident. Determining the cause of the problem helps teams understand what happened, what was involved in the resolution, and what to do during any future incident.

Performing a [root cause analysis(opens in a new tab)](https://wa.aws.amazon.com/wat.concept.rca.en.html) (RCA) helps in identifying what, how, and why an event or failure happened. Was a change made? Was the change control process followed? Was it specific to the workload or environment? Are the instances running and sized appropriately for the workload? Asking questions, such as the [_five whys_](https://wa.aws.amazon.com/wat.concept.fivewhys.en.html)[(opens in a new tab)](https://wa.aws.amazon.com/wat.concept.fivewhys.en.html), helps identify improvements to your process or your environment. Determining the RCA is part of the AWS Well-Architected Framework.

The post-incident review can also address and discuss improvements to the observability strategy. For example, how could a similar issue be detected and isolated in the future? Is there any additional data that could be gathered or used for proactive alarms or notifications? In this step you ask yourself how you can improve your processes and observability solution to avoid similar future incidents.

# **Step 6: Document the solution**

Documenting both the issue and resolution provides your team with a repository of knowledge that can be referenced days, months, and even years after an incident occurs. This type of knowledge repository often functions as the first source of data referenced when an incident occurs. If the same or similar incident is documented, the time to resolution decreases and you can investigate whether these incidents are part of a larger recurring pattern or are single incidents. Additionally, if valued teammates leave the team, if the company changes ownership, or if the team suddenly grows, these reference documents provide a useful onboarding and reference tool for the new or transitioning employees.