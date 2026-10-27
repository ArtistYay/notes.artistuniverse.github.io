---
tags:
  - Cybersecurity
  - Cloud
---

## Why Wiz Exists

### The Problem Wiz Solves
Before Wiz, answering a simple question like "Do I have any databases with sensitive data open to the public internet?" was nearly impossible. Here's why:

- Cloud complexity: multiple providers, thousands of technologies, and it keeps growing.
- Siloed tools: every security tool (CSPM, CIEM, CWPP, DSPM) made findings on its own with no shared context.
- Alert fatigue: no correlation between findings means way too many alerts and no way to prioritize.
- Agent dependency: most tools needed agents on every workload, which slowed deployment and left gaps.
- Shared responsibility confusion: customers didn't fully understand what *they* were responsible for securing.

### The Shared Responsibility Model
- IaaS (VMs): the customer is responsible for the OS, apps, and network config.
- PaaS: the cloud provider handles more, but the customer is still responsible for their data and apps.
- SaaS: the provider handles almost everything, and the customer handles access and data governance.

### What Wiz Does Instead
- A complete agentless scan of every cloud resource through APIs. No agents and no network changes.
- Deep assessment across vulnerabilities, misconfigurations, identities, secrets, and lateral movement paths.
- Toxic combination detection, which correlates findings across domains into prioritized issues.
- One view across AWS, Azure, GCP, OCI, Kubernetes, and VMware.
- Remediation guidance with business context, sent to the right teams through Jira, Slack, or ServiceNow.

### Three Success Criteria
1. Accuracy: less noise and fewer false positives.
2. Speed and scale: enterprise ready, deploys in minutes at any size.
3. User perspective: meets each team (security, DevOps, developers) where they already work.

---

## First-Gen Tools

These are the siloed point solutions Wiz consolidates or replaces. Know these cold.

| Acronym | Full Name | What It Does | Shortcoming |
|---------|-----------|--------------|-------------|
| CSPM | Cloud Security Posture Management | Scans cloud services for misconfigurations. API-based. | Only sees cloud config, with no vulnerability or identity context. Siloed. |
| CIEM | Cloud Infrastructure Entitlements Management | Manages access rights and permissions across cloud identities | No blast radius context. Siloed. |
| CWPP | Cloud Workload Protection Platform | Protects workloads with intrusion detection, vulnerability scanning, and behavior monitoring. Agent-based. | Agent-based. Siloed. |
| DSPM | Data Security Posture Management | Finds sensitive data (PII, PHI, financial) in storage | Data findings with no exposure or identity context. Siloed. |
| KSPM | Kubernetes Security Posture Management | Scans K8s for misconfigurations. API-based. | Only covers one architecture. Siloed. |
| SASE | Secure Access Service Edge | Cloud-hosted firewall/gateway that inspects traffic and detects intrusions | Only sees traffic, can't see inside workloads. |
| CASB | Cloud Access Security Broker | Makes sure access is authorized, watches for suspicious activity, and enforces policies on SaaS | SaaS only. Limited visibility. Siloed. |
| SSPM | SaaS Security Posture Management | Finds misconfigurations and risky settings in SaaS apps (like Microsoft 365, Salesforce, Slack) | SaaS only. Siloed. |

The main takeaway: all of these tools have limited visibility and don't share context. Wiz replaces or consolidates them into one security graph.

---

## Architecture

### Design Principles
- Eventually consistent: components run independently and asynchronously, and the data comes together on the graph over time. Performance and availability come before instant consistency.
- Asynchronous: microservices in containers that talk through message queues, so things can run in parallel and survive failures.
- Resilient: uses cloud availability zones, load balancing, auto-scaling, and multi-region replication. Images are immutable and nodes are stateless.

### Deployment Model (SaaS)
All services run in Wiz-managed tenants. This is the simplest and most common setup. Wiz holds SOC 2 Type 2, ISO 27001, PCI, and HIPAA certifications.

### Six Phases of Data Flow

```
Phase 1: CONNECT      → API connection to cloud (agentless, no network changes)
Phase 2: SCAN         → Cloud Scanner (API) + Workload/Volume Scanner (snapshot)
Phase 3: ENRICH       → Vulnerabilities, patches, configs, IAM, secrets, lateral movement
Phase 4: REFINE       → Validate findings, reduce false positives
Phase 5: ANALYZE      → Build the security graph, identify toxic combinations, prioritize
Phase 6: AUTOMATE     → Push remediation guidance to Jira, Slack, ServiceNow, etc.
```

### Main Architecture Components
- Cloud Scanner (fetcher): makes read-only API calls to get inventory, configs, network, identity, and audit logs.
- Workload/Volume Scanner: snapshots OS disks and scans them. It runs in a dedicated Wiz account *in the same region* as the customer. Zero-copy, meaning it mounts, scans, and deletes.
- Analysis Engine: a Kubernetes cluster in the Wiz backend that runs enrichment, calculates exposure, and runs controls.
- Security Graph: a graph database (AWS Neptune, plus Postgres for non-normalized data). All results get written here.
- GraphQL API: the only way into the Wiz platform. Authentication uses AWS Cognito tokens.

### Authentication Model
- One way in: the GraphQL API
- Auth through an AWS Cognito refresh token
- No web server, the portal is a single-page app making GraphQL queries

---

## Security Graph

### What It Is
The security graph is two things at the same time:
1. A graph database running in the Wiz backend that stores everything Wiz discovers and figures out.
2. A query interface in the Wiz portal where you run queries and see the results.

### Three Roles of the Graph
1. Knowledge representation: stores discovered inventory plus derived enrichments (lateral movement, blast radius, exposure paths).
2. Enrichment input: API scan data and workload scan data feed the enrichment engines, and the results go back into the graph.
3. Query foundation: every control, issue detection, and custom query runs against the graph.

### What Makes It Different
- Alive: background microservices update it constantly. It's never static.
- Normalized: cloud-specific names get mapped to Wiz names. For example, AWS EC2, Azure Compute, and GCP Compute Instance are all called "Virtual Machine" in Wiz, so you can write one query that works across clouds.

### Why a Graph Database?
A graph DB stores connected data as nodes (resources) and edges (relationships). That's perfect for questions like "find VMs with critical vulnerabilities that are internet exposed and have admin privileges." Being able to query relationships is what makes toxic combination detection possible.

