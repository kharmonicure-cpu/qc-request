from collections import defaultdict
import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path

# ========================================
# QC Request Form Generator
# ========================================
# Run locally with: streamlit run qc_form_generator.py
# Deployed at: https://qc-generator.streamlit.app/
# ========================================

# Setup paths
SCRIPT_DIR = Path(__file__).parent
DATA_FILE = SCRIPT_DIR / "project-tc-archive" / "combined_project_test_cases.csv"

# Load test case dataset with caching
@st.cache_data
def load_data():
    """Load and cache the test case data"""
    try:
        df = pd.read_csv(DATA_FILE)
        df.columns = df.columns.str.strip()
        return df
    except FileNotFoundError:
        st.error(f"❌ Data file not found: {DATA_FILE}")
        st.info("Please ensure 'combined_project_test_cases.csv' exists in the project-tc-archive folder.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

df = load_data()

# Define available devices
available_devices = [
    'Android Mobile', 'Apple Mobile', 'Android TV', 'Apple TV',
    'Fire TV', 'Roku', 'Web', 'Smart TV', 'Vizio TV'
]
available_regions = ["All Regions", "NA", "LATAM", "EU", "OCD", "BRL"]

# ========================================
# UI Components
# ========================================

st.title("QC Request Form Generator")

# 0. Project Selection
st.subheader("Project")
project_options = sorted(df.project_name.dropna().unique())
selected_project = st.selectbox("Select Project", ["Select a project..."] + project_options, index=0)

# 0.1 Filter by selected project
df_project = df[df.project_name == selected_project]

# 1. Basic Info
st.subheader("Basic Information")
request_date = date.today()
st.markdown(f"**Request Date:** {request_date}")
requester = st.text_input("Requester")
target_qc = st.selectbox("Target Device for QC", ["Select a device..."] + available_devices)
selected_regions = st.multiselect(
    "Target Region(s)",
    available_regions,
    default=["All Regions"]
)
if "All Regions" in selected_regions:
    selected_regions = ["All Regions"]
version = st.text_input("Version", placeholder="ex) 4.0.0")
test_env = st.selectbox("Test Environment", ["Staging", "Production", "Live"])

# Map test environment to short form
test_env_map = {
    "Staging": "STG",
    "Production": "PROD",
    "Live": "LIVE"
}
test_env_print = test_env_map.get(test_env, test_env)

# 2. Type Info
st.subheader("Type & Metadata")
qc_type = st.selectbox("Type for QC", ["New", "Bug Fix", "Routine", "Other"])
qc_round = st.selectbox("Round", list(range(1, 11)))
urgency = st.selectbox("Urgency Level", ["Normal", "Urgent"])
reference_doc = st.text_input("Reference Document (URL)", placeholder="Link to the relevant Zeplin Page Reference or Dashboard")
build_link = st.text_input("Build Download Link (URL)", placeholder="If applicable, please copy/paste the link to download the test build")

# 3. Scope of Development & Tests
st.subheader("Scope of Development")

selected_scope_tree = []
selected_tests = []

if target_qc != "Select a device...":
    # Filter based on selected device
    df_filtered = df_project[df_project[target_qc] == True].copy()

    global_select_all = False
    if qc_round == 1:
        # Add this before the loop that iterates over main categories
        global_select_all = st.checkbox("✅ Select ALL Components from ALL Categories (First QC Run)")

    if global_select_all:
        for main_cat in sorted(df_filtered['main_category'].unique()):
            selected_scope_tree.append(f"All Components under '{main_cat}'\n")
    else:
        for main_cat in sorted(df_filtered['main_category'].unique()):
            with st.expander(main_cat):
                cat_df = df_filtered[df_filtered['main_category'] == main_cat]
                select_all = st.checkbox(
                    "✅ Select all components",
                    key=f"{main_cat}_select"
                )

                # If user checks the "Select all components" box for this main category...
                if select_all:
                    # Add a simplified message instead of listing every component individually
                    selected_scope_tree.append(f"All Components under '{main_cat}'\n")

                    # Iterate through all rows/components under this main category
                    for _, row in cat_df.iterrows():
                        comp = row['scope_of_dev']

                        # Split the test_case string into a clean list (by newline or comma)
                        test_cases = [tc.strip() for tc in row['test_case'].splitlines() if tc.strip()]

                        # Store as a tuple to keep track of which test cases belong to which component
                        selected_tests.append((comp, test_cases))

                # If user is manually selecting components one by one...
                else:
                    for _, row in cat_df.iterrows():
                        comp = row['scope_of_dev']

                        # Prepare test cases (split + strip like above)
                        test_cases = [tc.strip() for tc in row['test_case'].splitlines() if tc.strip()]

                        # Create a unique key to persist checkbox state
                        comp_key = f"{main_cat}_{comp}"

                        # If this specific component is checked...
                        if st.checkbox(f"{comp}", key=comp_key):
                            # Add to scope tree as "Main > Component"
                            selected_scope_tree.append(f"{main_cat} > {comp}")

                            # Track associated test cases
                            selected_tests.append((comp, test_cases))


grouped_tests = defaultdict(set)
for comp, test_list in selected_tests:
    grouped_tests[comp].update(test_list)

included_formatted = ""
for comp in sorted(grouped_tests):
    included_formatted += f"<b>{comp}</b><br>\n"
    for tc in sorted(grouped_tests[comp]):
        included_formatted += f"- {tc}<br>\n"

# 4. Format Scope of Development
grouped_scope = defaultdict(list)

for entry in selected_scope_tree:
    if entry.startswith("All Components under"):
        # Special case: full category selected
        cat_name = entry.split("'")[1]  # get the main_cat name
        grouped_scope[cat_name].append(entry)
    else:
        main_cat, comp = entry.split(" > ", 1)
        grouped_scope[main_cat].append(f"* {comp}")

# Format into markdown-style bullet groupings
development_scope_formatted = ""
for main_cat in sorted(grouped_scope):
    development_scope_formatted += f"<b>{main_cat}</b><br>\n"
    for item in grouped_scope[main_cat]:
        development_scope_formatted += f"{item}<br>\n"
    development_scope_formatted += "<br>\n"  # line break between sections

ticket_title = f"[QC] {target_qc} v{version} ({qc_round}) - {test_env_print} Round {qc_round} {selected_project}"

# ========================================
# Generate Output
# ========================================
st.subheader("Generated QC Request Form")
if st.button("Generate QC Form"):
    if target_qc == "Select a device...":
        st.error("Please select a valid target device before generating the form.")
    else:
        st.markdown(f"**QTM Jira Ticket Title**:")
        st.markdown(f"{ticket_title}")
        html_output = f"""
        <table>
            <tr><th>Field</th><th>Value</th></tr>
            <tr><td valign="top">Request Date</td><td>{request_date}</td></tr>
            <tr><td valign="top">Requester</td><td>{requester}</td></tr>
            <tr><td valign="top">Target Device</td><td>{target_qc}</td></tr>
            <tr><td valign="top">Region</td><td>{selected_regions}</td></tr>
            <tr><td valign="top">Version</td><td>{version}_{qc_round}</td></tr>
            <tr><td valign="top">Task Name</td><td>{selected_project}</td></tr>
            <tr><td valign="top">Test Environment</td><td>{test_env}</td></tr>
            <tr><td valign="top">Type for QC</td><td>{qc_type} Round {qc_round}</td></tr>
            <tr><td valign="top">Urgency Level</td><td>{urgency}</td></tr>
            <tr><td valign="top">Reference Document</td><td>{reference_doc}</td></tr>
            <tr><td valign="top">Build Download Link</td><td>{build_link}</td></tr>
            <tr><td valign="top">Scope of Development</td><td>{development_scope_formatted}</td></tr>
            <tr><td valign="top">Excluded from Tests</td><td>**해당 시 직접 기입해주시기 바랍니다.**</td></tr>
        </table>
        """
        st.markdown(html_output, unsafe_allow_html=True)
        st.success("✅ QC Request Form Generated! Copy it to your Jira ticket.")
