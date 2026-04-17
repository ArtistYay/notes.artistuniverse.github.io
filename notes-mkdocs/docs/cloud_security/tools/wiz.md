---
tags:
  - Cybersecurity
  - Cloud
---

## Why Wiz Exists

### The Problem Wiz Solves
Before Wiz, answering a simple question — "Do I have any databases with sensitive data accessible to the public internet?" — was nearly impossible. Here's why:

- **Cloud complexity**: Multiple providers, thousands of technologies, exponential growth
- **Siloed tools**: Each security tool (CSPM, CIEM, CWPP, DSPM) generated findings in isolation with no shared context
- **Alert fatigue**: No correlation between findings = too many alerts, no prioritization
- **Agent dependency**: Most tools required agents deployed on workloads, which slowed deployment and left gaps
- **Shared responsibility confusion**: Customers didn't fully understand what *they* were responsible for securing

### The Shared Responsibility Model
- **IaaS (VMs)**: Customer is responsible for OS, apps, network config
- **PaaS**: Cloud provider handles more; customer still responsible for their data and apps
- **SaaS**: Provider handles almost everything; customer handles access and data governance

### What Wiz Delivers Instead
- **Complete agentless scan** of every cloud resource via APIs — no agents, no network changes
- **Deep assessment** across vulnerabilities, misconfigurations, identities, secrets, lateral movement paths
- **Toxic combination detection** — correlates findings across domains into prioritized issues
- **Single pane of glass** across AWS, Azure, GCP, OCI, Kubernetes, and VMware
- **Remediation guidance** with business context, delivered to the right teams via JIRA, Slack, ServiceNow

### Three Success Criteria
1. **Accuracy** — reduce noise, eliminate false positives
2. **Speed and Scale** — enterprise-ready, deploys in minutes at any scale
3. **User Perspective** — meets each team (security, DevOps, developers) where they are

---

## First-Gen Tools

These are the **siloed** point solutions Wiz consolidates or replaces. Know these cold.

| Acronym | Full Name | What It Does | Shortcoming |
|---------|-----------|--------------|-------------|
| **CSPM** | Cloud Security Posture Management | Scans cloud services for misconfiguration. API-based. | Only sees cloud config — no vuln or identity context. Siloed. |
| **CIEM** | Cloud Infrastructure Entitlements Management | Manages access rights and permissions across cloud identities | No blast radius context. Siloed. |
| **CWPP** | Cloud Workload Protection Platform | Protects workloads — intrusion detection, vuln scanning, behavior monitoring. Agent-based. | Agent-based. Siloed. |
| **DSPM** | Data Security Posture Management | Identifies sensitive data (PII, PHI, financial) in storage | Agent-based. Siloed. |
| **KSPM** | Kubernetes Security Posture Management | Scans K8s for misconfiguration. API-based. | Architecture-specific. Siloed. |
| **SASE** | Secure Access Service Edge | Cloud-hosted firewall/gateway, inspects traffic, detects intrusion | Inspects traffic only — can't see workload internals. |
| **CASB** | Cloud Access Security Broker | Ensures authorized access, monitors suspicious activity, enforces policies on SaaS | SaaS-only. Limited visibility. Siloed. |
| **SSPM** | Secure Serverless Platform Management | Security for serverless platforms — access controls, monitoring | Architecture-specific. Siloed. |

**Key takeaway**: All these tools have limited visibility and no context sharing. Wiz replaces or consolidates them into one unified security graph.

---

## Architecture

### Design Principles
- **Eventually consistent**: Components operate independently and asynchronously. Data converges on the graph over time. Performance and availability are prioritized over immediate consistency.
- **Asynchronous**: Microservice, containerized architecture. Services communicate via message queues. Enables parallel processing and fault tolerance.
- **Resilient**: Uses cloud availability zones, load balancing, auto-scaling, multi-region replication. Immutable images. Stateless nodes.

### Deployment Model (SaaS)
All services run in Wiz-managed tenants. Simplest and most common. Wiz holds SOC 2 Type 2, ISO 27001, PCI, HIPAA certifications.

### Six Phases of Data Flow

```
Phase 1: CONNECT      → API connection to cloud (agentless, no network changes)
Phase 2: SCAN         → Cloud Scanner (API) + Workload/Volume Scanner (snapshot)
Phase 3: ENRICH       → Vulnerabilities, patches, configs, IAM, secrets, lateral movement
Phase 4: REFINE       → Validate findings, reduce false positives
Phase 5: ANALYZE      → Build the security graph, identify toxic combinations, prioritize
Phase 6: AUTOMATE     → Push remediation guidance to JIRA, Slack, ServiceNow, etc.
```

### Key Architecture Components
- **Cloud Scanner (fetcher)**: Makes read-only API calls. Gets inventory, configs, network, identity, audit logs.
- **Workload/Volume Scanner**: Snapshots OS disks and scans them. Runs in a dedicated Wiz account *in the same region* as the customer. Zero-copy — mounts, scans, deletes.
- **Analysis Engine**: Kubernetes cluster in Wiz backend. Runs enrichment, calculates exposure, runs controls.
- **Security Graph**: Graph database (AWS Neptune + Postgres for non-normalized data). All results written here.
- **GraphQL API**: Only ingress into the Wiz platform. Authentication via AWS Cognito tokens.

### Authentication Model
- Single ingress point: GraphQL API
- Auth via AWS Cognito refresh token
- No web server — single-page app making GraphQL queries

---

## Security Graph

### What It Is
The security graph is **two things simultaneously**:
1. A **graph database** running in the Wiz backend (stores all discovered and derived knowledge)
2. A **query interface** in the Wiz portal (where you run queries and visualize results)

### Three Roles of the Graph
1. **Knowledge representation**: Stores discovered inventory + derived enrichments (lateral movement, blast radius, exposure paths)
2. **Enrichment input**: API scan data + workload scan data feeds enrichment engines, results go back to graph
3. **Query foundation**: All controls, issue detection, and custom queries run against the graph

### Key Attributes
- **Alive**: Constantly updated by background microservices. Not static.
- **Normalized**: Cloud-specific terms are mapped to Wiz terms. Example: AWS EC2, Azure Compute, GCP Compute Instance → all called "Virtual Machine" in Wiz. This allows cloud-agnostic queries.

