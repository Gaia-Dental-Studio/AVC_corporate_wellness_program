import streamlit as st
import corporate_wellness_app
import school_outreach_app
import agecare_outreach_app
import special_needs_outreach_app
import cashflow_page

# Create sidebar navigation with four options
selection = st.sidebar.selectbox(
    "Select Page",
    ["Corporate Wellness", "School Outreach", "Age Care Outreach", "Special Needs Outreach", "Cashflow"]
)

# Display the selected app based on sidebar navigation
if selection == "Corporate Wellness":
    corporate_wellness_app.app()

elif selection == "School Outreach":
    school_outreach_app.app()

elif selection == "Age Care Outreach":
    agecare_outreach_app.app()

elif selection == "Special Needs Outreach":
    special_needs_outreach_app.app()

elif selection == "Cashflow":
    cashflow_page.app()