### Graph Colors (Portal)
- Yellow = Technology
- Orange = Networking
- Purple = Identity/Permissions
- Blue = Cloud resource
- Aqua = Secrets
- Gray = Cloud org metadata / Wiz projects
- Red = Config finding or vulnerability
- Green = Sensitive data

### Graph Build Cycle
- Scheduled: once per day per connector
- Event-based: when a resource is created, deleted, started, or stopped
- Ongoing enrichment: vulnerability checks, patch assessments, technology updates

### Query Structure
- Root: the first node in the query, the main thing you're looking for.
- Condition: the where clause that filters by property values.
- Clause: narrows the conditions down more (using `that` statements).
- Properties: attributes that filter a node.
- Results: everything that matches the query.

### Controls
Controls are saved security graph queries plus a severity rating. They turn attacker playbooks into queries. When a control matches resources in your environment, it creates issues.

---

## Cloud Scanner

Also called the cloud fetcher or API scanner.

### What It Does
Makes read-only API calls (GET, LIST, DESCRIBE) to the cloud provider APIs. It collects:
- Resource inventory (VMs, buckets, databases, etc.)
- Network configuration
- Identity/IAM data
- Cloud audit logs
- Advanced resource parameters

### How It Works
- Connector Operator: handles the timing and scheduling of scans.
- Cloud Platform Fetcher: one pod per subscription, with up to 20 pods running in parallel.
- It pushes results to the enrichers and to the workload scanner (as a list of volume IDs to scan).

### Connector Types
| Level | What It Covers | Recommendation |
|-------|---------------|----------------|
| Organization level | The whole cloud org, and it auto-discovers new subscriptions | Recommended |
| Subscription level | A single account/subscription/project | Leaves blind spots |

### Normalized Terminology
| Wiz Term | AWS | Azure | GCP |
|----------|-----|-------|-----|
| Cloud Organization | Organization | Root Management Group | Organization |
| Subscription | Account | Subscription | Project |
| Resource Group | N/A | Resource Groups | N/A |

### Scanning Frequency
- Full cloud scan: once per day
- Event-triggered scanning: create/update/delete events kick off a targeted rescan of the affected resources between full scans.
- On-demand rescan: you can trigger it yourself by connector, subscription, or individual resource.

### Graph Timestamps
- Creation date: when the resource was created in the cloud.
- First seen: when Wiz first found it.
- Last changed: when Wiz last changed its graph properties (this can be after last seen because enrichments run async).
- Last seen: the last time the cloud scanner saw it.

### Double Scanning
When two connectors overlap (like an org-level connector and a subscription-level connector covering the same subscription), that subscription gets scanned twice. The graph doesn't duplicate resources, but it wastes compute and can mess with resource counts. Avoid it.

---

## Workload Scanner

Also called the disk scanner or volume scanner.

### What It Is
An agentless service that takes a snapshot of a workload's OS disk, mounts it read-only, scans it, then deletes it. No agents, no network changes, and no impact on production.

### What It Detects
From OS disks:
- Installed packages and versions (Linux: package manager. Windows: installed programs, services, hotfixes)
- Operating system metadata (type, build version)
- Running containers
- Local users and auth config
- Vulnerabilities
- Secrets (hardcoded credentials, API keys, tokens)
- Malware (file hash comparison plus YARA rules)
- Host configuration compliance (CIS benchmarks)
- Forensics data

### Zero-Copy Architecture
Wiz never copies the snapshot across regions or networks. The scanner cluster (in the same cloud and region as the customer) mounts the snapshot as a read-only volume, scans it, and deletes it. Usually under 10 minutes.

### High-Level Steps
1. Cloud scanner sends a list of volume IDs to the workload scanner.
2. Workload scanner creates a snapshot in the customer account.
3. The snapshot gets shared with the Wiz scanner cluster (same region).
4. The scanner mounts the snapshot, scans it, and pulls out metadata.
5. Metadata (not the raw data) gets sent to the Wiz backend.
6. The snapshot gets deleted. It's tagged `wiz-auto-gen-snapshot` so it's easy to spot.

### Regional Isolation
Workload scans always happen in the same region as the customer's workloads. That helps with:
- Data sovereignty compliance
- Performance and scaling
- Keeping data from crossing regional boundaries

### Encrypted Disk Handling (AWS)
Uses the re-encrypt permission. AWS decrypts the snapshot with the customer's key, then re-encrypts it with a Wiz key. Wiz never sees the customer key.

### Inactive Workloads
Wiz scans active AND inactive workloads because:
- A machine that's off today can be turned back on with new vulnerabilities that were found while it was sitting there.
- Infrastructure changes (new exposure paths, security group changes) might make it unsafe to turn back on.
- Attackers can snapshot inactive machines the same way Wiz does.

### Security Tool Scan Object
When a workload gets scanned, Wiz creates a `security_tool_scan` object on the graph attached to the resource. Use it to check scan status, look for errors, and see scan history.

---

## Wiz Outpost

### What It Is
A deployment model where the workload scanning infrastructure runs *inside the customer's cloud* instead of Wiz's. Only metadata (scan results) leaves the customer environment, never raw disk data.

### When to Use Outpost
- Highly regulated industries (financial services, defense, pharma)
- Private resources that aren't internet facing (needs network peering or private endpoints)
- Sovereign clouds (Azure China, AWS China, GovCloud)

### Three Outpost Types
| Type | Description | Who Controls |
|------|-------------|-------------|
| Wiz Automated Outpost | Fully automated. Wiz manages the cluster, scaling, and network | Wiz manages everything |
| Self-Managed Network Outpost (BYON) | Customer provides the network and Wiz deploys clusters inside it | Customer manages network |
| Self-Managed Outpost | Customer owns everything: images, deployment, maintenance | Customer manages all |

90% of use cases use the Wiz Automated Outpost.

### Outpost Components (All 5 Are in Every Deployment)
1. State bucket: holds Helm charts and configs for the workloads on the K8s clusters.
2. Principals: IAM roles (AWS), enterprise apps/service principals (Azure), managed service accounts (GCP).
3. Queue: volume IDs flow through here. SQS (AWS), Service Bus (Azure), Pub/Sub (GCP).
4. Clusters: K8s clusters (EKS, AKS, GKE) where the scanning happens.
5. Secrets: stored in AWS Secrets Manager, Azure Key Vault, or GCP Secret Manager.