### Why a Graph Database?
A graph DB stores interconnected data as **nodes** (resources) and **edges** (relationships). Perfect for questions like "find VMs with critical vulnerabilities that are internet-exposed and have admin privileges." Querying relationships is what makes toxic combination detection possible.

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
- **Scheduled**: Once per day per connector
- **Event-based**: When a resource is created, deleted, started, or stopped
- **Ongoing enrichment**: Vulnerability checks, patch assessments, technology updates

### Query Structure
- **Root**: First node in the query — the focal point
- **Condition**: Where clause — filters by property values
- **Clause**: Further narrows conditions (using `that` statements)
- **Properties**: Attributes that restrict/filter a node
- **Results**: Found instances matching the query

### Controls
Controls = **saved security graph queries + a severity rating**. They codify attacker playbooks. When a control matches resources in your environment, it generates **issues**.

---

## Cloud Scanner

Also called the **cloud fetcher** or **API scanner**.

### What It Does
Makes read-only API calls (GET, LIST, DESCRIBE) to cloud provider APIs. Collects:
- Resource inventory (VMs, buckets, databases, etc.)
- Network configuration
- Identity/IAM data
- Cloud audit logs
- Advanced resource parameters

### How It Works
- **Connector Operator**: Orchestrates timing and scheduling of scans
- **Cloud Platform Fetcher**: One pod per subscription. Up to 20 pods run in parallel.
- Pushes results to enrichers and the workload scanner (as a list of volume IDs to scan)

### Connector Types
| Level | What It Covers | Recommendation |
|-------|---------------|----------------|
| **Organization level** | Entire cloud org — auto-discovers new subscriptions | ✅ Recommended |
| **Subscription level** | Single account/subscription/project | ⚠️ Leaves blind spots |

### Normalized Terminology
| Wiz Term | AWS | Azure | GCP |
|----------|-----|-------|-----|
| Cloud Organization | Organization | Root Management Group | Organization |
| Subscription | Account | Subscription | Project |
| Resource Group | — | Resource Groups | — |

### Scanning Frequency
- Full cloud scan: Once per day
- **Event-triggered scanning**: Create/update/delete events kick off a targeted rescan of affected resources between full scans
- On-demand rescan: Users can trigger manually by connector, subscription, or individual resource

### Graph Timestamps
- **Creation date**: When the resource was created in the cloud
- **First seen**: When Wiz first detected it
- **Last changed**: When Wiz last modified its graph properties (can be after last seen due to async enrichments)
- **Last seen**: Last time the cloud scanner detected it

### Double Scanning
When two connectors overlap (e.g., one org-level + one subscription-level covering the same subscription), the same subscription gets scanned twice. The graph does NOT duplicate resources, but it wastes compute and can affect resource counts. Avoid it.

---

## Workload Scanner

Also called the **disk scanner** or **volume scanner**.

### What It Is
An agentless service that creates a **snapshot** of a workload's OS disk, mounts it read-only, scans it, then **deletes** it. No agents. No network changes. Zero impact on production.

### What It Detects
From OS disks:
- Installed packages and versions (Linux: package manager; Windows: installed programs, services, hotfixes)
- Operating system metadata (type, build version)
- Running containers
- Local users and auth config
- **Vulnerabilities**
- **Secrets** (hardcoded credentials, API keys, tokens)
- **Malware** (via file hash comparison + YARA rules)
- Host configuration compliance (CIS benchmarks)
- Forensics data

### Zero-Copy Architecture
Wiz never copies the snapshot across regions or networks. The scanner cluster (in the same cloud + region as the customer) **mounts the snapshot as a read-only volume**. Scan → delete. Typically under 10 minutes.

### High-Level Steps
1. Cloud scanner sends list of volume IDs to workload scanner
2. Workload scanner creates a snapshot in the customer account
3. Snapshot is shared with the Wiz scanner cluster (same region)
4. Scanner mounts snapshot, scans it, extracts metadata
5. Metadata (not raw data) sent to Wiz backend
6. Snapshot is deleted (tagged `wiz-auto-gen-snapshot` for easy identification)

### Regional Isolation
Workload scans always happen **in the same region** as the customer's workloads. This ensures:
- Data sovereignty compliance
- Better performance and scaling
- Avoids data crossing regional boundaries

### Encrypted Disk Handling (AWS)
Uses **re-encrypt** permission: AWS decrypts the snapshot with the customer key, then re-encrypts it with a Wiz key. Wiz never sees the customer key.

### Inactive Workloads
Wiz scans both active AND inactive workloads because:
- A machine off today can be turned on with new vulnerabilities discovered while it was dormant
- Infrastructure changes (new exposure paths, security group changes) may have made it unsafe to restart
- Attackers can snapshot inactive machines the same way Wiz does

### Security Tool Scan Object
When a workload is scanned, Wiz creates a `security_tool_scan` object on the graph attached to the resource. Use this to verify scan status, check for errors, and monitor scan history.

---

## Wiz Outpost

### What It Is
An **in-customer-tenant** deployment model where the workload scanning infrastructure runs **inside the customer's cloud**, not Wiz's. Only metadata (scan results) leaves the customer environment — never raw disk data.

### When to Use Outpost
- Highly regulated industries (financial services, defense, pharma)
- Non-internet-facing private resources (requires network peering or private endpoints)
- Sovereign clouds (Azure China, AWS China, GovCloud)

### Three Outpost Types
| Type | Description | Who Controls |
|------|-------------|-------------|
| **Wiz Automated Outpost** | Fully automated — Wiz manages cluster, scaling, network | Wiz manages everything |
| **Self-Managed Network Outpost (BYOK)** | Customer provides network; Wiz deploys clusters within it | Customer manages network |
| **Self-Managed Outpost** | Customer owns everything — images, deployment, maintenance | Customer manages all |

90% of use cases use the Wiz Automated Outpost.

### Outpost Components (All 5 Present in Every Deployment)
1. **State bucket**: Holds Helm charts and configs for workloads on K8s clusters
2. **Principles**: IAM roles (AWS), enterprise app/service principals (Azure), managed service accounts (GCP)
3. **Queue**: Volume IDs flow through here — SQS (AWS), Service Bus (Azure), Pub/Sub (GCP)
4. **Clusters**: K8s clusters (EKS, AKS, GKE) where scanning happens
5. **Secrets**: Stored in AWS Secrets Manager, Azure Key Vault, GCP Secret Manager

