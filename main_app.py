import streamlit as st
import pandas as pd
from model import Model  # Importing the Model class from model.py
import numpy as np

# Load treatment prices CSV to get the list of treatments
treatment_prices_df = pd.read_csv('treatment_prices.csv')
treatment_list = treatment_prices_df['Treatment'].tolist()

# Load DSP CSV
dsp_df = pd.read_csv('dsp.csv')

# Title and Description
st.title("Corporate Wellness Program")
st.write("""
The Corporate Wellness Program aims to partner with local businesses to provide comprehensive dental wellness services to their employees. This initiative is designed to improve oral health, enhance employee benefits, and generate additional revenue for the dental clinic.
""")

# Divider
st.divider()

# Layout using columns for a more compact design
with st.form("wellness_form"):
    
    st.markdown("#### Employee Wellness Program Parameters")
    # First row: Total Potential Employee and Conversion Rate
    col1, col2 = st.columns(2)
    with col1:
        total_potential_employee = st.number_input("Total Potential Employee", step=1, value=466)
    with col2:
        conversion_rate = st.number_input("Conversion Rate (%)", step=1, value=20)
        
    # Third row: Discount Package and Subscription Length
    col1, col2 = st.columns(2)
    with col1:
        discount_package = st.number_input("Discount Package (%)", step=1, value=20)
    with col2:
        subscription_length = st.number_input("Subscription Length (years)", step=1, value=1, max_value=5)
    
    # Second row: Treatment package checkboxes
    st.write("Treatment Package")
    selected_treatments = []
    cols = st.columns(2)  # Adjusted to fit two columns for compactness
    for i, treatment in enumerate(treatment_list):
        if cols[i % 2].checkbox(treatment, value=True):  # Create checkboxes for each treatment
            selected_treatments.append(treatment)
            
    st.divider()
    
    st.markdown('#### Dental Saving Plan Parameters')
    
    # DSP Editor for checkboxes, discount rate adjustments, and conversion rate adjustments
    dsp_df['Selected'] = dsp_df['Treatment'].apply(lambda x: True)  # default all selected
    dsp_df['Conversion Rate'] = dsp_df['Conversion Rate'].apply(lambda x: float(x.replace('%', '')))
    dsp_df['Discount Rate'] = dsp_df['Discount Price'].apply(lambda x: float(x.replace('%', '')))
    
    # Filtered DSP dataframe to show only Selected, Conversion Rate, and Discount Rate in the editor
    dsp_editable_df = dsp_df[['Treatment', 'Selected', 'Conversion Rate', 'Discount Rate']]
    dsp_editor = st.data_editor(dsp_editable_df, use_container_width=True, num_rows="dynamic")
    
    # Submit button
    submit_button = st.form_submit_button(label="Submit")

# If the form is submitted, create a Model instance and display the ARO calculation
if submit_button:
    # Create an instance of the Model class from model.py
    model = Model(
        total_potential_employee=total_potential_employee,
        conversion_rate=conversion_rate,
        treatments=selected_treatments,
        discount_package=discount_package,
        subscription_length=subscription_length
    )
    
    # Calculate ARO and total cost for Employee Wellness Program
    aro = model.calculate_ARO()
    total_cost = model.calculate_total_cost()
    
    # Calculate Total Joining Employee
    total_joining_employee = np.ceil(total_potential_employee * (conversion_rate / 100))
    
    # Calculate total profit generated
    total_profit = aro - total_cost
    
    # Calculate ARO and cost for DSP
    dsp_aro, dsp_cost, dsp_df_output = model.calculate_DSP(dsp_editor, total_joining_employee)
    total_dsp_profit = dsp_aro - dsp_cost
    
    # Display results using st.metric
    
    st.markdown('#### Employee Wellness Program Results')
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Display the package price per employee
        st.metric(label="Monthly Package Price/Employee", value="Rp{:,.0f}".format((aro / (subscription_length*12) / total_joining_employee)))
        st.metric(label="Additional Revenue Opportunity (ARO)", value="Rp{:,.0f}".format(aro))
        st.metric(label="Total Profit Generated", value="Rp{:,.0f}".format(total_profit))
        
    with col2:
        st.metric(label="Total Joining Employee", value=int(total_joining_employee))
        st.metric(label="Total Cost Generated", value="Rp{:,.0f}".format(total_cost))
    
    # Display DSP results below
    st.divider()
    st.markdown('#### Dental Saving Plan Results')
    
    # Display DSP DataFrame with joining customers, total revenue, and total cost
    st.dataframe(dsp_df_output, hide_index=True)
    
    # Grand totals for DSP
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total DSP Revenue", value="Rp{:,.0f}".format(dsp_aro))
    with col2:
        st.metric(label="Total DSP Cost", value="Rp{:,.0f}".format(dsp_cost))
    with col3:
        st.metric(label="Total DSP Profit", value="Rp{:,.0f}".format(total_dsp_profit))


    st.divider()

    st.markdown('## Overall Results')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Revenue", value="Rp{:,.0f}".format(aro + dsp_aro))
        
    with col2:
        st.metric(label="Total Cost", value="Rp{:,.0f}".format(total_cost + dsp_cost))
        
    with col3:
        st.metric(label="Total Profit", value="Rp{:,.0f}".format(total_profit + total_dsp_profit))