### Principal Scopes
- Read Only: powers the connector and reads cloud inventory.
- Orchestrator: builds the cluster, VNets, and scanning resources.
- Worker: handles scaling and cluster management.
- Scanner: creates and manages the snapshots/clones for scanning.

### Outpost vs SaaS Scanning
They're almost the same. The only difference is the scanner account moves from a Wiz-owned trusted account (SaaS) to an account inside the customer's cloud (Outpost). Either way, only metadata leaves, never raw snapshot data.

---

## Boards, Threat Center & Inventory

### Boards (Dashboards)
Boards are visual summaries of issues, organized by risk domain (external exposure, entitlements, secrets, vulnerabilities, etc.).

Board types:
- Overview: the default landing page. Shows total issue counts, trends, burn-down rate, compliance score, and top issues.
- Managed by Wiz: built-in boards for each risk domain. You can't edit them, but you can clone them.
- Private boards: made by a user and only visible to them until they share it.
- Shared boards: custom boards shared at the project, global, or org level.
- Champion Center / Journey Center: an onboarding tracker that shows how much of Wiz you've turned on.

KPIs on the Overview board:
- Issue count by severity (critical/high/medium/low) with the trend vs. last week
- Average issue age (vs. SLA)
- Burn-down rate: are issues getting fixed faster than new ones show up? (You want fixed > found.)
- Compliance score by framework (PCI, SOC 2, NIST, etc.)
- Projects with the most issues

Board access control:
- Private: only the creator
- Project: members of that project
- Global users: anyone with a global role
- Organizational: all users

Creating custom widgets: start from the Issues page, Security Graph, Technologies, Vulnerabilities, or the Control drawer, filter to what you need, then save it as a board widget.

### Threat Center
A Wiz-maintained news feed of cloud-focused threats (not a generic threat database). The Wiz Threat Research team runs it.

What it answers:
- "Am I affected by this threat?"
- "What is it?"
- "Is it a problem for my cloud?"