### Key Principle Scopes
- **Read Only**: Powers the connector — reads cloud inventory
- **Orchestrator**: Builds the cluster, VNets, and scanning resources
- **Worker**: Handles scaling and cluster management
- **Scanner**: Creates and manages snapshots/clones for scanning

### Outpost vs SaaS Scanning
Both are nearly identical. The only difference: the scanner account moves from a **Wiz-owned trusted account** (SaaS) to an **account within the customer's cloud** (Outpost). In both cases, only metadata leaves — never raw snapshot data.

---

## Boards, Threat Center & Inventory

### Boards (Dashboards)
Boards are visual summaries of issues, organized by risk domain (external exposure, entitlements, secrets, vulnerabilities, etc.).

**Key Board Types:**
- **Overview**: Default landing page. Shows total issue counts, trends, burn-down rate, compliance score, top issues.
- **Managed by Wiz**: Built-in boards per risk domain. Cannot edit, but can be cloned.
- **Private boards**: User-created. Only visible to creator until shared.
- **Shared boards**: Custom boards shared at project, global, or org level.
- **Champion Center / Journey Center**: Onboarding progress tracker — shows how much of Wiz is enabled.

**Key KPIs on Overview Board:**
- Issue count by severity (critical/high/medium/low) with trend vs. last week
- Average issue age (vs. SLA)
- Burn-down rate: are issues being resolved faster than they're created? (want fixed > found)
- Compliance score by framework (PCI, SOC 2, NIST, etc.)
- Projects with most issues

**Board Access Control:**
- Private → only creator
- Project → members of that project
- Global users → anyone with a global role
- Organizational → all users

**Creating Custom Widgets:**
Start from Issues page, Security Graph, Technologies, Vulnerabilities, or Control drawer → filter to what you need → Save as board widget.

### Threat Center
A **Wiz-maintained news feed** of cloud-focused threats (not a generic threat database). Powered by the Wiz Threat Research team.

**What It Answers:**
- "Am I affected by this threat?"
- "What is it?"
- "Is it a problem for my cloud?"

**Threat Icons:**
- 🔴 Red exclamation = finding or issue detected in YOUR environment
- 🟠 Orange exclamation = mitigation is outside Wiz (CSP-level threat)
- ✅ Green check = threat exists but NOT found in your environment
- 🔵 Blue eye = informational only (already mitigated by CSP)

**Coverage:**
- Goes back to February 2021 (SolarWinds)
- New threats added within 24 hours of publication (Wiz added Log4Shell 8 hours after CVE publication)
- Focus is **cloud-specific threats** — APIs, libraries, CSP platform services, Kubernetes

**Automation:**
Set up automation rules so when a new threat creates an issue matching "high profile threat" risk category → trigger JIRA ticket, Slack message, email.

### Inventory (Technologies Page)
Shows all technologies detected across all connected clouds — cloud services, OS packages, libraries, SaaS resources.

**Coverage Status:**
- **Supported (Full Coverage)**: Technology is fully normalized and assessed for risk
- **Partial Coverage**: Technology detected but not yet normalized — shows bleeding-edge/shadow IT

**Technology Types:**
- **Hosted Technology**: Found on a workload (VM, container, serverless) — customer is responsible for patching/upgrading
- **Non-Hosted Technology**: Cloud service not running on customer-managed compute (e.g., managed database) — third party is responsible for patching

**Shadow IT Management Workflow:**
Status options: `Unreviewed` (default) → `Approved`, `Required`, `Unwanted`
- Automation rule: if an Unwanted technology is detected → send alert
- Example: Flag any new Windows Server 2008 deployment as Unwanted → auto-alert when someone spins one up

**Key Use Cases:**
- Comprehensive visibility across clouds
- Multi-cloud inventory management
- Detect workloads without required agents
- Lifecycle, version, and patch management
- Shadow IT governance

---

## Issues, Findings & Network Exposure

### Findings vs. Issues — The Critical Distinction

| Term | Definition |
|------|-----------|
| **Finding** | A weakness or compromisable aspect of a specific resource. Single data point. Example: "This VM has CVE-2024-1234" or "This bucket allows public access." |
| **Issue** | A **toxic combination** — multiple findings across risk domains that together represent a real, prioritized risk. Issues are generated by **controls**. |

**Analogy**: A finding is a clue. An issue is the crime scene that multiple clues point to.

### Finding Types
| Type | Source | Example |
|------|--------|---------|
| **Cloud configuration finding** | Failed cloud config rule | S3 bucket allows public access |
| **Host configuration finding** | Failed host config rule | SSH root login enabled |
| **Vulnerability finding** | Vuln scanner matched CVE to resource | OpenSSH CVE on EC2 |
| **Security event finding** | Threat detection rule / CSP security service | Unusual API call pattern |
| **Excessive access finding** | Unused permissions (90-day default) | User hasn't used IAM CreateRole in 90 days |
| **Lateral movement finding** | Graph traversal of privilege paths | VM can assume role that has admin to S3 |
| **Data finding** | DSPM scan matched classifier | Credit card data in public S3 bucket |
| **Secret instance** | Workload scan found hardcoded secret | AWS access key in /etc/config |
| **Malware instance** | Malware hash match | Ransomware hash found on EC2 disk |

### How Issues Are Generated
```
Controls (graph queries + severity) → run against graph → return results → Issues created
```
- Controls represent **attacker playbooks** — known patterns of how attackers exploit clouds
- A single control can generate multiple issues (e.g., 20 VMs all matching the same rule = 20 issues)
- Issues are automatically resolved by Wiz when a later scan shows the risk is remediated
- Only threat-detection-generated issues can be **manually** resolved

### Ignoring an Issue
1. Open issue details drawer
2. Status → Ignore
3. Select a reason + add comment
4. Issue is silenced but recorded

### Context and Prioritization
Wiz provides 178,000 known vulnerabilities — but only 98 may be in a critical attack path. **Context is the differentiator.** A vulnerable VM in dev with no internet exposure is low priority. A vulnerable VM in prod with internet exposure, admin privileges, and access to sensitive data is a critical issue.

### Network Exposure Analysis

**Three Layers of Exposure:**
1. Internet exposure (quad-zero / 0.0.0.0/0)
2. Cross-subscription access (accessible from another account)
3. VPN/private network access (accessible from corporate networks)

