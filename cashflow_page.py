import streamlit as st
import pandas as pd
from cashflow.cashflow_plot import ModelCashflow
import os

@st.cache_data
def load_company_data(file_path):
    return pd.read_csv(file_path)

def app():
    # Initialize the cashflow model
    cashflow_model = ModelCashflow()

    # Streamlit app title
    st.title("Cashflow Visualization Dashboard")

    # Short description
    st.write("""
    This dashboard allows you to visualize the cashflow of different companies. 
    You can select which companies to include in the visualization by using the checkboxes below.
    """)

    # Checkbox for company 1 and company 2
    company_1_checked = st.checkbox('Corporate Wellness', value=True)
    company_2_checked = st.checkbox('School Outreach', value=True)

    # Load company data using caching
    df1 = load_company_data('corporate_cashflow.csv')
    df2 = load_company_data('school_cashflow.csv')

    # Function to update the cashflow model
    def update_cashflow_model():
        cashflow_model.remove_all_companies()
        if company_1_checked:
            cashflow_model.add_company_data('Corporate Wellness', df1)
        if company_2_checked:
            cashflow_model.add_company_data('School Outreach', df2)

    # Create a placeholder for the plot to be updated later
    cashflow_plot_placeholder = st.empty()

    # Initially update the cashflow model and plot
    update_cashflow_model()
    cashflow_plot_placeholder.plotly_chart(cashflow_model.cashflow_plot())

    # # Button to update the cashflow
    # if st.button('Update'):
    #     # Update the cashflow model based on current selections
    #     update_cashflow_model()
    #     # Update the existing plot in the placeholder
    #     cashflow_plot_placeholder.plotly_chart(cashflow_model.cashflow_plot())
    
    combined_df, avg_total_revenue, avg_total_expense = cashflow_model.combine_and_average()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Average Revenue per Month", f"Rp.{avg_total_revenue:,.0f}")
    with col2:
        st.metric("Average Expense per Month", f"Rp.{avg_total_expense:,.0f}")
        
        
    scenario_metrics = [avg_total_revenue, avg_total_expense]
    
    # Filepath for saving scenarios
    csv_file_path = 'scenario_metrics.csv'

    # Function to save the scenario_metrics_dict to a CSV file
    def save_scenarios_to_csv(scenario_dict, file_path):
        df = pd.DataFrame.from_dict(scenario_dict, orient='index', columns=['Avg Total Revenue', 'Avg Total Expense'])
        df.index.name = 'Scenario'
        df.to_csv(file_path)

    # Function to load scenarios from a CSV file
    def load_scenarios_from_csv(file_path):
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, index_col='Scenario')
            return df.to_dict(orient='index')
        return {}

    # Load scenarios from the CSV file into session_state
    if 'scenario_metrics_dict' not in st.session_state:
        st.session_state['scenario_metrics_dict'] = load_scenarios_from_csv(csv_file_path)
    

    # Add a scenario to the dictionary when the button is clicked
    if st.button("Save Cashflow Scenario for Comparison"):
        # Determine the next key to use (incremental based on existing keys)
        next_key = len(st.session_state['scenario_metrics_dict']) + 1
        # Add the new scenario to the dictionary
        st.session_state['scenario_metrics_dict'][next_key] = scenario_metrics
        # Save the updated dictionary to CSV
        save_scenarios_to_csv(st.session_state['scenario_metrics_dict'], csv_file_path)
        st.success(f"Scenario {next_key} saved.")

    # # Display the current saved scenarios
    # st.write("Current Scenarios:")
    # st.write(st.session_state['scenario_metrics_dict'])

    st.divider()

    # Reset all scenarios
    if st.button("Reset All Scenario"):
        # Clear session state and remove CSV file
        st.session_state['scenario_metrics_dict'] = {}
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)
        st.success("All scenarios have been erased.")
        
    comparison_matrix = cashflow_model.create_profit_comparison_matrix(st.session_state['scenario_metrics_dict'])
    
    st.dataframe(comparison_matrix)