import pandas as pd
import numpy as np

class Model:
    def __init__(self, total_potential_employee, conversion_rate, treatments, discount_package, subscription_length):
        self.total_potential_employee = total_potential_employee
        self.conversion_rate = conversion_rate
        self.treatments = treatments
        self.discount_package = discount_package
        self.subscription_length = subscription_length
        
        self.total_joining_employee = np.ceil(total_potential_employee * (conversion_rate / 100))
        
        # Load treatment prices CSV
        self.prices_df = pd.read_csv('treatment_prices.csv')
        
        # Load treatment costs CSV
        self.costs_df = pd.read_csv('treatment_costs.csv')
    
    def calculate_ARO(self):
        # Get the price of selected treatments
        selected_treatments = self.treatments
        
        # Summing the prices of selected treatments
        total_price = self.prices_df[self.prices_df['Treatment'].isin(selected_treatments)]['Price'].apply(self._convert_price).sum()
        
        # Calculate ARO
        aro = (total_price * self.total_joining_employee
               * (100 - self.discount_package) / 100 * (self.subscription_length * 12))
        
        return aro
    
    def calculate_total_cost(self):
        # Get the cost of selected treatments
        selected_treatments = self.treatments
        
        # Summing the costs of selected treatments
        treatment_cost = self.costs_df[self.costs_df['Component'].isin(selected_treatments)]['Cost'].apply(self._convert_price).sum()
        
        # Add dentist fee and monthly cost/employee (multiplied by subscription length in months)
        dentist_fee = self.prices_df[self.prices_df['Treatment'].isin(selected_treatments)]['Price'].apply(self._convert_price).sum() * ((100 - self.discount_package) / 100 ) * 0.1 
        
        card_fee = self.costs_df[self.costs_df['Component'] == 'Member Card (monthly)']['Cost'].apply(self._convert_price).values[0]
        
        # Total cost is the sum of treatment cost, dentist fee, and monthly cost/employee
        total_cost_per_employee = dentist_fee + card_fee + treatment_cost
        
        total_cost = (total_cost_per_employee * self.total_joining_employee
                * (self.subscription_length * 12))
        
        return total_cost

    def calculate_DSP(self, dsp_editor_df, total_joining_employee):
        # Use the original dsp_df for Price and Cost Material
        dsp_original_df = pd.read_csv('dsp.csv')
        
        # Get the selected DSP treatments and their conversion rates from the edited DSP editor
        dsp_selected = dsp_editor_df[dsp_editor_df['Selected'] == True]
        
        print(total_joining_employee)
        
        total_dsp_aro = 0
        total_dsp_cost = 0
        
        dsp_output_data = {
            "Treatment": [],
            "Joining Customers": [],
            "Total Revenue": [],
            "Total Cost": []
        }
        
        # Iterate through the selected rows in dsp_editor_df, but use dsp_original_df for Price and Cost Material
        for _, row in dsp_selected.iterrows():
            treatment_name = row['Treatment']
            dsp_conversion_rate = row['Conversion Rate'] / 100
            
            # Cross-reference with original dsp_df to get Price and Cost Material
            original_row = dsp_original_df[dsp_original_df['Treatment'] == treatment_name].iloc[0]
            dsp_price = self._convert_price(original_row['Price'])
            dsp_cost_material = self._convert_price(original_row['Cost Material'])
            dsp_dentist_fee = self._convert_price(original_row['Price']) * 0.1
            
            dsp_total_joining = np.ceil(total_joining_employee * dsp_conversion_rate)
            
            # DSP ARO and cost calculations
            dsp_aro = dsp_price * dsp_total_joining
            dsp_cost = (dsp_cost_material + dsp_dentist_fee) * dsp_total_joining
            
            total_dsp_aro += dsp_aro
            total_dsp_cost += dsp_cost
            
            # Add row to output data
            dsp_output_data["Treatment"].append(treatment_name)
            dsp_output_data["Joining Customers"].append(int(dsp_total_joining))
            dsp_output_data["Total Revenue"].append(int(dsp_aro))
            dsp_output_data["Total Cost"].append(int(dsp_cost))
        
        # Create a DataFrame for output
        dsp_df_output = pd.DataFrame(dsp_output_data)
        
        return total_dsp_aro, total_dsp_cost, dsp_df_output

    def _convert_price(self, price):
        """Helper function to convert price from string to integer."""
        return int(price.replace('Rp', '').replace('.', '').replace(',', '').strip())