**How Effective Exposure Is Calculated:**
Wiz builds the full network architecture on the graph:
- All NICs, subnets, VPCs, load balancers, internet gateways
- Security group rules (allow/deny), firewall rules, proxy rules (load balancer listener + target group)
- Calculates ingress path to every resource

Result: Wiz knows exactly which resources are exposed, to whom, through which path, on which ports.

**Application Endpoint Object:**
Created when a resource is exposed to the full internet (0.0.0.0/0) on at least one port. Properties:
- IP address + port combination
- Validated open ports (via dynamic scanner)
- HTTP status code from the scanner
- Screenshot of what the dynamic scanner saw
- Authentication method detected (SSO, basic auth, Google/Okta/Microsoft)

**Dynamic Scanner:**
Periodically validates that calculated exposures are actually reachable. Uses TCP three-way handshake. For HTTP/HTTPS ports, sends GET request and captures response + screenshot. Runs every 7 days by default. Requires Wiz Advanced license.

**Why Dynamic Scanner Matters:**
If a security group is open but the web server is stopped, without the dynamic scanner, Wiz still shows "internet exposed = true." WITH the dynamic scanner, it validates the port is closed, removes the application endpoint, and sets `wide_internet_exposure = false`. More accurate.

**Application Endpoint Exposure Policy:**
Controls the severity of exposure-related findings:
- **Moderate** (default/recommended): Basic auth = medium severity
- **Permissive**: Any auth = low severity
- **Strict**: Any exposure = high severity

---

## Cloud Entitlements

### What Wiz Analyzes
Wiz performs **effective permissions analysis** — meaning it looks at what a principal can *actually* do, accounting for:
- Granted permissions
- Organizational/account-level blocks (like AWS Service Control Policies)
- Resource-level restrictions

### What Is a Principal?
Any entity that can access a resource: users, service accounts, groups, predefined groups (like admin groups in CSP IAM).

### Three Permission Levels

**Admin Permissions:**
- Allow creation, modification, deletion, or assignment of identities
- OR wildcard permissions on a subscription/account
- Kubernetes admin = wildcard on the *cluster* (not just a namespace)
- Note: If a user has admin permissions BUT an SCP blocks them → Wiz does NOT mark them as admin

**High Privileges:**
- Can create/modify/delete/assign resources or sensitive configurations
- Can disrupt the integrity of cloud workflows
- Kubernetes examples: code execution permissions, reading secrets, workflow disruption permissions

**Data Access:**
- Can read, write, or manipulate data within a cloud service
- Applied at the most granular level (e.g., S3 `GetObject` = data access to individual objects in a bucket)

### Lateral Movement Findings
Wiz calculates potential paths from any resource to highly privileged principals, within 10 hops. Hops include: secrets → user accounts → service accounts → VMs → K8s clusters.

**Crown Jewels** (what lateral movement targets):
- Admin principals
- Sensitive data (databases, buckets with PII/PHI/PCI)

### Excessive Access Findings
Wiz flags permissions not used in the last **90 days** (configurable). Sources:
- AWS: IAM Access Advisor
- GCP: IAM Recommender
- Azure: Azure Cloud Events

Wiz recommends a reduced policy — shows what permissions are actually being used and what can be removed.

### Where to Find Entitlement Data
- **Cloud Entitlements page** (Explorer → Cloud Entitlements): All identities with their access type, permissions, visualization, and findings. Updated every 24 hours.
- **Cloud Identities page** (Inventory → Cloud Identities): Detects inactive accounts, accounts without MFA, developer identities across VCS.
- **Cloud Entitlements Board**: Single pane for all identity risk — preset queries, customizable columns.
- **Reports**: Schedule automated cloud entitlement reports (e.g., "all identities with admin rights used in last 90 days").

---

## Secrets

### Types of Secrets Wiz Detects
- **Cloud encryption keys**: AES-256 keys used to encrypt data at rest (stored in AWS Secrets Manager, Azure Key Vault, GCP Secret Manager)
- **Cloud certificates**: SSL/TLS certs used for secure communication
- **Cloud access keys**: Public access key ID + private secret access key for programmatic access (e.g., AWS IAM keys)
- **SSH keys**: Used by system administrators for VM access, often stored on local disk
- **DB connection strings**: Server address, database name, credentials for app-to-database connections
- **Pre-signed URLs**: Temporary secure access tokens for cloud storage
- **SaaS API keys**: Keys for third-party tools (Datadog, Slack, LaunchDarkly, etc.)
- **Weak/exposed passwords**, git credentials, certificates, public keys

### How Wiz Detects Secrets
1. Cloud connector, workload scanner, data scanner, and Wiz CLI each trigger a secrets search
2. Known secret types are defined by **regular expressions (regex)** — pattern matching
3. **Important**: Wiz stores only **metadata** about the secret, NOT the secret itself. It shows a partially redacted sample.

### Security Graph Representation
- **Secret (normalized term)**: The generic object representing any secret type
- **Secret Data object**: The actual instance of the secret (e.g., a specific public key)
- **Secret Instance object**: Links the secret to the resource where it was found (e.g., the VM it was found on)
- If the same key is found on 5 VMs → 5 Secret Instance objects pointing to the same Secret Data object

### Risk of Exposed Secrets
- **Lateral movement**: Attacker gets a secret key → assumes a role → escalates privileges → admin access
- **Data exposure**: Secret enables access to sensitive data stores
- **HIPAA/PCI/GDPR violations**: Many compliance frameworks mandate secret management

### Where to Find Secrets in Wiz
- Secure Use of Secrets board
- Graph controls filtered by "insecure use of secrets"
- Cloud configuration rules → risk: insecure use of secrets
- Threat detection rules → risk: insecure use of secrets
- CI/CD policies → enable secrets scanning at code and build stages (NOT deploy — too late by then)

---

## Vulnerability Management

### Key Definitions
- **Vulnerability**: A weakness in software/application that can be exploited
- **CVE** (Common Vulnerabilities and Exposures): Unique identifier assigned to publicly disclosed vulnerabilities by the CVE program (sponsored by CISA)
- **CVSS** (Common Vulnerability Scoring System): 0–10 severity score for vulnerabilities. Wiz uses **vendor severity over NVD severity** for vulnerability findings.
- **KEV** (Known Exploited Vulnerabilities): CISA's catalog of CVEs with confirmed exploits in the wild — highest priority to patch

