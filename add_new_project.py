#!/usr/bin/env python3
"""
QC Test Case Processor - Simplified Workflow

WORKFLOW:
1. Script reads a new CSV from the preprocessed-tc/ folder
2. Processes and creates per-project CSV in project-tc-archive/
3. Updates the combined CSV in project-tc-archive/
4. Streamlit app (qc_form_generator.py) reads from the combined CSV

USAGE:
1. Place your raw input CSV in preprocessed-tc/ folder
2. Update INPUT_FILE and PROJECT_NAME below
3. Run: python add_new_project.py
4. Done! The app will automatically use the updated data
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# ========== UPDATE THESE VALUES ==========
INPUT_FILE = "basic_web.csv"  # File in preprocessed-tc/ folder
PROJECT_NAME = "Basic Verification"   # Your project name
# =========================================

# === DO NOT MODIFY BELOW THIS LINE ===

# Paths
SCRIPT_DIR = Path(__file__).parent
PREPROCESSED_DIR = SCRIPT_DIR / "preprocessed-tc"
ARCHIVE_DIR = SCRIPT_DIR / "project-tc-archive"
COMBINED_FILE = ARCHIVE_DIR / "combined_project_test_cases.csv"

# Constants
AVAILABLE_DEVICES = [
    'Android Mobile', 'Apple Mobile', 'Android TV', 'Apple TV',
    'Fire TV', 'Smart TV', 'Vizio TV', 'Roku', 'Web'
]

RENAME_RULES = {
    "대분류": "main_category",
    "중분류": "sub_category",
    "소분류": "component",
    "Section": "scenario",
    "테스트 항목": "test_case"
}


def generate_scope_of_dev(main: str, sub: str, comp: str) -> str:
    """Generate scope_of_dev column from category hierarchy."""
    if comp == "":
        if sub == "":
            return "General Rules"
        else:
            return sub
    else:
        if sub != "":
            return sub
    return comp


def set_device_relevancy(purpose: str, df: pd.DataFrame, idx: int):
    """Set device columns based on Purpose value."""
    purpose_lower = purpose.lower()

    if "web" in purpose_lower:
        df.at[idx, "Web"] = True
    if "mobile" in purpose_lower:
        df.at[idx, "Android Mobile"] = True
        df.at[idx, "Apple Mobile"] = True
    if "connected tv" in purpose_lower:
        df.at[idx, "Android TV"] = True
        df.at[idx, "Apple TV"] = True
        df.at[idx, "Fire TV"] = True
        df.at[idx, "Roku"] = True
    if "smarttv" in purpose_lower:
        df.at[idx, "Smart TV"] = True
        df.at[idx, "Vizio TV"] = True


def main():
    print("=" * 60)
    print("QC Test Case Processor")
    print("=" * 60)
    print()

    # Ensure directories exist
    PREPROCESSED_DIR.mkdir(exist_ok=True)
    ARCHIVE_DIR.mkdir(exist_ok=True)

    # Validate input file exists
    input_path = PREPROCESSED_DIR / INPUT_FILE
    if not input_path.exists():
        print(f"❌ ERROR: Input file not found at: {input_path}")
        print(f"   Make sure the file is in the 'preprocessed-tc/' folder")
        print(f"   Current preprocessed-tc/ contents:")
        for f in PREPROCESSED_DIR.glob("*.csv"):
            print(f"     - {f.name}")
        return

    print(f"📁 Input file: {INPUT_FILE}")
    print(f"📦 Project name: {PROJECT_NAME}")
    print()

    # Read files
    print("✓ Reading input file from preprocessed-tc/...")
    try:
        df_new = pd.read_csv(input_path)[['Purpose', '대분류', '중분류', '소분류', '테스트 항목']].fillna("")
        df_new.rename(columns=RENAME_RULES, inplace=True)
    except KeyError as e:
        print(f"❌ ERROR: Missing required column in input file: {e}")
        print(f"   Required columns: Purpose, 대분류, 중분류, 소분류, 테스트 항목")
        return
    except Exception as e:
        print(f"❌ ERROR: Failed to read input file: {e}")
        return

    # Check if combined file exists
    if COMBINED_FILE.exists():
        print("✓ Reading existing combined file from project-tc-archive/...")
        df_combined = pd.read_csv(COMBINED_FILE)
    else:
        print("⚠️  No existing combined file found. Creating new one...")
        df_combined = pd.DataFrame()

    # Process new data
    print("✓ Processing data...")
    df_new["project_name"] = PROJECT_NAME

    # Initialize device columns
    for device in AVAILABLE_DEVICES:
        df_new[device] = False

    # Strip whitespace
    for col in ["main_category", "sub_category", "component"]:
        df_new[col] = df_new[col].astype(str).str.strip()

    # Generate scope_of_dev
    df_new["scope_of_dev"] = df_new.apply(
        lambda row: generate_scope_of_dev(row["main_category"], row["sub_category"], row["component"]),
        axis=1
    )

    # Set device relevancy
    for idx, row in df_new.iterrows():
        set_device_relevancy(row["Purpose"], df_new, idx)

    # Drop Purpose column (no longer needed)
    df_new = df_new.drop(columns=["Purpose", "sub_category", "component", "scenario"], errors='ignore')

    # Group by scope and combine test cases
    df_new = df_new.groupby(['project_name', 'main_category', 'scope_of_dev']).agg({
        'test_case': lambda x: '\n'.join(x),
        'Fire TV': 'max',
        'Roku': 'max',
        'Android TV': 'max',
        'Apple TV': 'max',
        'Web': 'max',
        'Apple Mobile': 'max',
        'Android Mobile': 'max',
        'Smart TV': 'max',
        'Vizio TV': 'max'
    }).reset_index()

    # Reorder columns
    col_order = [
        'project_name', 'main_category', 'scope_of_dev', 'test_case',
        'Fire TV', 'Roku', 'Android TV', 'Apple TV', 'Web',
        'Apple Mobile', 'Android Mobile', 'Smart TV', 'Vizio TV'
    ]
    df_new = df_new[col_order]

    # Save individual project file to archive
    today = datetime.today().strftime("%Y%m%d")
    project_output_file = ARCHIVE_DIR / f"{today}_{PROJECT_NAME}.csv"
    print(f"✓ Saving per-project file to project-tc-archive/: {project_output_file.name}")
    df_new.to_csv(project_output_file, index=False)

    # Merge with combined file
    print("✓ Merging with combined file in project-tc-archive/...")
    if df_combined.empty:
        df_merged = df_new
    else:
        df_merged = pd.concat([df_combined, df_new]).sort_values(by=['project_name'], ascending=False)

    df_merged.to_csv(COMBINED_FILE, index=False)
    print(f"✓ Updated combined file: {COMBINED_FILE.name}")

    print()
    print("=" * 60)
    print(f"✅ Done! Project '{PROJECT_NAME}' added successfully.")
    print("=" * 60)
    print()
    print("📊 Summary:")
    print(f"   - Test case groups added: {len(df_new)}")
    print(f"   - Per-project file: {project_output_file.name}")
    print(f"   - Combined file: {COMBINED_FILE.name}")
    print()
    print("📂 File locations:")
    print(f"   - Input: preprocessed-tc/{INPUT_FILE}")
    print(f"   - Output: project-tc-archive/{project_output_file.name}")
    print(f"   - Combined: project-tc-archive/{COMBINED_FILE.name}")
    print()
    print("🔗 Next steps:")
    print("   1. Run the Streamlit app: streamlit run qc_form_generator.py")
    print("   2. Or check the deployed app: https://qc-generator.streamlit.app/")
    print("   3. Your new project should appear in the dropdown!")
    print()


if __name__ == "__main__":
    main()
