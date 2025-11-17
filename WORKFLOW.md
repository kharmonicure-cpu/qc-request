# QC Form Generator - Complete Workflow

## 📂 Folder Structure

```
qc-request-handover-package/
├── preprocessed-tc/              # INPUT: Place new raw CSV files here
│   └── sample_input.csv         # Example input file
│
├── project-tc-archive/           # OUTPUT: All processed data
│   ├── 20251028_Get Started.csv # Per-project processed files
│   ├── 20250819_Email Verification.csv
│   └── combined_project_test_cases.csv  # Master file (used by Streamlit app)
│
├── qc_form_generator.py          # Streamlit app (reads from combined CSV)
├── add_new_project.py            # Data processor script
└── ...                           # Documentation and config files
```

---

## 🔄 Complete Workflow

### Step 1: Prepare Input File
1. Create or obtain your test case CSV file
2. Ensure it has required columns:
   - `Purpose` (WEB, MOBILE, CONNECTED TV, SMARTTV)
   - `대분류`, `중분류`, `소분류`, `테스트 항목`
3. **Place the file in `preprocessed-tc/` folder**

### Step 2: Process the Data
1. Open `add_new_project.py`
2. Update two variables at the top:
   ```python
   INPUT_FILE = "your_file.csv"  # Must be in preprocessed-tc/
   PROJECT_NAME = "Your Project Name"
   ```
3. Run the script:
   ```bash
   python add_new_project.py
   ```

### Step 3: Script Execution
The script automatically:
1. ✅ Reads raw CSV from `preprocessed-tc/`
2. ✅ Processes data (device mapping, grouping, etc.)
3. ✅ Saves per-project file to `project-tc-archive/YYYYMMDD_ProjectName.csv`
4. ✅ Updates `project-tc-archive/combined_project_test_cases.csv`

### Step 4: Streamlit App Updates
The `qc_form_generator.py` app:
- Reads from `project-tc-archive/combined_project_test_cases.csv`
- Automatically shows your new project in the dropdown
- No manual intervention needed!

---

## 📊 Data Flow Diagram

```
┌─────────────────────┐
│   Raw Input CSV     │
│ (preprocessed-tc/)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ add_new_project.py  │ ◄─── You edit INPUT_FILE & PROJECT_NAME
└──────────┬──────────┘
           │
           ├─────────────────────┐
           │                     │
           ▼                     ▼
┌──────────────────┐   ┌─────────────────────┐
│  Per-Project CSV │   │   Combined CSV      │
│ (archive/DATE_   │   │ (combined_project_  │
│  ProjectName.csv)│   │  test_cases.csv)    │
└──────────────────┘   └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ qc_form_generator.py│
                       │  (Streamlit App)    │
                       └─────────────────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │   User sees new     │
                       │ project in dropdown │
                       └─────────────────────┘
```

---

## 🎯 Key Points

### Input Location
- **Always** place raw CSV files in `preprocessed-tc/` folder
- This is where `add_new_project.py` looks for input files

### Output Locations
- **Per-project files**: `project-tc-archive/YYYYMMDD_ProjectName.csv`
  - Date-stamped for version control
  - Contains only that project's test cases

- **Combined file**: `project-tc-archive/combined_project_test_cases.csv`
  - Master file with all projects
  - Used by the Streamlit app
  - Automatically updated when you run the script

### Streamlit App
- **Local**: Run `streamlit run qc_form_generator.py`
- **Production**: https://qc-generator.streamlit.app/
- **Data source**: Always reads from `project-tc-archive/combined_project_test_cases.csv`

---

## 🔧 Example Workflow

### Scenario: Adding "Login Feature" test cases

```bash
# 1. You have a file: Login_TestCases_Dec2025.csv
# 2. Place it in preprocessed-tc/
cp Login_TestCases_Dec2025.csv preprocessed-tc/

# 3. Edit add_new_project.py
# Change:
#   INPUT_FILE = "Login_TestCases_Dec2025.csv"
#   PROJECT_NAME = "Login Feature"

# 4. Run the script
python add_new_project.py

# Output:
# ✓ Reading input file from preprocessed-tc/...
# ✓ Processing data...
# ✓ Saving per-project file to project-tc-archive/: 20251214_Login Feature.csv
# ✓ Merging with combined file in project-tc-archive/...
# ✓ Updated combined file: combined_project_test_cases.csv
# ✅ Done! Project 'Login Feature' added successfully.

# 5. Check the Streamlit app
streamlit run qc_form_generator.py
# "Login Feature" now appears in the project dropdown!
```

---

## 📁 File Management

### What to Keep
- ✅ `preprocessed-tc/` - Keep raw input files for reference
- ✅ `project-tc-archive/` - Keep all files (history + combined)

### What to Delete (optional)
- Old files in `preprocessed-tc/` after processing (if space is limited)
- But recommended to keep for backup/audit purposes

### What NOT to Delete
- ❌ `combined_project_test_cases.csv` - App needs this!
- ❌ Date-stamped files - These are your version history

---

## 🚀 Deployment Workflow

When deploying to Streamlit Cloud:

1. **GitHub Repository** must contain:
   - `qc_form_generator.py`
   - `project-tc-archive/combined_project_test_cases.csv`
   - `requirements.txt`
   - `.streamlit/config.toml`

2. **When you add new projects locally**:
   ```bash
   # After running add_new_project.py
   git add project-tc-archive/combined_project_test_cases.csv
   git add project-tc-archive/YYYYMMDD_ProjectName.csv
   git commit -m "Add [ProjectName] test cases"
   git push
   ```

3. **Streamlit Cloud auto-redeploys**:
   - Detects the push
   - Rebuilds the app
   - New project appears in production!

---

## 🔍 Troubleshooting

### Issue: Script can't find input file
**Solution**: Make sure the file is in `preprocessed-tc/` folder, not the root

### Issue: New project doesn't appear in app
**Solution**:
- Check that `combined_project_test_cases.csv` was updated
- Restart the Streamlit app (Ctrl+C, then rerun)
- Clear browser cache

### Issue: "Combined file not found"
**Solution**:
- Run the script once to create it
- Or copy an existing combined file to `project-tc-archive/`

---

## 📝 Summary

**Simple 3-step workflow:**
1. 📥 Drop CSV in `preprocessed-tc/`
2. ✏️ Edit 2 lines in `add_new_project.py`
3. ▶️ Run `python add_new_project.py`

**Everything else is automatic!** ✨
