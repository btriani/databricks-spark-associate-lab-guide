#!/usr/bin/env bash
set -euo pipefail

PASS=0
FAIL=0

check() {
    local name="$1"
    local cmd="$2"
    local min_version="${3:-}"

    if eval "$cmd" &>/dev/null; then
        echo "  [PASS] $name"
        ((PASS++))
    else
        echo "  [FAIL] $name"
        ((FAIL++))
    fi
}

echo ""
echo "=== Databricks Spark Lab Guide — Prerequisites Check ==="
echo ""

echo "1. Python"
check "Python 3.10+" "python3 --version 2>&1 | grep -E 'Python 3\.(1[0-9]|[2-9][0-9])'"

echo ""
echo "2. Databricks CLI"
check "Databricks CLI installed" "databricks --version"

echo ""
echo "3. Python Packages"
check "databricks-sdk" "python3 -c 'import databricks.sdk'"

echo ""
echo "4. Authentication"
check "Databricks auth configured" "databricks auth describe --profile DEFAULT 2>&1 | grep -i 'valid'"

echo ""
echo "=== Results ==="
echo "  Passed: $PASS"
echo "  Failed: $FAIL"
echo ""

if [ "$FAIL" -gt 0 ]; then
    echo "Some checks failed. See prerequisites.md for setup instructions."
    exit 1
else
    echo "All checks passed. You are ready to run the labs."
    echo "Next step: python scripts/setup-catalog.py"
fi
