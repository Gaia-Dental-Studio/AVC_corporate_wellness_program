import streamlit as st
from streamlit_navigation_bar import st_navbar
import corporate_wellness_app
import school_outreach_app
import agecare_outreach_app
import special_needs_outreach_app

# Create navigation bar with two options
selection = st_navbar(["Corporate Wellness", "School Outreach", "Age Care Outreach", "Special Needs Outreach"])

if selection == "Corporate Wellness":
    corporate_wellness_app.app()

elif selection == "School Outreach":

    school_outreach_app.app()
    
elif selection == "Age Care Outreach":
    agecare_outreach_app.app()  
    
elif selection == "Special Needs Outreach":
    special_needs_outreach_app.app()        