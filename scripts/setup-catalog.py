"""
Setup script for Databricks Spark Associate Lab Guide.
Creates Unity Catalog resources and downloads public datasets.

Usage: python scripts/setup-catalog.py
"""

import sys
import os
import urllib.request
import tempfile
from pathlib import Path

try:
    from databricks.sdk import WorkspaceClient
    from databricks.sdk.service.catalog import VolumeType
except ImportError:
    print("ERROR: databricks-sdk not installed. Run: pip install databricks-sdk")
    sys.exit(1)

CATALOG = "spark_lab_guide"
SCHEMA = "default"
TAXI_VOLUME = "nyc_taxi"
GITHUB_VOLUME = "github_archive"

# NYC Taxi: 3 months of Yellow Taxi data (Jan-Mar 2024, Parquet)
TAXI_URLS = [
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet",
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-02.parquet",
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-03.parquet",
]

# GitHub Archive: 3 hours of events (JSON, gzipped)
GITHUB_URLS = [
    "https://data.gharchive.org/2024-01-15-10.json.gz",
    "https://data.gharchive.org/2024-01-15-11.json.gz",
    "https://data.gharchive.org/2024-01-15-12.json.gz",
]


def create_catalog_resources(w):
    """Create catalog, schema, and volumes."""
    print(f"Creating catalog: {CATALOG}")
    try:
        # Try without storage location first (works if default storage is configured)
        w.catalogs.create(name=CATALOG)
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"  Catalog {CATALOG} already exists, continuing...")
        elif "storage root" in str(e).lower() or "storage location" in str(e).lower():
            # Workspace requires explicit storage — get root from an existing catalog
            print("  Default storage not available, detecting storage root...")
            for cat in w.catalogs.list():
                if cat.storage_root and cat.name not in ("system", "samples"):
                    storage_root = cat.storage_root
                    print(f"  Using storage root: {storage_root}")
                    w.catalogs.create(name=CATALOG, storage_root=storage_root)
                    break
            else:
                raise RuntimeError("No existing catalog with storage root found. Please create the catalog manually.")
        else:
            raise

    print(f"Creating schema: {CATALOG}.{SCHEMA}")
    try:
        w.schemas.create(name=SCHEMA, catalog_name=CATALOG)
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"  Schema {CATALOG}.{SCHEMA} already exists, continuing...")
        else:
            raise

    for vol_name in [TAXI_VOLUME, GITHUB_VOLUME]:
        print(f"Creating volume: {CATALOG}.{SCHEMA}.{vol_name}")
        try:
            w.volumes.create(
                catalog_name=CATALOG,
                schema_name=SCHEMA,
                name=vol_name,
                volume_type=VolumeType.MANAGED,
            )
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"  Volume {vol_name} already exists, continuing...")
            else:
                raise


def download_and_upload(w, urls, volume_path):
    """Download files from URLs and upload to Databricks Volume."""
    # Set User-Agent header (required by some data providers like GH Archive)
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'databricks-spark-lab-guide/1.0')]
    urllib.request.install_opener(opener)

    for url in urls:
        filename = url.split("/")[-1]
        dest_path = f"{volume_path}/{filename}"
        print(f"  Downloading {filename}...")

        with tempfile.NamedTemporaryFile(delete=False, suffix=filename) as tmp:
            urllib.request.urlretrieve(url, tmp.name)
            tmp_path = tmp.name

        print(f"  Uploading to {dest_path}...")
        with open(tmp_path, "rb") as f:
            w.files.upload(dest_path, f, overwrite=True)

        os.unlink(tmp_path)
        print(f"  Done: {filename}")


def validate(w):
    """Verify all resources exist."""
    print("\nValidating setup...")
    taxi_path = f"/Volumes/{CATALOG}/{SCHEMA}/{TAXI_VOLUME}"
    github_path = f"/Volumes/{CATALOG}/{SCHEMA}/{GITHUB_VOLUME}"

    taxi_files = list(w.files.list_directory_contents(taxi_path))
    github_files = list(w.files.list_directory_contents(github_path))

    print(f"  NYC Taxi files:     {len(taxi_files)} files in {taxi_path}")
    print(f"  GitHub Archive files: {len(github_files)} files in {github_path}")

    if len(taxi_files) < 3 or len(github_files) < 3:
        print("\nWARNING: Some files may be missing. Check the volumes manually.")
        return False

    print("\nSetup complete. All resources are in place.")
    return True


def main():
    print("=" * 60)
    print("Databricks Spark Associate Lab Guide — Setup")
    print("=" * 60)
    print()

    w = WorkspaceClient()

    create_catalog_resources(w)

    taxi_path = f"/Volumes/{CATALOG}/{SCHEMA}/{TAXI_VOLUME}"
    github_path = f"/Volumes/{CATALOG}/{SCHEMA}/{GITHUB_VOLUME}"

    print("\nDownloading NYC Taxi data (3 months, Parquet)...")
    download_and_upload(w, TAXI_URLS, taxi_path)

    print("\nDownloading GitHub Archive data (3 hours, JSON)...")
    download_and_upload(w, GITHUB_URLS, github_path)

    validate(w)

    print()
    print("Next step: Open Lab 01 in your Databricks workspace.")
    print("See README.md for instructions.")


if __name__ == "__main__":
    main()
