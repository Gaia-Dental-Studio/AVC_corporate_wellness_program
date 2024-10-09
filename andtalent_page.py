import streamlit as st
import pandas as pd

def app():
    # Title and Description
    st.title("Talent Dashboard")
    st.image("andtalent_logo.png", width=500)

    st.write("**Hiring Minimum Hour a Week**: Total cumulative hours per week in accomodating client needs, irrespective the number of dentist composing the total hours")
    st.write("**Fee per Hour per Dentist (Rp.)**: Fee per hour per dentist that client needs to pay")

    hiring_df = pd.DataFrame({'Hiring Minimum Hour a Week': [0, 10, 30, 50], 'Fee per Hour per Dentist (Rp.)': [150000, 140000, 120000, 110000]})
    st.data_editor(hiring_df, hide_index=True)   

    if st.button("Update Price List to Client"):
        st.success("Price List Updated to Client")
        hiring_df.to_csv('andtalent_pricing.csv', index=False)