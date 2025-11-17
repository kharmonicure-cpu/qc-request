#!/usr/bin/env python3
"""
Verification script for combined_project_test_cases.csv

Checks for common issues and data quality problems.
"""

import pandas as pd
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
COMBINED_FILE = ROOT_DIR / "processed-data" / "combined_project_test_cases.csv"

REQUIRED_COLUMNS = [
    'project_name', 'main_category', 'scope_of_dev', 'test_case',
    'Fire TV', 'Roku', 'Android TV', 'Apple TV', 'Web',
    'Apple Mobile', 'Android Mobile', 'Smart TV', 'Vizio TV'
]

DEVICE_COLUMNS = [
    'Fire TV', 'Roku', 'Android TV', 'Apple TV', 'Web',
    'Apple Mobile', 'Android Mobile', 'Smart TV', 'Vizio TV'
]


def main():
    print("=" * 60)
    print("Data Verification Script")
    print("=" * 60)
    print()

    if not COMBINED_FILE.exists():
        print(f"❌ ERROR: Combined file not found at: {COMBINED_FILE}")
        return

    print(f"📁 Checking: {COMBINED_FILE.name}")
    print()

    # Read the file
    try:
        df = pd.read_csv(COMBINED_FILE)
    except Exception as e:
        print(f"❌ ERROR: Failed to read CSV file")
        print(f"   {str(e)}")
        return

    issues_found = 0

    # Check 1: Required columns
    print("1️⃣  Checking required columns...")
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        print(f"   ❌ Missing columns: {', '.join(missing_cols)}")
        issues_found += 1
    else:
        print("   ✅ All required columns present")
    print()

    # Check 2: Empty values
    print("2️⃣  Checking for empty values...")
    empty_projects = df[df['project_name'].isna() | (df['project_name'] == '')].shape[0]
    empty_categories = df[df['main_category'].isna() | (df['main_category'] == '')].shape[0]
    empty_scope = df[df['scope_of_dev'].isna() | (df['scope_of_dev'] == '')].shape[0]
    empty_tests = df[df['test_case'].isna() | (df['test_case'] == '')].shape[0]

    if empty_projects > 0:
        print(f"   ⚠️  {empty_projects} rows with empty project_name")
        issues_found += 1
    if empty_categories > 0:
        print(f"   ⚠️  {empty_categories} rows with empty main_category")
        issues_found += 1
    if empty_scope > 0:
        print(f"   ⚠️  {empty_scope} rows with empty scope_of_dev")
        issues_found += 1
    if empty_tests > 0:
        print(f"   ⚠️  {empty_tests} rows with empty test_case")
        issues_found += 1

    if empty_projects + empty_categories + empty_scope + empty_tests == 0:
        print("   ✅ No empty values found")
    print()

    # Check 3: Device columns
    print("3️⃣  Checking device columns...")
    device_issues = 0
    for device_col in DEVICE_COLUMNS:
        if device_col in df.columns:
            non_boolean = df[~df[device_col].isin([True, False, 0, 1])].shape[0]
            if non_boolean > 0:
                print(f"   ⚠️  {device_col}: {non_boolean} non-boolean values")
                device_issues += 1
        else:
            print(f"   ❌ {device_col}: Column missing")
            device_issues += 1

    if device_issues == 0:
        print("   ✅ All device columns have valid boolean values")
    else:
        issues_found += 1
    print()

    # Check 4: Rows with no devices selected
    print("4️⃣  Checking for rows with no devices selected...")
    df_devices = df[DEVICE_COLUMNS]
    no_devices = df_devices.sum(axis=1) == 0
    rows_no_devices = no_devices.sum()

    if rows_no_devices > 0:
        print(f"   ⚠️  {rows_no_devices} rows have no devices selected")
        print("   These rows won't appear in any device dropdown!")
        issues_found += 1
    else:
        print("   ✅ All rows have at least one device selected")
    print()

    # Check 5: Project summary
    print("5️⃣  Project summary...")
    if 'project_name' in df.columns:
        projects = df['project_name'].unique()
        print(f"   📊 Total projects: {len(projects)}")
        for project in sorted(projects):
            count = len(df[df['project_name'] == project])
            print(f"      - {project}: {count} test case groups")
    print()

    # Check 6: Duplicate rows
    print("6️⃣  Checking for potential duplicates...")
    duplicates = df.duplicated(subset=['project_name', 'main_category', 'scope_of_dev'], keep=False)
    dup_count = duplicates.sum()

    if dup_count > 0:
        print(f"   ⚠️  {dup_count} potential duplicate rows found")
        print("   (Same project_name + main_category + scope_of_dev)")
        issues_found += 1
    else:
        print("   ✅ No duplicate rows found")
    print()

    # Summary
    print("=" * 60)
    if issues_found == 0:
        print("✅ All checks passed! Data looks good.")
    else:
        print(f"⚠️  Found {issues_found} issue(s) that need attention.")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
