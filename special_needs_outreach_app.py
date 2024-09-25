import streamlit as st
import pandas as pd
from model import *  # Importing the Model class from model.py
import numpy as np

def app():
    # Title and Description
    st.title("Special Needs Outreach Program")
    st.write("Special Needs Outreach Program focuses on providing dental health services for special needs individuals. This initiative is designed to improve oral health, enhance dental health awareness, and generate additional revenue for the dental clinic.")

    # Divider
    st.divider()

    # Layout using columns for a more compact design
    # with st.form("wellness_form"):
        
    st.markdown("#### Program Parameters")
    st.caption("Monthly Basis")
    # First row: Total Potential Employee and Conversion Rate
    col1, col2 = st.columns(2)
    with col1:
        # total_students = st.number_input("Total Students", step=1, value=1000)
        # total_teachers_parents = st.number_input("Total Teachers & Parents", step=1, value=500)
        total_population = st.number_input("Total Potential Customer", step=1, value=100)
        conversion_rate = st.number_input("Conversion Rate (%)", step=1, value=20)
    with col2:
        
        discount_price = st.number_input("Discount Price (%)", step=5, value=10)
        event_frequency = st.number_input("Event Frequency", step=1, value=4, help="Assumed number of events executed to reach the specified conversion rate")
    
    st.write(f"Total Joined Programs: **{total_population * conversion_rate / 100:,.0f}**")
    
    model = ModelSpecialNeedsOutreach(total_population, conversion_rate, discount_price)
        
    with st.expander("Treatment Prices & Cost", expanded=True):    
        edited_prices = st.data_editor(model.initial_price_df(), hide_index=True, column_config=
                                       {'Conversion Rate (%)': st.column_config.NumberColumn("Conversion Rate (%)", help="Conversion Rate out of Total Joined Program")})
        
    with st.expander("Event Cost", expanded = True):
        edited_event_cost = st.data_editor(model.event_cost_df, hide_index=True)
        
        # calculate total event cost by sumproduct, from edited_event_cost, column of 'Unit' and 'Cost per Unit (Rp.)'
        total_event_cost = (edited_event_cost['Unit'] * edited_event_cost['Cost per Unit (Rp.)']).sum()
        
        st.write(f"Total Event Cost (per Event): **Rp.{total_event_cost:,.0f}**")
        



    st.divider()


    st.markdown("#### Adjusted Prices")

    price_df = model.price_df(edited_prices)
    st.dataframe(price_df[['Treatment', 'Adjusted Price (Rp.)', 'Demand']], hide_index=True)
    
    if st.button("Calculate"):
        
        st.header("Financial Performance (Monthly)")

        total_revenue, total_cost, total_profit = model.calculate_financials(price_df, total_event_cost, event_frequency)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Revenue", f"Rp.{total_revenue:,.0f}")
            st.metric("Total Cost", f"Rp.{total_cost:,.0f}")


        with col2:
            st.metric("Total Profit", f"Rp.{total_profit:,.0f}")