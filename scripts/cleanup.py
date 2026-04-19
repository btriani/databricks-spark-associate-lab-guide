"""
Cleanup script for Databricks Spark Associate Lab Guide.
Removes all Unity Catalog resources created by setup and labs.

Usage: python scripts/cleanup.py
"""

import sys

try:
    from databricks.sdk import WorkspaceClient
except ImportError:
    print("ERROR: databricks-sdk not installed. Run: pip install databricks-sdk")
    sys.exit(1)

CATALOG = "spark_lab_guide"


def main():
    print("=" * 60)
    print("Databricks Spark Associate Lab Guide — Cleanup")
    print("=" * 60)
    print()
    print(f"This will permanently delete the catalog '{CATALOG}' and ALL")
    print("tables, views, volumes, and data inside it.")
    print()

    confirm = input("Type 'yes' to confirm: ").strip().lower()
    if confirm != "yes":
        print("Cleanup cancelled.")
        return

    w = WorkspaceClient()

    print(f"\nDeleting catalog '{CATALOG}' and all contents...")
    try:
        w.catalogs.delete(name=CATALOG, force=True)
        print(f"  Catalog '{CATALOG}' deleted successfully.")
    except Exception as e:
        if "not found" in str(e).lower() or "does not exist" in str(e).lower():
            print(f"  Catalog '{CATALOG}' does not exist. Nothing to clean up.")
        else:
            print(f"  Error deleting catalog: {e}")
            sys.exit(1)

    print("\nCleanup complete. All lab resources have been removed.")


if __name__ == "__main__":
    main()