### Wiz Vulnerability Coverage
- 120,000+ vulnerabilities detected
- Windows, macOS, and most Linux distributions
- OS packages, code libraries (direct and transitive dependencies), standalone applications
- Container images (by layer), serverless functions, VMs

### Detection Methods
| Method | What It Scans | How |
|--------|--------------|-----|
| **Package detection** | OS native package manager | Matches package name + version to vendor feeds |
| **Library detection** | Application files and installed libraries | Scans dependency files per language (requirements.txt, package.json, pom.xml, etc.) |
| **File detection** | System files | Vulnerability on specific files |
| **OS detection** | Windows KB updates, Linux kernel | Checks vendor update stream for kernel version |
| **Hash-based (Java)** | Java Archive (JAR) files | Compares JAR hash to Maven repository — handles renamed JARs |

### Vulnerability Catalog
- Updated at least daily (more often for high-priority events)
- Sources: NVD (National Vulnerability Database), CSP-specific databases, Exploit-DB, product-specific advisories
- Newly added CVE takes 24-48 hours to generate findings (requires next scan)
- Only **high + critical severity** AND/OR **KEV (known exploited)** CVEs are on the security graph; all others are on the Vulnerability Findings page only

### Vulnerability Scanning Architecture
```
Cloud connector → API scan → metadata to Analysis Engine
Workload scanner → disk snapshot → Vulnerability Engine matches against catalog → findings generated
Registry connector → container image layers → same vulnerability engine
Wiz CLI → developer desktop or CI/CD pipeline → same engine
Wiz Sensor → runtime validation of vulnerabilities
```

### CPE (Common Platform Enumeration)
A standardized identifier for software components and versions. Wiz uses CPE to match detected software to known vulnerabilities in NVD. Example: `cpe:2.3:a:haproxy:haproxy:2.4.0:*:*:*:*:*:*:*`

### Vulnerability Findings vs. Vulnerability Object
- **Vulnerability object**: Generic info about the CVE — attack vector, exploitability, has_exploit flag
- **Vulnerability finding**: Resource-specific instance — exact detection method, file location, vendor severity vs. NVD severity

---

## Malware

### How Wiz Detects Malware

**Two Methods:**
1. **Hash-based detection** (via Reversing Labs): Wiz computes a hash of every file on the disk and compares to Reversing Labs' database of known malware hashes. Note: the file itself is NOT sent — only the hash.
2. **Pattern-based detection** (Wiz YARA rules): Proprietary YARA rules written by Wiz research team detect behavior patterns — finds malware families not in public hash databases (web shells, offensive security tools, crypto miners)

**Wiz generates malware issues only at 50%+ confidence.**

### Malware Types (Know These)
- **Ransomware**: Encrypts files and holds them ransom
- **Rootkit**: Collection of tools giving hackers admin-level control
- **Worm**: Replicates and infects other computers
- **Trojan**: Disguised as legitimate software
- **Backdoor**: Hidden access mechanism
- **Coin miner**: Cryptomining malware

### Graph Objects
- **Malware object**: Generic high-level info about the malware family
- **Malware instance object**: Specific to the workload — includes file path where malware was found

### Malware Naming Convention
`[Platform].[Sub-Platform].[Type].[Name]`
Example: `Win32.Ransomware.Sodinokibi` = Targeting 32-bit Windows, ransomware type, Sodinokibi family

### Detection Scope
- Workload scanner: All files on OS disks + non-OS disks (including ZIP, JAR, WAR, UPX, PAR archives)
- Wiz Runtime Sensor: Real-time detection on running workloads
- Buckets: Only scanned if DSPM is enabled

