# Cost Guide

## Full Run Cost: ~$10-15

Going through all 10 labs from start to finish costs approximately $10-15. This applies whether you are a learner working through the material or a contributor running a validation pass.

| Resource | Estimated Cost | Notes |
|----------|---------------|-------|
| Serverless compute (Labs 02-09) | $5-8 | ~$0.07/DBU, per-second billing, zero idle cost |
| Cluster compute (Labs 01 & 10) | $3-5 | Single-node cluster, ~30 min each |
| Data storage (Unity Catalog Volumes) | <$0.50 | A few GB of taxi and GitHub data |
| **Total** | **$10-15** | |

## Cost Breakdown by Lab

| Lab | Compute Type | Estimated Cost | Time |
|-----|-------------|---------------|------|
| 01 - Spark Architecture | Cluster | $1-2 | 25 min |
| 02 - Reading & Writing Data | Serverless | ~$1 | 30 min |
| 03 - Transformations & Actions | Serverless | ~$1 | 35 min |
| 04 - Aggregations & Grouping | Serverless | ~$1 | 35 min |
| 05 - Joins & Set Operations | Serverless | ~$1 | 35 min |
| 06 - Complex Data Types | Serverless | ~$1 | 30 min |
| 07 - Spark SQL & Catalog | Serverless | $1-2 | 35 min |
| 08 - Structured Streaming | Serverless | $1-2 | 35 min |
| 09 - Delta Lake, Pandas API & Spark Connect | Serverless | ~$1 | 30 min |
| 10 - Performance Tuning | Cluster | $2-3 | 40 min |

## Cost Traps

| Trap | Risk | How to Avoid |
|------|------|-------------|
| Leaving cluster running after Lab 01 | ~$2-4/hour idle | Terminate cluster immediately after Lab 01. You don't need it again until Lab 10. |
| Forgetting to stop streams in Lab 08 | Continuous compute charges | Run the cleanup cell at the end of Lab 08. It stops all active streams. |
| Not running cleanup.py when finished | Small but accumulating storage costs | Run `python scripts/cleanup.py` when you are done with all labs. |

## Tips

- **Serverless compute has zero idle cost.** You can pause mid-lab, close your laptop, and come back later without charges accumulating.
- **Run labs in order.** The setup script downloads data once, and Lab 02 creates shared Delta tables. Re-running setup wastes compute.
- **Labs 01 and 10 are the only cluster labs.** They are placed at the start and end so you only pay for cluster time twice.

## For Contributors and Forkers

If you fork this repository and want to validate that all labs run correctly, budget 2-3 full passes:

| Scenario | Estimated Cost |
|----------|---------------|
| First full pass (setup + 10 labs + cleanup) | $10-15 |
| Subsequent pass (data already loaded, fixing issues) | $5-10 |
| **Total QA budget** | **$20-30** |

Each pass runs `setup-catalog.py` once, executes all 10 labs in sequence (skipping per-lab cleanup cells), then runs `cleanup.py` once at the end.