Threat icons:
- Red exclamation: a finding or issue was found in YOUR environment.
- Orange exclamation: the fix is outside of Wiz (it's a CSP-level threat).
- Green check: the threat exists but wasn't found in your environment.
- Blue eye: informational only (the CSP already mitigated it).

Coverage:
- Goes back to February 2021 (SolarWinds).
- New threats get added within 24 hours of being published (Wiz added Log4Shell 8 hours after the CVE came out).
- Focuses on cloud-specific threats like APIs, libraries, CSP platform services, and Kubernetes.

Automation: you can set up automation rules so when a new threat creates an issue in the "high profile threat" risk category, it opens a Jira ticket, sends a Slack message, or sends an email.

### Inventory (Technologies Page)
Shows every technology found across all your connected clouds: cloud services, OS packages, libraries, and SaaS resources.

Coverage status:
- Supported (full coverage): the technology is fully normalized and assessed for risk.
- Partial coverage: the technology was found but isn't normalized yet. This is where bleeding-edge stuff and shadow IT show up.

Technology types:
- Hosted technology: found on a workload (VM, container, serverless). The customer is responsible for patching and upgrading it.
- Non-hosted technology: a cloud service that isn't running on compute the customer manages (like a managed database). The third party is responsible for patching it.

Shadow IT workflow: technologies start as `Unreviewed` and can be set to `Approved`, `Required`, or `Unwanted`.
- Automation rule: if an Unwanted technology shows up, send an alert.
- Example: mark Windows Server 2008 as Unwanted, and you get an alert any time someone spins one up.

Use cases:
- Visibility across all your clouds
- Multicloud inventory management
- Finding workloads that are missing required agents
- Lifecycle, version, and patch management
- Shadow IT governance

---

## Issues, Findings & Network Exposure

### Findings vs. Issues (the big difference)

| Term | Definition |
|------|-----------|
| Finding | A weakness on one specific resource. One data point. Example: "This VM has CVE-2024-1234" or "This bucket allows public access." |
| Issue | A toxic combination: multiple findings across risk domains that together are a real, prioritized risk. Controls create issues. |

The way I think about it: a finding is a clue, and an issue is the crime scene all the clues point to.

### Finding Types
| Type | Source | Example |
|------|--------|---------|
| Cloud configuration finding | Failed cloud config rule | S3 bucket allows public access |
| Host configuration finding | Failed host config rule | SSH root login enabled |
| Vulnerability finding | Vuln scanner matched a CVE to a resource | OpenSSH CVE on EC2 |
| Security event finding | Threat detection rule / CSP security service | Unusual API call pattern |
| Excessive access finding | Unused permissions (90-day default) | User hasn't used IAM CreateRole in 90 days |
| Lateral movement finding | Graph traversal of privilege paths | VM can assume a role that has admin to S3 |
| Data finding | DSPM scan matched a classifier | Credit card data in a public S3 bucket |
| Secret instance | Workload scan found a hardcoded secret | AWS access key in /etc/config |
| Malware instance | Malware hash match | Ransomware hash found on an EC2 disk |

### How Issues Get Created
```
Controls (graph queries + severity) → run against graph → return results → Issues created
```
- Controls are attacker playbooks, known patterns of how attackers go after clouds.
- One control can create a bunch of issues (20 VMs that match the same rule = 20 issues).
- Wiz resolves issues automatically when a later scan shows the risk is fixed.
- Only issues from threat detection can be resolved by hand.

### Ignoring an Issue
1. Open the issue details drawer.
2. Status → Ignore
3. Pick a reason and add a comment.
4. The issue is silenced but still recorded.

### Context and Prioritization
Wiz might show 178,000 known vulnerabilities, but only 98 of them may be in a critical attack path. Context is what makes the difference. A vulnerable VM in dev with no internet exposure is low priority. A vulnerable VM in prod with internet exposure, admin privileges, and access to sensitive data is a critical issue.

### Network Exposure Analysis

Three layers of exposure:
1. Internet exposure (quad-zero, 0.0.0.0/0)
2. Cross-subscription access (reachable from another account)
3. VPN/private network access (reachable from corporate networks)

How effective exposure gets calculated: Wiz builds out the whole network architecture on the graph:
- Every NIC, subnet, VPC, load balancer, and internet gateway
- Security group rules (allow/deny), firewall rules, and proxy rules (load balancer listener + target group)
- The ingress path to every resource

The result is Wiz knows exactly which resources are exposed, to who, through which path, on which ports.

Application endpoint object: gets created when a resource is exposed to the whole internet (0.0.0.0/0) on at least one port. Its properties include:
- IP address + port combo
- Validated open ports (from the dynamic scanner)
- HTTP status code from the scanner
- A screenshot of what the dynamic scanner saw
- The authentication method it found (SSO, basic auth, Google/Okta/Microsoft)

Dynamic scanner: checks every so often that the calculated exposures are actually reachable. It uses a TCP three-way handshake, and for HTTP/HTTPS ports it sends a GET request and grabs the response and a screenshot. Runs every 7 days by default and needs a Wiz Advanced license.

Why the dynamic scanner matters: say a security group is open but the web server is stopped. Without the dynamic scanner, Wiz still says "internet exposed = true." With it, Wiz sees the port is closed, removes the application endpoint, and sets `wide_internet_exposure = false`. Way more accurate.

Application endpoint exposure policy: controls the severity of exposure findings.
- Moderate (default and recommended): basic auth = medium severity
- Permissive: any auth = low severity
- Strict: any exposure = high severity

---

## Cloud Entitlements

### What Wiz Analyzes
Wiz does effective permissions analysis, meaning it looks at what a principal can *actually* do after accounting for:
- Granted permissions
- Organization/account-level blocks (like AWS Service Control Policies)
- Resource-level restrictions

### What Is a Principal?
Anything that can access a resource: users, service accounts, groups, and predefined groups (like admin groups in the CSP's IAM).

### Three Permission Levels

Admin permissions:
- Can create, modify, delete, or assign identities
- OR has wildcard permissions on a subscription/account
- Kubernetes admin = wildcard on the *cluster* (not just a namespace)
- If a user has admin permissions BUT an SCP blocks them, Wiz does NOT mark them as admin.

High privileges:
- Can create/modify/delete/assign resources or sensitive configurations
- Can mess with the integrity of cloud workflows
- Kubernetes examples: code execution permissions, reading secrets, permissions that can disrupt workflows

Data access:
- Can read, write, or change data inside a cloud service
- Applied at the most granular level (like S3 `GetObject` = data access to individual objects in a bucket)

### Lateral Movement Findings
Wiz calculates possible paths from any resource to highly privileged principals, up to 10 hops. Hops can go through secrets, user accounts, service accounts, VMs, and K8s clusters.

Crown jewels (what lateral movement is going after):
- Admin principals
- Sensitive data (databases and buckets with PII/PHI/PCI)

### Excessive Access Findings
Wiz flags permissions that haven't been used in the last 90 days (you can change that). Where the data comes from:
- AWS: IAM Access Advisor
- GCP: IAM Recommender
- Azure: Azure cloud events

Wiz suggests a smaller policy that shows which permissions are actually being used and which ones you can remove.

### Where to Find Entitlement Data
- Cloud Entitlements page (Explorer → Cloud Entitlements): every identity with its access type, permissions, a visualization, and findings. Updated every 24 hours.
- Cloud Identities page (Inventory → Cloud Identities): finds inactive accounts, accounts without MFA, and developer identities across your VCS.
- Cloud Entitlements board: one place for all identity risk, with preset queries and columns you can customize.
- Reports: schedule automated entitlement reports (like "all identities with admin rights used in the last 90 days").

---

## Secrets

### Types of Secrets Wiz Detects
- Cloud encryption keys: AES-256 keys used to encrypt data at rest (stored in AWS Secrets Manager, Azure Key Vault, GCP Secret Manager)
- Cloud certificates: SSL/TLS certs used for secure communication
- Cloud access keys: a public access key ID plus a private secret access key for programmatic access (like AWS IAM keys)
- SSH keys: used by sysadmins to get into VMs, often stored on the local disk
- DB connection strings: server address, database name, and credentials an app uses to connect to a database
- Pre-signed URLs: temporary access links for cloud storage
- SaaS API keys: keys for third party tools (Datadog, Slack, LaunchDarkly, etc.)
- Weak or exposed passwords, git credentials, certificates, and public keys

### How Wiz Detects Secrets
1. The cloud connector, workload scanner, data scanner, and Wiz CLI each run a secrets search.
2. Known secret types are defined with regular expressions (regex), basically pattern matching.
3. Important: Wiz only stores metadata about the secret, NOT the secret itself. It shows a partially redacted sample.

### How Secrets Show Up on the Graph
- Secret (normalized term): the generic object for any type of secret.
- Secret Data object: the actual instance of the secret (like a specific public key).
- Secret Instance object: links the secret to the resource where it was found (like the VM).
- If the same key is found on 5 VMs, you get 5 Secret Instance objects pointing to the same Secret Data object.

### Why Exposed Secrets Are a Risk
- Lateral movement: attacker grabs a secret key, assumes a role, escalates privileges, and ends up with admin access.
- Data exposure: the secret gives access to sensitive data stores.
- HIPAA/PCI/GDPR violations: a lot of compliance frameworks require proper secret management.

### Where to Find Secrets in Wiz
- Secure Use of Secrets board
- Graph controls filtered by "insecure use of secrets"
- Cloud configuration rules → risk: insecure use of secrets
- Threat detection rules → risk: insecure use of secrets
- CI/CD policies: turn on secrets scanning at the code and build stages (NOT deploy, that's too late)

---

## Vulnerability Management

### Definitions
- Vulnerability: a weakness in software that can be exploited.
- CVE (Common Vulnerabilities and Exposures): a unique ID given to publicly disclosed vulnerabilities by the CVE program (sponsored by CISA).
- CVSS (Common Vulnerability Scoring System): a 0 to 10 severity score. Wiz uses the vendor severity over the NVD severity for vulnerability findings.
- KEV (Known Exploited Vulnerabilities): CISA's catalog of CVEs that are confirmed to be exploited in the wild. These are the top priority to patch.

### Wiz Vulnerability Coverage
- 120,000+ vulnerabilities detected
- Windows, macOS, and most Linux distros
- OS packages, code libraries (direct and transitive dependencies), and standalone apps
- Container images (by layer), serverless functions, and VMs

### Detection Methods
| Method | What It Scans | How |
|--------|--------------|-----|
| Package detection | OS native package manager | Matches package name + version to vendor feeds |
| Library detection | App files and installed libraries | Scans dependency files per language (requirements.txt, package.json, pom.xml, etc.) |
| File detection | System files | Vulnerabilities on specific files |
| OS detection | Windows KB updates, Linux kernel | Checks the vendor update stream for the kernel version |
| Hash-based (Java) | Java Archive (JAR) files | Compares the JAR hash to the Maven repository, so it catches renamed JARs |

### Vulnerability Catalog
- Updated at least daily (more often for high-priority events)
- Sources: NVD (National Vulnerability Database), CSP-specific databases, Exploit-DB, and product-specific advisories
- A newly added CVE takes 24 to 48 hours to create findings (it needs the next scan)
- Only high and critical CVEs and/or KEV (known exploited) CVEs go on the security graph. Everything else is only on the Vulnerability Findings page.

### Vulnerability Scanning Architecture
```
Cloud connector → API scan → metadata to Analysis Engine
Workload scanner → disk snapshot → Vulnerability Engine matches against catalog → findings generated
Registry connector → container image layers → same vulnerability engine
Wiz CLI → developer desktop or CI/CD pipeline → same engine
Wiz Sensor → runtime validation of vulnerabilities
```

### CPE (Common Platform Enumeration)
A standard ID for software and versions. Wiz uses CPE to match the software it finds to known vulnerabilities in NVD. Example: `cpe:2.3:a:haproxy:haproxy:2.4.0:*:*:*:*:*:*:*`

### Vulnerability Findings vs. Vulnerability Object
- Vulnerability object: general info about the CVE, like attack vector, exploitability, and the has_exploit flag.
- Vulnerability finding: the resource-specific instance, with the exact detection method, file location, and vendor severity vs. NVD severity.

---

## Malware

### How Wiz Detects Malware

Two methods:
1. Hash-based detection (through ReversingLabs): Wiz hashes every file on the disk and compares it to ReversingLabs' database of known malware hashes. The file itself is NOT sent, only the hash.
2. Pattern-based detection (Wiz YARA rules): YARA rules written by the Wiz research team that look for behavior patterns. These catch malware families that aren't in public hash databases (web shells, offensive security tools, crypto miners).

Wiz only creates malware issues at 50%+ confidence.

### Malware Types (Know These)
- Ransomware: encrypts files and holds them for ransom
- Rootkit: a set of tools that gives an attacker admin-level control
- Worm: copies itself and infects other computers
- Trojan: pretends to be legit software
- Backdoor: a hidden way back in
- Coin miner: cryptomining malware

### Graph Objects
- Malware object: general info about the malware family.
- Malware instance object: specific to the workload, including the file path where it was found.

### Malware Naming Convention
`[Platform].[Sub-Platform].[Type].[Name]`

Example: `Win32.Ransomware.Sodinokibi` means it targets 32-bit Windows, it's ransomware, and it's the Sodinokibi family.

### Detection Scope
- Workload scanner: every file on OS disks and non-OS disks (including ZIP, JAR, WAR, UPX, and PAR archives)
- Wiz Runtime Sensor: real-time detection on running workloads
- Buckets: only scanned if DSPM is turned on

### Custom Hash Detection
You can upload your own file hashes to detect:
- Settings → Scanners → Custom Detection
- Use cases: external threat intel feeds, or tracking your own files (like detecting classified files showing up where they shouldn't be)

### Malware Exclusion Rules
Rules that stop Wiz from creating malware findings on resources you know are safe:
- Scope by directory path, file extension, file name, project, resource, subscription, or resource tag
- Example: honeypot VMs that have malware on purpose. Exclude them so they don't keep alerting.

---

## DSPM

DSPM = Data Security Posture Management

### What It Is
Agentless, read-only scanning that gives you constant visibility into sensitive data across your cloud. It only samples, Wiz never stores the actual data.

### What Wiz Scans for Sensitive Data
- VM disk files (OS and non-OS volumes)
- Public and private buckets
- PaaS databases (AWS RDS, Azure SQL, GCP Cloud SQL)
- IaaS databases (MySQL, MariaDB, Postgres, MongoDB)
- Other databases and data warehouses (DynamoDB, Redshift, BigQuery, Snowflake)
- Serverless functions
- AI workloads (SageMaker, Bedrock, GCP Vertex AI)

Cloud only. No on-prem scanning.

### Sensitive Data Categories (Three Types)
1. Regulated personal data: PII, PHI, and financial data (regulated by HIPAA, GDPR, PCI DSS)
2. Secrets: credentials, API tokens, TLS certificates
3. Proprietary information: business plans, trade secrets, financials

### Data Classification Rules
- 100+ built-in rules (credit cards, SSNs, health IDs, passport numbers, email addresses, etc.)
- Custom classifiers come in two types:
  - Regex-based: looks through the data content for pattern matches.
  - Metadata-based: matches file characteristics (name, location, size, type).
- Rules are on by default, so turn off the ones that don't apply.

### Requirements to Turn On DSPM
1. A Wiz Cloud Advanced license
2. Turn on data scanning in Settings → Scanners → Data Security (toggle the scan types)
3. Turn on DSPM permissions in the cloud connector config

Public bucket scanning works without DSPM permissions (it uses the connector permissions you already have) and is on by default.

### DSPM Graph Objects
| Object | What It Represents |
|--------|-------------------|
| Data finding | A classification rule matched on a resource (PII, PCI, PHI) |
| Secret instance | A secret found on a resource |
| Data resource | Wiz's abstraction of any scannable data resource (bucket, DB, VM) |
| Data store | A collection of structured/unstructured data attached to a resource |
| Data schema | Structured data that was found (a DB table or JSON fields) |
| Data inventory | File list and detected content types |
| AI dataset | Training/validation data for AI models |
| AI model | The model itself (an LLM, a fine-tuned model) |

### Finding Severity
Based on two things:
1. The severity of the classification rule (credit card > zip code)
2. How often it shows up and how many unique matches there are (more unique matches = higher severity)

### Use Cases
1. Breach prevention: get rid of attack paths to sensitive data before someone uses them.
2. Data exfiltration detection: near-real-time correlation of CSP events and the Wiz sensor.
3. Data lineage: track how data spreads across environments and regions (big for GDPR, since data shouldn't end up in regions it's not allowed in).
4. Compliance automation: scans on a 24-hour cycle check all cloud configurations against data regulations.

### Data Leakage Risk Type
When CDR (Cloud Detection & Response) is on, Wiz can detect *active* data exfiltration attempts, not just unprotected data. That's the "data leakage" risk type:
- It combines a sensitive data finding with a near-real-time exfiltration event from GuardDuty, Macie, Sentinel, or the Wiz sensor.

---

## Policy Management

### Policy Hierarchy
```
Policies (rules) → generate Findings → Findings feed Controls (graph queries + severity) → Controls generate Issues
```

### Four Policy/Rule Types

Cloud Configuration Rules (CCR):
- Check cloud resource configurations using the JSON from the CSP.
- Powered by OPA (Open Policy Agent) and the Rego language.
- Use these when you need regex-based path checks, Kubernetes admission controller checks, or near-real-time config checks.
- Results go to the Cloud Configuration Findings page.

Host Configuration Rules (HCR):
- Check OS-level and app-level configs on workloads.
- Run during the workload scan (24-hour cycle or manual).
- Based on CIS benchmark OVAL (Open Vulnerability and Assessment Language) definitions.
- You can write your own HCR rules.
- Results go to the Host Configuration Findings page.

Data Classification Rules:
- Find sensitive data on storage resources and databases.
- Regex-based or metadata-based matching.
- Results go to the Data Findings page.

Threat Detection Rules (three subtypes):
- Cloud event rules: a single malicious event on the cloud control plane (like an external subscription doing something to a public S3 bucket).
- Workload runtime rules: need the Wiz sensor. They detect activity right on the workload in near real time.
- Correlation rules: malicious chains of events across multiple cloud events (like a bunch of failed logins followed by a successful login from a privileged user).

### Controls
- Core security graph queries plus a severity rating
- They turn attacker playbooks into code
- Run automatically after every scan update
- One control can create multiple issues (one per matching resource)
- You find them under Policies → Graph Controls

### Three Detection Layers (for prioritization)
1. Single event rules: real time, one malicious event, like talking to a known malicious IP.
2. Correlation rules: chains of events that point to an attack, so higher confidence.
3. Controls: full security graph context (blast radius, exposure, permissions), so the most context.

### Policy Tuning Options
- Ignore an issue: a documented exception. It shouldn't be standard practice, so always use a reason and an expiration date.
- Ignore a finding: per finding type (cloud config, host config, etc.).
- Malware exclusion rules: exclude specific hashes, paths, or resources from malware detection.
- Custom file detection: upload hashes to detect specific files you own.
- Ignore rules: suppress specific kinds of findings on specific resources. Be surgical, not broad.
- Dynamic scanner exposure policy: change the severity of application endpoint exposure (Moderate/Permissive/Strict).

Best practices for tuning:
- Be surgical and target specific findings and resources.
- Put expiration dates on ignore rules.
- Review ignored stuff on a regular schedule.

---

## Access, Authentication & Projects

### Projects
Projects are how Wiz splits up your cloud environment for different teams. They:
- Cut down on alert fatigue (teams only see issues for their own resources)
- Let you do role-based access at the resource level
- Can be scoped by cloud org, subscription, cluster, registry, or resource tags

Project hierarchy:
- Project folders can hold projects or other folders (max 2 folder levels).
- Each project can have one parent folder.
- Each folder can hold up to 5,000 child projects.
- Projects can be archived (kept) or deleted (you have to remove all the resources first).

Project inheritance: a user assigned to a folder gets access to every project in that folder and any child folders.

Risk profile metadata (the customer sets this, not Wiz):
- Business impact (high/medium/low)
- Internet facing?
- Regulatory requirements?
- Customer accessible?

### User Types

Local users:
- Managed by Wiz (backed by AWS Cognito)
- One role per user
- Use cases: POC/POV, break-glass accounts, backup admin

SSO users (federated):
- Connected through SAML 2.0
- Can have multiple roles (through SSO role mapping)
- Supported IdPs: Microsoft Entra ID, Okta, Ping, AWS IAM Identity Center, and any SAML 2.0 provider
- Roles get assigned at the SSO group mapping step

### Service Accounts
Used for API calls, automations, and third party integrations. Examples:
- Jira integration
- Slack notifications
- Wiz sensor deployment
- Wiz broker and admission controller
- Custom scripts using the GraphQL API

### RBAC (Role-Based Access Control)
- Predefined roles: Global Admin, Global Contributor, Project Member, Connector Admin, etc.
- Custom roles: you set the name, description, project scope, and API scope.
- API scopes decide exactly which API calls a role can make.

### SSO Setup Flow (SAML 2.0)
1. Add the identity provider in Wiz (Settings → Access Management → SSO).
2. Set up the SAML app in the IdP (map the ACS URL, audience, and attribute fields).
3. Bring the IdP metadata (sign-on URL, logout URL, certificate) into Wiz.
4. Set up group-to-role mappings.

---

## Integrations, Actions & Automations

### Three Pieces

Integration: the auth info Wiz needs to talk to a third party tool (URL plus credentials or tokens).

Action: what Wiz sends to the third party using the integration (like the JSON body for a new Jira ticket).

Automation rule: When + If + Then logic. Example: "When an issue is created, if the severity is critical, then create a Jira ticket."

### Integration Types
- Push: Wiz holds the credentials and pushes data to Jira, Slack, ServiceNow, etc.
- Pull: the third party holds Wiz service account credentials and pulls data from Wiz (SOAR, SIEM).
- Enrich: a third party tool (like BigID) pushes its findings into the Wiz graph.
- Export: Wiz exports issues, findings, and reports to S3, Snowflake, or GCP buckets for long-term storage.

One integration can be used by a lot of automation rules.

### Three Ways to Trigger an Action
1. Manual: from the Issues page, pick one issue and run the action.
2. Semi-automated (bulk): turn on multi-select on the Issues page, pick multiple issues/controls, and run the action on all of them.
3. Automation rule: set in Settings → Response & Automation. Condition-based, and it fires on its own. Automation rules don't apply retroactively though, only to new events after the rule exists.

### Jira Integration Tips
- Test the integration first (Settings → Integrations → test run).
- Get the project key from Jira (like "JAT").
- Uses the Mustache template language to customize ticket bodies.
- Make a Create rule for new issues and a separate Transition rule for resolved issues (so tickets close).
- Use bulk actions for existing issues, since automation only catches future ones.

### ServiceNow Vulnerability Response Integration
- Pulls vulnerability findings from Wiz (findings, not issues).
- Three jobs: (1) the first full sync, (2) daily new vulns, (3) daily resolved vulns.
- Recommended filter: critical and high only (unless the customer needs everything).
- Shows up in ServiceNow as detections (1:1 with the Wiz vulnerability findings page).

---

## Compliance

### What Compliance Means in Wiz
A point-in-time check of whether cloud resources follow industry standards, regulations, and internal policies, with continuous monitoring. Compliance doesn't always equal security, but it does show you're doing your due diligence.

### Framework Structure
```
Framework → Categories → Guidelines → Policies (controls/config rules)
```

### Two Guideline Types
- Benchmark guidelines: specific, prescriptive checks (CIS benchmarks, where almost everything can be checked).
- Non-restrictive guidelines: general principles, and some of them are outside what Wiz can check (like "contractors must have background checks").

### Compliance Scoring (Four Metrics)
1. Passed checks: categories where every resource passed every guideline. 7/28 means 7 categories had a 100% pass rate.
2. Compliance posture: total passed checks divided by total checks (passed + failed), as a percentage. Calculated per category, guideline, and policy.
3. Guideline score: every policy in a guideline has to pass before the guideline counts as passed.
4. Policy score: X of Y resources passed that specific policy check.

### Compliance Heat Map
Shows every framework against every project at once so you can spot which projects are failing which frameworks. Double-click a hotspot to drill in.

### Wiz Frameworks (Not Regulatory)
Wiz builds its own frameworks focused on preventing cloud threats and being ready for detection and response:
- Wiz for Risk Assessment: has controls that map to the built-in dashboards, so you can control which issues show up on which boards.
- Wiz for Cloud Native: cloud-specific threat prevention.

### Compliance Reports
- Can be scheduled (weekly, monthly, etc.)
- Export to email, S3, GCP/AWS buckets, or Snowflake
- Filter by framework, subscription, category, or status

### Slow Roll Strategy
For compliance teams drowning in findings: turn on a new framework with every policy disabled, then turn policies on one at a time. That way teams can deal with violations in a controlled way instead of all at once.

### CIS Certification
A CIS-certified Wiz framework means Wiz was verified to correctly check and report on that specific CIS benchmark version.

---

## Licensing & Workloads

### Two Licenses

Wiz Essentials:
- Immediate cloud visibility
- Prioritization with a lot of context
- More agility
- No DSPM (but some DSPM-like features)
- Best for small teams, early cloud adoption, and simple environments

Wiz Advanced: everything in Essentials, plus:
- Container registry scanning
- Admission controller support
- Attack path analysis
- Internal lateral movement detection
- CDR (Cloud Detection & Response) features
- Advanced integrations and auto-remediation
- Custom policy support
- Advanced detections (dangling DNS entries, unauthorized file changes, validated open ports)
- Wiz Outpost (Advanced only)
- Full DSPM

### Billing (Billable Workloads)

| Type | What Counts | License |
|------|------------|---------|
| Compute | VMs, containers, serverless (50 functions = 1 workload) | Both |
| Data workloads | Buckets, non-OS volumes, databases | Advanced only |
| Runtime sensors | Wiz sensor deployments | Advanced only |

- VMs and containers each count as 1 workload.
- 50 serverless functions = 1 workload.
- 10 serverless containers = 1 workload.
- A VM plus a container running on it = counted twice (they're separate resources).
- Billing is the monthly average of the daily workload counts.

---

## Wiz Code (Shift Left)

### The Problem Wiz Code Solves
Traditional cloud security starts once code is deployed. Attackers are going after stuff before that now:
- Source code repositories (VCS)
- CI/CD pipelines
- Developer credentials and secrets in code
- Third party library dependencies (supply chain attacks)
- Container images before they're deployed

Shift left = catch security issues at the *code* stage, not in production.

### Wiz Code Architecture
Wiz covers every stage of the SDLC:

```
Code (IDE + VCS) → Build (CI/CD pipelines) → Deploy (registries, admission controller) → Runtime (Wiz Sensor)
```

### What Wiz Code Scans For
- Vulnerabilities in code libraries and dependencies (SAST + SCA)
- Secrets: hardcoded credentials, API keys, tokens in code
- IaC misconfigurations: Terraform, CloudFormation, Docker, all scanned before deployment
- Sensitive data in code and repos
- Supply chain integrity: container image signing validation (cosign, Notary v2)

### Tools and Integrations
- Wiz CLI: a small executable that runs on a developer's machine or in a pipeline. Scans container images, VM images, IaC files, and directories.
- IDE integration (VS Code): instant feedback on vulnerabilities without leaving the editor.
- VCS integration (GitHub, GitLab, etc.): scans pull/merge requests and can block PRs with critical findings.
- Admission controller: checks container images at deploy time before they run in Kubernetes.

### CI/CD Policy Stages
- Code stage: vulnerabilities, secrets, IaC config, sensitive data
- Build stage: everything in the code stage plus host configuration
- Deploy stage: IaC configuration and image trust only

### Policy Actions
- Audit: notify but don't block
- Block: stop the pipeline or the PR merge

### Default Policies
- Vulnerabilities: block on critical severity when a fix is available
- Secrets: audit, threshold = informational (notify but don't block)
- IaC config: audit on critical
- Sensitive data: audit only
- Image trust: block if it's not signed with cosign/Notary v2

### Exception Management
Ways to ignore findings in code (should be temporary and documented):
- Inline code comments: ignore a specific file, block, or line.
- A `.wiz` file in the repo root: ignore by CVE ID, file path, or directory.
- PR/MR comments: `#wiz-ignore reason:false-positive`
- Block PR label: skips the whole check (it gets noted, but it's not an ignore rule).

Security teams can turn these exception options off per VCS connector to fully enforce policies.

---

## Wiz Defend (CDR & Threat Detection)

### What Wiz Defend Is
Wiz Defend is Cloud Detection and Response (CDR), the runtime threat detection and investigation part of Wiz. It came out of Wiz buying Gem Security in April 2024. It's built for the security operations team (SOC analysts, threat hunters, incident responders).

### Four Pillars of Defend

1. Prepare (incident readiness)
    - Incident readiness score that tracks your posture over time
    - Sensor coverage metrics across K8s clusters, Linux VMs, Fargate, etc.
    - Log configuration breakdown: are you collecting the right logs? (CloudTrail, VPC flow, S3 data events, DNS, etc.)
    - MITRE ATT&CK for Cloud mapping: shows which tactics and techniques you can detect and which ones you're missing
    - Remediation guidance in Terraform or other IaC formats

2. Detect (detection pipeline)

    Data sources it ingests:

    - AWS CloudTrail (read and write events)
    - VPC flow logs, S3 data events
    - Azure activity/storage logs, Key Vault logs
    - GCP audit logs
    - CrowdStrike, SentinelOne (EDR platforms)
    - Okta identity logs
    - GitHub/GitLab audit logs
    - Wiz runtime sensor events

    Detection features:

    - Behavioral baselines: models normal behavior for every entity, so it can tell business-as-usual (a CI pipeline enumerating stuff) apart from a threat actor enumerating stuff.
    - Smart grouping (automated correlation): groups related detections into one *threat* that tells the attack story as it happens.

3. Investigate (investigation graph)

    Similar to the security graph, but it shows the attack *timeline* instead of attack paths:

    - Initial access point
    - Processes spawned
    - Lateral movement events
    - Data accessed or exfiltrated
    - All of it across multiple signal sources (sensor + CloudTrail + S3 data events + GuardDuty)

4. Respond (response guidance)
    - Recommended actions (call the developer, kill the process, revoke credentials)
    - Cloud-native playbooks
    - Cuts response time from hours or days down to minutes

### Threat Object
The new work item for SOC teams in Wiz Defend. A threat:
- Groups correlated detections together
- Keeps growing (new activity gets added as the attack moves along)
- Shows the MITRE ATT&CK tactics and techniques
- Shows every event source that contributed to it

### Wiz Sensor
An eBPF-based runtime sensor you can deploy on Kubernetes clusters and Linux VMs. It gives you:
- Real-time process monitoring
- Network connection tracking
- File system activity
- Continuous workload telemetry
- The data behind workload runtime detection rules

---

## Quick Glossary

| Term | Definition |
|------|-----------|
| Agentless | Scanning that doesn't need software (agents) installed on the target. Uses APIs or snapshots. |
| Application Endpoint | Wiz object created when a resource is exposed to 0.0.0.0/0 on at least one port. |
| Blast Radius | How much damage an attacker could do if they compromised a specific resource. |
| CCR | Cloud Configuration Rule. A policy check against a cloud resource's JSON config. |
| CDR | Cloud Detection & Response. Runtime threat detection, part of Wiz Defend. |
| CNAPP | Cloud-Native Application Protection Platform. Unified security for cloud apps from code to runtime. Wiz IS a CNAPP. |
| Control | Security graph query + severity rating. Turns an attacker playbook into a query. Creates issues. |
| CVE | Common Vulnerabilities and Exposures. A unique ID for a publicly disclosed vulnerability. |
| CVSS | Common Vulnerability Scoring System. 0 to 10 score. Wiz uses vendor severity over NVD. |
| Dynamic Scanner | Wiz module that checks network exposure by actually trying TCP connections to exposed ports. Needs an Advanced license. |
| eBPF | Extended Berkeley Packet Filter. Kernel technology the Wiz sensor uses for low-overhead runtime monitoring. |
| Effective Permissions | What a principal can *actually* do, after counting all grants, blocks, and boundary policies. |
| Enrichment | Adding derived knowledge (exposure, lateral movement, effective permissions) to the graph after discovery. |
| Eventually Consistent | Wiz's architecture model. Components process data asynchronously, and the graph becomes consistent over time. |
| Finding | A specific weakness on a specific resource. One data point. NOT the same as an issue. |
| HCR | Host Configuration Rule. A policy check against OS/app configuration on a workload. |
| Issue | A toxic combination of findings that's a real, prioritized risk. Created by controls. |
| KEV | Known Exploited Vulnerabilities. CISA's catalog of CVEs with confirmed real-world exploits. Top priority. |
| Lateral Movement | An attacker moving from one resource to another after getting initial access. |
| OPA | Open Policy Agent. Open-source policy engine that runs CCR policies (Rego language). |
| OVAL | Open Vulnerability and Assessment Language. Used to define HCR check logic. |
| Principal | Anything that can access a resource: user, service account, group, predefined group. |
| Project | Wiz's way of dividing cloud resources for team-based access and alerting. |
| Rego | The policy language used with OPA to write cloud configuration rules. |
| Security Graph | The graph database at the core of Wiz. Stores everything discovered and derived. Every query and control runs on it. |
| Subscription | Wiz's normalized term for an AWS Account, Azure Subscription, GCP Project, OCI Compartment, or Alibaba Account. |
| Toxic Combination | Multiple findings across risk domains that together are a real risk (an attack path). What Wiz issues represent. |
| Wiz CLI | Small command-line tool for shift-left scanning on local machines and in CI/CD pipelines. |
| Wiz Outpost | Workload scanning inside the customer's own tenant. Only metadata leaves the customer environment. |
| Wiz Sensor | eBPF-based runtime agent for real-time workload monitoring and threat detection. |
| YARA | Pattern-matching language used for malware detection based on behavior patterns, not just hashes. |
| Zero-Copy | How Wiz scans workloads. The snapshot gets mounted (not copied) to the scanner, scanned, then deleted. |

---

*Last updated: April 2026 | Based on Wiz Technical Essentials, Managing Cloud Security Posture, Securing Cloud Development, and Wiz Defend training*
