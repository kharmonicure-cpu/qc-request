# QC Request Form Generator - Handover Package

## What's in This Package

This folder contains everything needed to maintain and operate the QC Request Form Generator application.

### Documentation
- **`HANDOVER_DOCUMENT.md`** - Complete English documentation
- **`HANDOVER_DOCUMENT_KR.md`** - Complete Korean documentation (음슴체)
- **`QUICK_START.md`** - Quick reference guide for common tasks

### Sample Files
- **`sample_input.csv`** - Example of properly formatted input file
- **`input_template.xlsx`** - Excel template for creating new test cases

### Scripts
- **`add_new_project.py`** - Simplified script for adding new projects (just update variables at top)
- **`verify_data.py`** - Script to verify your processed data is correct

### Deployment Files
- **`requirements.txt`** - Python dependencies for Streamlit Cloud
- **`.streamlit/config.toml`** - Streamlit configuration file
- **`.gitignore`** - Git ignore file for version control
- **`DEPLOYMENT_GUIDE.md`** - Complete deployment instructions (English)
- **`DEPLOYMENT_GUIDE_KR.md`** - Complete deployment instructions (Korean)

---

## For New Maintainers

**Start here:**
1. Read `QUICK_START.md` for the most common task (adding new test cases)
2. Read `DEPLOYMENT_CHECKLIST.md` if you need to deploy to Streamlit Cloud
3. Refer to `HANDOVER_DOCUMENT.md` or `HANDOVER_DOCUMENT_KR.md` for full details
4. Use `sample_input.csv` as a reference when preparing your input files

**Production App**: https://qc-generator.streamlit.app/

**New to Streamlit Cloud?** Follow `DEPLOYMENT_GUIDE.md` (English) or `DEPLOYMENT_GUIDE_KR.md` (Korean) for step-by-step deployment instructions.

---

## Quick Command Reference

```bash
# Add new project (after updating variables in the script)
python add_new_project.py

# Verify the output
python verify_data.py

# Run locally
streamlit run qc_form_generator.py
```

---

## Need Help?
Contact the PM team or refer to the detailed documentation files in this package.
