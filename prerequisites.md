# Prerequisites

## Databricks Workspace

You need access to a Databricks workspace with:
- **Unity Catalog** enabled
- Permission to create catalogs, schemas, and volumes
- Access to **serverless compute** (Labs 02-09)
- Ability to create a **single-node cluster** (Labs 01 and 10)

A pay-as-you-go workspace or a trial workspace with Unity Catalog will work.

## Local Environment

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Python | 3.10+ | `python --version` |
| Databricks CLI | 0.200+ | `databricks --version` |
| databricks-sdk | latest | `pip show databricks-sdk` |

## Authentication

Configure Databricks CLI authentication before running the setup script:

```bash
databricks configure
```

You will need:
- Your workspace URL (e.g., `https://adb-1234567890.12.azuredatabricks.net`)
- A personal access token (generate one from **Settings > Developer > Access Tokens** in your workspace)

## Validate Setup

Run the prerequisites check script to verify everything is configured:

```bash
bash scripts/check-prerequisites.sh
```

## Cluster Configuration (Labs 01 and 10 only)

For the two labs that require a cluster, create a single-node cluster with:
- **Databricks Runtime:** 15.4 LTS or later
- **Node type:** Smallest available (e.g., `i3.xlarge` on AWS, `Standard_DS3_v2` on Azure)
- **Workers:** 0 (single-node mode)
- **Auto-termination:** 30 minutes

All other labs use serverless compute (no cluster setup needed).
