# Streamlit Cloud Deployment Checklist

Use this checklist when deploying the QC Form Generator to Streamlit Cloud.

---

## Pre-Deployment Checklist

### GitHub Repository Setup
- [ ] Create GitHub account (if not already done)
- [ ] Create new repository on GitHub
- [ ] Repository name: `qc-generator` (or your choice)
- [ ] Repository visibility: Public (or Private with Streamlit access)

### Files to Include in Repository
- [ ] `qc_form_generator.py` - Main app file
- [ ] `requirements.txt` - Python dependencies
- [ ] `.streamlit/config.toml` - Streamlit config
- [ ] `.gitignore` - Git ignore rules
- [ ] `processed-data/combined_project_test_cases.csv` - Your data
- [ ] `README.md` (optional but recommended)

### Verify File Paths
- [ ] Open `qc_form_generator.py`
- [ ] Check line 9: CSV path should be **relative**, not absolute
- [ ] Correct format: `"qc-request/processed-data/combined_project_test_cases.csv"`
- [ ] Or if at root: `"processed-data/combined_project_test_cases.csv"`

---

## Deployment Steps

### Step 1: Push to GitHub
```bash
# Initialize git
[ ] git init

# Add all files
[ ] git add .

# Create first commit
[ ] git commit -m "Initial commit: QC Form Generator"

# Connect to GitHub
[ ] git remote add origin https://github.com/YOUR_USERNAME/qc-generator.git

# Push to GitHub
[ ] git branch -M main
[ ] git push -u origin main
```

### Step 2: Streamlit Cloud Setup
- [ ] Go to https://share.streamlit.io/
- [ ] Click "Sign up" with GitHub
- [ ] Authorize Streamlit to access your repositories

### Step 3: Deploy App
- [ ] Click "New app" button
- [ ] Select repository: `YOUR_USERNAME/qc-generator`
- [ ] Select branch: `main`
- [ ] Main file path: `qc-request/qc_form_generator.py`
- [ ] (Optional) Custom URL: `qc-generator`
- [ ] Click "Deploy!"

### Step 4: Wait for Deployment
- [ ] Watch deployment logs
- [ ] Wait for "Your app is live!" message
- [ ] Should take 2-5 minutes

---

## Post-Deployment Verification

### Test the App
- [ ] Open the app URL (e.g., https://qc-generator.streamlit.app/)
- [ ] Check that projects load in dropdown
- [ ] Select a project
- [ ] Select a device (e.g., "Android Mobile")
- [ ] Verify components appear
- [ ] Select some components
- [ ] Click "Generate QC Form"
- [ ] Verify form generates correctly

### Check for Errors
- [ ] No error messages in the app
- [ ] All dropdowns work
- [ ] Data loads correctly
- [ ] Form output is formatted properly

---

## Common Issues During Deployment

| Issue | Quick Fix |
|-------|-----------|
| "File not found" error | Check CSV path in line 9 of qc_form_generator.py |
| "Module not found" | Verify requirements.txt is in repository root |
| Empty dropdown | Check CSV file is committed and pushed to GitHub |
| Old data showing | Clear browser cache or reboot app |
| Repository access denied | Make repo public or grant Streamlit access |

---

## Updating After Deployment

### When You Add New Test Cases:
```bash
# 1. Update combined_project_test_cases.csv locally
[ ] Run add_new_project.py

# 2. Commit and push
[ ] git add processed-data/combined_project_test_cases.csv
[ ] git commit -m "Add [Project Name] test cases"
[ ] git push

# 3. Wait for auto-redeploy (1-2 minutes)
[ ] Check app URL to verify new project appears
```

---

## Access Information

After deployment, save this information:

**App URL:** `https://_____________________________.streamlit.app/`

**GitHub Repository:** `https://github.com/_____________/______________`

**Streamlit Dashboard:** `https://share.streamlit.io/`

**Deployed on:** ____/____/______

**Deployed by:** _____________________

---

## Handover to Next Person

When transferring to another team member:

### Option A: Transfer Repository
- [ ] Go to GitHub repo Settings
- [ ] Scroll to "Transfer ownership"
- [ ] Transfer to new owner's GitHub account
- [ ] New owner redeploys on their Streamlit account

### Option B: Add Collaborator
- [ ] Go to GitHub repo Settings → Collaborators
- [ ] Add new person's GitHub username
- [ ] Grant "Write" access
- [ ] They can now push updates (app auto-redeploys)

---

## Emergency Contacts

**Streamlit Support:** https://discuss.streamlit.io/
**GitHub Help:** https://docs.github.com/

**Documentation:**
- Read `DEPLOYMENT_GUIDE.md` for full instructions
- Read `DEPLOYMENT_GUIDE_KR.md` for Korean instructions

---

## Notes

Use this space for deployment-specific notes:

```
Date: ____________
Notes:
_________________________________________________
_________________________________________________
_________________________________________________
_________________________________________________
```
