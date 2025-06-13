# The Lesson

- CloudTrail provides a centralized record of nearly all administrative actions within an AWS account.
- Enable **multi-region trails** to ensure comprehensive logging.
- Store logs in a **private, encrypted S3 bucket**.
- Avoid using custom encryption keys unless necessary (to reduce management overhead).
- Verify that **log file validation is enabled** for forensic integrity.
- **Management Events**: Logs admin actions (e.g., IAM changes, EC2 modifications).
- **Data Events**: Logs access to resources (e.g., S3 object reads/writes). **Incurs additional costs**.
- **Insights Events**: Detects unusual API activity but requires additional AWS charges.