### Custom Hash Detection
You can upload custom file hashes for detection:
- Settings → Scanners → Custom Detection
- Use cases: External threat intelligence feeds, proprietary file tracking (detect if classified files appear where they shouldn't)

### Malware Exclusion Rules
Create rules to prevent Wiz from generating malware findings on known-safe resources:
- Scope by directory path, file extension, file name, project, resource, subscription, resource tag
- Example: Honeypot VMs that intentionally contain malware — exclude them from alerting

---

## DSPM

**DSPM = Data Security Posture Management**

### What It Is
100% agentless, read-only scanning that provides continuous visibility into sensitive data across your cloud. Only sampling — Wiz never stores the actual data.

### What Wiz Scans for Sensitive Data
- VM disk files (OS + non-OS volumes)
- Public and private buckets
- PaaS databases (AWS RDS, Azure SQL, GCP Cloud SQL)
- IaaS databases (MySQL, MariaDB, Postgres, MongoDB)
- Data warehouses (DynamoDB, Redshift, BigQuery, Snowflake)
- Serverless functions
- AI workloads (SageMaker, Bedrock, GCP Vertex)

**Cloud-only. No on-premises scanning.**

### Sensitive Data Categories (Three Types)
1. **Regulated personal data**: PII, PHI, financial data (HIPAA, GDPR, PCI DSS regulated)
2. **Secrets**: Credentials, API tokens, TLS certificates
3. **Proprietary information**: Business plans, trade secrets, financials

### Data Classification Rules
- 100+ built-in rules (credit cards, SSNs, health IDs, passport numbers, email addresses, etc.)
- **Custom classifiers** (two types):
  - **Regex-based**: Parses data content for pattern matches
  - **Metadata-based**: Matches file characteristics (name, location, size, type)
- Rules enabled by default; toggle off ones that don't apply

### Requirements to Enable DSPM
1. **Wiz Cloud Advanced license**
2. Enable data scanning in Settings → Scanners → Data Security (toggle scan types)
3. Enable DSPM permissions in the cloud connector configuration

Public bucket scanning works without DSPM permissions (uses existing connector permissions) and is enabled by default.

### DSPM Graph Objects
| Object | What It Represents |
|--------|-------------------|
| **Data finding** | Match of a classification rule on a resource (PII, PCI, PHI) |
| **Secret instance** | A detected secret on a resource |
| **Data resource** | Wiz abstraction of any scannable data resource (bucket, DB, VM) |
| **Data store** | Collection of structured/unstructured data attached to a resource |
| **Data schema** | Detected structured data (DB table or JSON fields) |
| **Data inventory** | File list and detected content types |
| **AI dataset** | Training/validation data for AI models |
| **AI model** | Computation architecture (LLM, fine-tuned model) |

### Finding Severity
Based on two factors:
1. **Severity of the classification rule** (credit card > zip code)
2. **Frequency of occurrence and number of unique matches** (more unique matches = higher severity)

### Key Use Cases
1. **Breach prevention**: Proactively eliminate attack paths to sensitive data
2. **Data exfiltration detection**: Near-real-time correlation of CSP events + Wiz sensor
3. **Data lineage**: Track how data propagates across environments and regions (important for GDPR — data shouldn't cross into unsupported regions)
4. **Compliance automation**: 24-hour cycle scans assess all cloud configurations against data regulations

### Data Leakage Risk Type
When CDR (Cloud Detection & Response) is enabled, Wiz can detect **active data exfiltration attempts** — not just unprotected data. This is the "data leakage" risk type:
- Combines a sensitive data finding + a near-real-time exfiltration event from GuardDuty, Macie, Sentinel, or the Wiz sensor

---

## Policy Management

### Policy Hierarchy
```
Policies (rules) → generate Findings → Findings feed Controls (graph queries + severity) → Controls generate Issues
```

### Four Policy/Rule Types

**Cloud Configuration Rules (CCR):**
- Check cloud resource configurations via JSON from the CSP
- Powered by OPA (Open Policy Agent) and Rego language
- Use when you need regex-based path evaluation, Kubernetes admission controller checks, or near-real-time config checks
- Results → Cloud Configuration Findings page

**Host Configuration Rules (HCR):**
- Check OS-level and application-level configs on workloads
- Run during workload scan (24-hour cycle or manual)
- Based on CIS benchmark OVAL (Open Vulnerability and Assessment Language) definitions
- Can create custom HCR rules
- Results → Host Configuration Findings page

**Data Classification Rules:**
- Detect sensitive data on storage resources and databases
- Regex-based or metadata-based matching
- Results → Data Findings page

**Threat Detection Rules (three subtypes):**
- **Cloud event rules**: Single malicious event on the cloud control plane (e.g., external subscription operating on a public S3 bucket)
- **Workload runtime rules**: Requires Wiz sensor. Detects activity directly on workloads in near-real-time.
- **Correlation rules**: Malicious chains of events across multiple cloud events (e.g., many failed logins → successful login by privileged user)

### Controls
- Core security graph queries + severity rating
- Codify attacker playbooks
- Run automatically after every scan update
- Single control → multiple issues (one per matching resource)
- Found under: Policies → Graph Controls

### Three Detection Layers (for prioritization)
1. **Single event rules**: Real-time, single malicious event — communication with malicious IP
2. **Correlation rules**: Chains of events indicating attack — higher confidence
3. **Controls**: Full security graph context — blast radius, exposure, permissions — highest context

### Policy Tuning Options
- **Ignore an issue**: Documented exception (shouldn't be standard practice — use with reason + expiration date)
- **Ignore a finding**: Per finding type (cloud config, host config, etc.)
- **Malware exclusion rules**: Exclude specific hashes/paths/resources from malware detection
- **Custom file detection**: Upload hashes to detect specific proprietary files
- **Ignore rules**: Suppress specific types of findings on specific resources (surgical — not broad-brush)
- **Dynamic scanner exposure policy**: Adjust severity of application endpoint exposure (Moderate/Permissive/Strict)

**Best practices for tuning:**
- Be surgical — target specific findings and resources
- Set expiration dates on ignore rules
- Review ignored items on a regular cadence

---

## Access, Authentication & Projects

### Projects
Projects are Wiz's way of logically dividing your cloud estate for different teams. They:
- Reduce alert fatigue (teams only see issues for their resources)
- Enable role-based access at a resource level
- Can scope by cloud org, subscription, cluster, registry, or by **resource tags**

**Project Hierarchy:**
- **Project Folders** can contain Projects or other Folders (max 2 folder levels)
- Each Project can have one parent folder
- Each folder can contain up to 5,000 child projects
- Projects can be archived (preserved) or deleted (requires removing all resources first)

**Project Inheritance:**
User assigned to Folder → inherits access to all Projects within that Folder and any child Folders.

**Risk Profile Metadata** (set by customer, not Wiz):
- Business impact (high/medium/low)
- Internet-facing?
- Regulatory requirements?
- Customer-accessible?

### User Types

**Local Users:**
- Managed by Wiz (backed by AWS Cognito)
- Single role per user
- Use cases: POC/POV, break-glass accounts, backup admin

**SSO Users (Federated):**
- Integrated via SAML 2.0
- Multiple roles per user (via SSO role mapping)
- Supported IDPs: Azure AD, Okta, Ping, AWS IAM Identity Center, and any SAML 2.0 compliant provider
- Role assignments happen at the SSO group mapping stage

### Service Accounts
Used for API calls, automations, third-party integrations. Examples:
- JIRA integration
- Slack notifications
- Wiz sensor deployment
- Wiz broker, admission controller
- Custom scripts via GraphQL API

### RBAC (Role-Based Access Control)
- Predefined roles: Global Admin, Global Contributor, Project Member, Connector Admin, etc.
- Custom roles: Define name, description, project scope, and API scope
- API scopes determine exactly which API calls the role can make

### SSO Setup Flow (SAML 2.0)
1. Add identity provider in Wiz (Settings → Access Management → SSO)
2. Configure SAML application in IDP (map ACS URL, audience, attribute fields)
3. Bring IDP metadata (sign-on URL, logout URL, certificate) into Wiz
4. Set group-to-role mappings

---

## Integrations, Actions & Automations

### Three Components

**Integration**: Authentication info for Wiz to talk to a third-party tool (URL + credentials/tokens).

**Action**: The information Wiz sends to the third party using the integration (e.g., JSON body for a new JIRA ticket).

**Automation Rule**: When + If + Then logic. Example: "When an issue is created, if severity is critical, then create a JIRA ticket."

### Integration Types
- **Push**: Wiz holds auth credentials → pushes data to JIRA, Slack, ServiceNow, etc.
- **Pull**: Third party holds Wiz service account credentials → pulls data from Wiz (SOAR, SIEM)
- **Enrich**: Third-party tool (e.g., BigID) pushes security findings into the Wiz graph
- **Export**: Wiz exports issues/findings/reports to S3, Snowflake, GCP buckets for long-term storage

A single integration can be used by many automation rules.

### Three Ways to Trigger an Action
1. **Manual**: From Issues page → select one issue → run action
2. **Semi-automated (bulk)**: Enable multi-select on Issues page → select multiple issues/controls → run action for all
3. **Automation rule**: Defined in Settings → Response & Automation. Conditions-based. Fires automatically when triggered. Note: automation rules don't apply retroactively — only to new events after the rule is created.

### JIRA Integration Key Points
- Test the integration first (Settings → Integrations → test run)
- Get the project key from JIRA (e.g., "JAT")
- Uses Mustache template language for customizing ticket bodies
- **Create rule** for new issues + **separate Transition rule** for resolved issues (to close tickets)
- Use bulk actions for existing issues (automation only captures future ones)

### ServiceNow Vulnerability Response Integration
- Fetches **vulnerability findings** from Wiz (not issues — findings)
- Three jobs: (1) initial full sync, (2) daily new vulns, (3) daily resolved vulns
- Filters recommended: critical + high severity only (unless customer needs all)
- Appears in ServiceNow as detections (1:1 with Wiz vulnerability findings page)

---

## Compliance

### What Compliance Means in Wiz
A point-in-time assessment of whether cloud resources adhere to industry standards, regulatory requirements, and internal policies. Continuous monitoring. Does not always equal security — but it does attest to diligence.

### Framework Structure
```
Framework → Categories → Guidelines → Policies (controls/config rules)
```

### Two Guideline Types
- **Benchmark guidelines**: Specific, prescriptive criteria (CIS benchmarks — nearly everything can be checked)
- **Non-restrictive guidelines**: General principles — some are outside Wiz's scope (e.g., "contractors must have background checks")

### Compliance Scoring (Four Metrics)
1. **Passed Checks**: Categories where every resource for every guideline passed. 7/28 means 7 categories had 100% pass rate.
2. **Compliance Posture**: Total passed checks ÷ total checks (passed + failed). Expressed as percentage. Calculated per category, guideline, and policy.
3. **Guideline score**: All policies in a guideline must pass before the guideline is marked passed.
4. **Policy score**: X of Y resources passed the specific policy check.

### Compliance Heat Map
View all frameworks against all projects simultaneously. Spot which projects are failing which frameworks. Double-click hotspots to drill into specifics.

### Wiz-Specific Frameworks (Not Regulatory)
Wiz builds its own frameworks focused on **preventing cloud threats and being prepared for detection and response**:
- **Wiz for Risk Assessment**: Includes controls that map to built-in dashboards. Allows you to control which issues appear on which boards.
- **Wiz for Cloud Native**: Cloud-specific threat prevention

### Compliance Reports
- Can be scheduled (weekly, monthly, etc.)
- Export to email, S3 bucket, GCP/AWS bucket, Snowflake
- Filter by framework, subscription, category, status

### Slow Roll Strategy
For compliance teams overwhelmed by findings: enable a new framework with all policies disabled → enable policies one at a time → teams can address violations in a controlled, manageable way.

### CIS Certification
CIS-certified Wiz frameworks means Wiz has been verified to accurately check and report on specific CIS benchmark versions.

---

## Licensing & Workloads

### Two Licenses

**Wiz Essentials:**
- Immediate cloud visibility
- Context-rich prioritization
- Increased agility
- No DSPM (but some DSPM-like features)
- Best for: small teams, early cloud adoption, simple environments

**Wiz Advanced:**
Includes all Essentials features, plus:
- Container registry scanning
- Admission controller support
- Attack path analysis
- Internal lateral movement detection
- CDR (Cloud Detection & Response) features
- Advanced integrations and auto-remediation
- Custom policy support
- Advanced detections (DNS dangling entries, unauthorized file changes, validated open ports)
- **Wiz Outpost** (Advanced only)
- DSPM (full)

### Billing — Billable Workloads

| Type | What Counts | License |
|------|------------|---------|
| **Compute** | VMs, containers, serverless (50 functions = 1 workload) | Both |
| **Data workloads** | Buckets, non-OS volumes, databases | Advanced only |
| **Runtime sensors** | Wiz sensor deployments | Advanced only |

- VMs and containers each count as 1 workload
- 50 serverless functions = 1 workload
- 10 serverless containers = 1 workload
- VM + container running on it = counted twice (separate resources)
- Billing: monthly average of daily workload counts

---

## Wiz Code — Shift Left

### The Problem Wiz Code Solves
Traditional cloud security starts when code is deployed. Attackers now target:
- Source code repositories (VCS)
- CI/CD pipelines
- Developer credentials and secrets in code
- Third-party library dependencies (supply chain attacks)
- Container images before deployment

**Shift-left** = catch security issues at the **code stage**, not production.

### Wiz Code Architecture
Wiz protects every stage of the SDLC:

```
Code (IDE + VCS) → Build (CI/CD pipelines) → Deploy (registries, admission controller) → Runtime (Wiz Sensor)
```

### What Wiz Code Scans For
- **Vulnerabilities**: In code libraries and dependencies (SAST + SCA)
- **Secrets**: Hardcoded credentials, API keys, tokens in code
- **IaC misconfigurations**: Terraform, CloudFormation, Docker — scanned before deployment
- **Sensitive data**: In code and repositories
- **Supply chain integrity**: Container image signing validation (cosign, Notary v2)

### Key Tools/Integrations
- **Wiz CLI**: Lightweight executable. Runs on developer desktop or in pipeline. Scans container images, VM images, IaC files, directories.
- **IDE integration** (VS Code): Instant feedback on vulnerabilities without leaving the editor
- **VCS integration** (GitHub, GitLab, etc.): Pull/merge request scanning → can block PRs with critical findings
- **Admission controller**: Validates container images at deploy time before they run in Kubernetes clusters

### CI/CD Policy Stages
- **Code stage**: Vulnerabilities, secrets, IaC config, sensitive data
- **Build stage**: All of code stage + host configuration
- **Deploy stage**: IaC configuration + image trust only

### Policy Actions
- **Audit**: Notify but don't block
- **Block**: Stop the pipeline / prevent the PR merge

### Default Policies
- Vulnerabilities: **Block** on critical severity with a fix available
- Secrets: Audit, threshold = informational (notify but don't block)
- IaC config: Audit on critical
- Sensitive data: Audit only
- Image trust: Block if not signed with cosign/Notary v2

### Exception Management
Ways to ignore findings in code (temporary, documented only):
- **Inline code comments**: Ignore specific file, block, or single line
- **`.wiz` file** in repo root: Ignore by CVE ID, file path, or directory
- **PR/MR comments**: `#wiz-ignore reason:false-positive`
- **Block PR label**: Skip the entire check (noted but not an ignore rule)

Security teams can disable these exception capabilities per VCS connector to enforce policies fully.

---

## Wiz Defend — CDR & Threat Detection

### What Wiz Defend Is
Wiz Defend = **Cloud Detection and Response (CDR)** — the runtime threat detection and investigation layer. Built from the acquisition of Gem Security (April 2024). Focused on the **security operations team** (SOC analysts, threat hunters, incident responders).

### Four Pillars of Defend

**1. Prepare** — Incident Readiness
- Incident readiness score (tracks posture over time)
- Sensor coverage metrics across K8s clusters, Linux VMs, Fargate, etc.
- Log configuration breakdown: are you collecting the right logs? (CloudTrail, VPC flow, S3 data events, DNS, etc.)
- **MITRE ATT&CK for Cloud mapping**: Shows which tactics/techniques you can detect vs. which you're missing
- Remediation guidance in Terraform or IaC format

**2. Detect** — Detection Pipeline
Data sources ingested:
- AWS CloudTrail (read + write events)
- VPC flow logs, S3 data events
- Azure activity/storage logs, Key Vault logs
- GCP audit logs
- CrowdStrike, SentinelOne (EDR platforms)
- Okta identity logs
- GitHub/GitLab audit logs
- Wiz runtime sensor events

Detection features:
- **Behavioral baselines**: Model normal behavior for every entity. Distinguish business-as-usual (CI pipeline enumeration) from threat-actor enumeration.
- **Smart grouping (automated correlation)**: Groups related detections into a single **threat** — shows the attack story as it unfolds

**3. Investigate** — Investigation Graph
Similar to the Security Graph but shows **attack timeline**, not attack paths. Displays:
- Initial access point
- Processes spawned
- Lateral movement events
- Data accessed or exfiltrated
- All across multiple signal sources (sensor + CloudTrail + S3 data events + GuardDuty)

**4. Respond** — Response Guidance
- Provides recommended actions (call developer, kill process, revoke credentials)
- Cloud-native playbooks
- Reduces response time from hours/days to minutes

### Threat Object
New work item for SOC teams in Wiz Defend. A threat:
- Groups correlated detections together
- Is a living, breathing thing (new activity gets added as the attack evolves)
- Shows MITRE ATT&CK tactics and techniques
- Shows all event origins contributing to the threat

### Wiz Sensor
An eBPF-based runtime sensor deployable on Kubernetes clusters and Linux VMs. Provides:
- Real-time process monitoring
- Network connection tracking
- File system activity
- Continuous workload telemetry
- Powers workload runtime detection rules

---

## Quick Glossary

| Term | Definition |
|------|-----------|
| **Agentless** | Scanning technique that doesn't require installing software (agents) on target systems. Uses APIs or snapshots. |
| **Application Endpoint** | Wiz object created when a resource is exposed to 0.0.0.0/0 on at least one port. |
| **Blast Radius** | The extent of damage an attacker could cause if they compromised a specific resource. |
| **CCR** | Cloud Configuration Rule — policy check against cloud resource JSON config. |
| **CDR** | Cloud Detection & Response — runtime threat detection. Wiz Defend capability. |
| **CNAPP** | Cloud-Native Application Protection Platform — unified security for cloud apps from code to runtime. Wiz IS a CNAPP. |
| **Control** | Security graph query + severity rating. Codifies an attacker playbook. Generates issues. |
| **CVE** | Common Vulnerability and Exposure. Unique identifier for a publicly disclosed vulnerability. |
| **CVSS** | Common Vulnerability Scoring System. 0–10 score. Wiz uses vendor severity over NVD. |
| **Dynamic Scanner** | Wiz module that validates network exposure by actually attempting TCP connections to exposed ports. Requires Advanced license. |
| **eBPF** | Extended Berkeley Packet Filter — kernel technology used by the Wiz sensor for low-overhead runtime monitoring. |
| **Effective Permissions** | What a principal can *actually* do, after accounting for all grants, blocks, and boundary policies. |
| **Enrichment** | The process of adding derived knowledge (exposure, lateral movement, effective permissions) to the graph after initial discovery. |
| **Eventually Consistent** | Wiz's architecture model — components process data asynchronously, and the graph converges to a consistent state over time. |
| **Finding** | A specific weakness on a specific resource. One data point. NOT the same as an issue. |
| **HCR** | Host Configuration Rule — policy check against OS/application configuration on a workload. |
| **Issue** | A toxic combination of findings representing a real, prioritized risk. Generated by controls. |
| **KEV** | Known Exploited Vulnerabilities — CISA catalog of CVEs with confirmed real-world exploits. Highest priority. |
| **Lateral Movement** | An attacker's ability to move from one resource to another after gaining initial access. |
| **OPA** | Open Policy Agent — open-source policy engine used to run CCR policies (Rego language). |
| **OVAL** | Open Vulnerability and Assessment Language — used to define HCR check logic. |
| **Principal** | Any entity that can access a resource — user, service account, group, predefined group. |
| **Project** | Wiz's logical division of cloud resources for team-based access and alerting. |
| **Rego** | Policy language used with OPA for writing cloud configuration rules. |
| **Security Graph** | The graph database at the core of Wiz. Stores all discovered and derived knowledge. Foundation for all queries and controls. |
| **Subscription** | Wiz normalized term for: AWS Account, Azure Subscription, GCP Project, OCI Compartment, Alibaba Account. |
| **Toxic Combination** | Multiple findings across risk domains that together represent a real risk (attack path). What Wiz issues represent. |
| **Wiz CLI** | Lightweight command-line tool for shift-left scanning in IDEs, local machines, and CI/CD pipelines. |
| **Wiz Outpost** | In-customer-tenant workload scanning. Only metadata leaves the customer environment. |
| **Wiz Sensor** | eBPF-based runtime agent for real-time workload monitoring and threat detection. |
| **YARA** | Pattern-matching language used for malware detection based on behavioral signatures, not just hashes. |
| **Zero-Copy** | Wiz workload scanning approach — snapshot is mounted (not copied) to the scanner, scanned, then deleted. |

---

*Last updated: April 2026 | Based on Wiz Technical Essentials, Managing Cloud Security Posture, Securing Cloud Development, and Wiz Defend training*