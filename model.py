import pandas as pd
import numpy as np

class ModelCorporateWellness:
    def __init__(self, total_potential_employee, conversion_rate, treatments, discount_package, subscription_length):
        self.total_potential_employee = total_potential_employee
        self.conversion_rate = conversion_rate
        self.treatments = treatments
        self.discount_package = discount_package
        self.subscription_length = subscription_length
        
        self.total_joining_employee = np.ceil(total_potential_employee * (conversion_rate / 100))
        
        # Load treatment prices CSV
        self.prices_df = pd.read_csv(r'corporate_wellness_data\treatment_prices.csv')
        
        # Load treatment costs CSV
        self.costs_df = pd.read_csv(r'corporate_wellness_data\treatment_costs.csv')
    
    def calculate_ARO(self, treatment_price_df=None, treatment_cost_df=None):
        # Get the price of selected treatments
        selected_treatments = self.treatments

        
        if treatment_price_df is not None:
            # Use the edited treatment prices DataFrame
            self.prices_df = treatment_price_df
        
        # Summing the prices of selected treatments
        total_price = self.prices_df[self.prices_df['Treatment'].isin(selected_treatments)]['Price (Rp.)'].sum()
        
        # Calculate ARO
        aro = (total_price * self.total_joining_employee
               * (100 - self.discount_package) / 100 * (self.subscription_length * 12))
        
        return aro
    
    def calculate_total_cost(self, treatment_price_df=None, treatment_cost_df=None):
        
        if treatment_price_df is not None:
            # Use the edited treatment prices DataFrame
            self.prices_df = treatment_price_df
            
        if treatment_cost_df is not None:
            # Use the edited treatment costs DataFrame
            self.costs_df = treatment_cost_df
        
        # Get the cost of selected treatments
        selected_treatments = self.treatments
        
        # Summing the costs of selected treatments
        treatment_cost = self.costs_df[self.costs_df['Component'].isin(selected_treatments)]['Cost (Rp.)'].sum()
        
        # Add dentist fee and monthly cost/employee (multiplied by subscription length in months)
        dentist_fee = self.prices_df[self.prices_df['Treatment'].isin(selected_treatments)]['Price (Rp.)'].sum() * ((100 - self.discount_package) / 100) * 0.1 
        
        card_fee = self.costs_df[self.costs_df['Component'] == 'Member Card (monthly)']['Cost (Rp.)'].values[0]
        
        # Total cost is the sum of treatment cost, dentist fee, and monthly cost/employee
        total_cost_per_employee = dentist_fee + card_fee + treatment_cost
        
        total_cost = (total_cost_per_employee * self.total_joining_employee
                      * (self.subscription_length * 12))
        
        return total_cost

    def calculate_DSP(self, dsp_editor_df, total_joining_employee):
        # Use the original dsp_df for Original Price and Cost Material
        # dsp_original_df = pd.read_csv('dsp.csv')
        
        
        
        # Get the selected DSP treatments and their conversion rates and discount rates from the edited DSP editor
        dsp_selected = dsp_editor_df[dsp_editor_df['Selected'] == True]
        
        dsp_original_df = dsp_selected # we will use the selected as it needs to be editable
        
        total_dsp_aro = 0
        total_dsp_cost = 0
        
        dsp_output_data = {
            "Treatment": [],
            "Joining Customers": [],
            "Total Revenue (Rp.)": [],
            "Total Cost (Rp.)": []
        }
        
        # Iterate through the selected rows in dsp_editor_df, but use dsp_original_df for Original Price and Cost Material
        for _, row in dsp_selected.iterrows():
            treatment_name = row['Treatment']
            dsp_conversion_rate = row['Conversion Rate (%)'] / 100
            discount_rate = row['Discount Price (%)'] / 100
            
            # Cross-reference with original dsp_df to get Original Price and Cost Material
            original_row = dsp_original_df[dsp_original_df['Treatment'] == treatment_name].iloc[0]
            original_price = original_row['Original Price (Rp.)']
            dsp_cost_material = original_row['Cost Material (Rp.)']
            dsp_dentist_fee = original_row['Dentist Fee (Rp.)']
            
            # Calculate the new discounted price
            dsp_price = original_price * (1 - discount_rate)
            
            dsp_total_joining = np.ceil(total_joining_employee * dsp_conversion_rate)
            
            # DSP ARO and cost calculations
            dsp_aro = dsp_price * dsp_total_joining
            dsp_cost = (dsp_cost_material + dsp_dentist_fee) * dsp_total_joining
            
            total_dsp_aro += dsp_aro
            total_dsp_cost += dsp_cost
            
            # Add row to output data
            dsp_output_data["Treatment"].append(treatment_name)
            dsp_output_data["Joining Customers"].append(int(dsp_total_joining))
            dsp_output_data["Total Revenue (Rp.)"].append(int(dsp_aro))
            dsp_output_data["Total Cost (Rp.)"].append(int(dsp_cost))
        
        # Create a DataFrame for output
        dsp_df_output = pd.DataFrame(dsp_output_data)
        
        return total_dsp_aro, total_dsp_cost, dsp_df_output

    # def _convert_price(self, price):
    #     """Helper function to convert price from string to integer."""
    #     return int(price.replace('Rp', '').replace('.', '').replace(',', '').strip())




class ModelSchoolOutreach:
    def __init__(self, total_students, total_teachers_parents, conversion_rate, discount_price):
        self.total_students = total_students
        self.total_teachers_parents = total_teachers_parents
        self.total_population = total_students + total_teachers_parents
        self.conversion_rate = conversion_rate
        self.discount_price = discount_price
        self.total_joined = self.total_population * (self.conversion_rate / 100)
        
        
        # Load the treatment prices CSV
        self.treatment_prices_df = pd.read_csv(r'school_outreach_data\treatment_prices.csv')
        self.event_cost_df = pd.read_csv(r'school_outreach_data\event_cost.csv')

    
    def initial_price_df(self):
        df = self.treatment_prices_df.copy()
        df['Discount Price (%)'] = self.discount_price
        return df
        
    
    
    def price_df(self, df):
        # Adjust prices based on discount price
        df['Adjusted Price (Rp.)'] = df['Original Price (Rp.)'] * ( 1 -  (df['Discount Price (%)'] / 100))
        
        
        
        # Create the DataFrame with necessary columns
        price_df = df.copy()
        price_df['Adjusted Price (Rp.)'] = df['Adjusted Price (Rp.)']
        price_df['Demand'] = np.ceil(self.total_joined * (df['Conversion Rate (%)'] / 100))
        # price_df = price_df[['Treatment', 'Adjusted Price (Rp.)', 'Demand']]
        
        return price_df
    
    def calculate_financials(self, price_df, total_event_cost, event_frequency):
        # Calculate total revenue for each treatment
        price_df['Total Revenue (Rp.)'] = price_df['Adjusted Price (Rp.)'] * price_df['Demand']
        
        # Calculate total cost for each treatment (Cost Material + Dentist Fee) * Demand
        price_df['Total Cost (Rp.)'] = (price_df['Cost Material (Rp.)'] + price_df['Dentist Fee (Rp.)']) * price_df['Demand']
        
        # Calculate total profit for each treatment (Total Revenue - Total Cost)
        price_df['Total Profit (Rp.)'] = price_df['Total Revenue (Rp.)'] - price_df['Total Cost (Rp.)']
        
        # Sum total revenue, total cost, and total profit across all treatments
        total_revenue = price_df['Total Revenue (Rp.)'].sum()
        total_cost = price_df['Total Cost (Rp.)'].sum() + total_event_cost * event_frequency
        total_profit = price_df['Total Profit (Rp.)'].sum()

        # Return the overall financials and the price_df with detailed calculations
        return total_revenue, total_cost, total_profit
    
    def initial_event_cost_df(self):
        
        return self.event_cost_df



class ModelAgecareOutreach:
    def __init__(self, total_population, conversion_rate, discount_price):

        self.total_population = total_population
        self.conversion_rate = conversion_rate
        self.discount_price = discount_price
        self.total_joined = self.total_population * (self.conversion_rate / 100)
        
        
        # Load the treatment prices CSV
        self.treatment_prices_df = pd.read_csv(r'agecare_outreach_data\treatment_prices.csv')
        self.event_cost_df = pd.read_csv(r'agecare_outreach_data\event_cost.csv')

    
    def initial_price_df(self):
        df = self.treatment_prices_df.copy()
        df['Discount Price (%)'] = self.discount_price
        return df
        
    
    
    def price_df(self, df):
        # Adjust prices based on discount price
        df['Adjusted Price (Rp.)'] = df['Original Price (Rp.)'] * ( 1 -  (df['Discount Price (%)'] / 100))
        
        
        
        # Create the DataFrame with necessary columns
        price_df = df.copy()
        price_df['Adjusted Price (Rp.)'] = df['Adjusted Price (Rp.)']
        price_df['Demand'] = np.ceil(self.total_joined * (df['Conversion Rate (%)'] / 100))
        # price_df = price_df[['Treatment', 'Adjusted Price (Rp.)', 'Demand']]
        
        return price_df
    
    def calculate_financials(self, price_df, total_event_cost, event_frequency):
        # Calculate total revenue for each treatment
        price_df['Total Revenue (Rp.)'] = price_df['Adjusted Price (Rp.)'] * price_df['Demand']
        
        # Calculate total cost for each treatment (Cost Material + Dentist Fee) * Demand
        price_df['Total Cost (Rp.)'] = (price_df['Cost Material (Rp.)'] + price_df['Dentist Fee (Rp.)']) * price_df['Demand']
        
        # Calculate total profit for each treatment (Total Revenue - Total Cost)
        price_df['Total Profit (Rp.)'] = price_df['Total Revenue (Rp.)'] - price_df['Total Cost (Rp.)']
        
        # Sum total revenue, total cost, and total profit across all treatments
        total_revenue = price_df['Total Revenue (Rp.)'].sum()
        total_cost = price_df['Total Cost (Rp.)'].sum() + total_event_cost * event_frequency
        total_profit = price_df['Total Profit (Rp.)'].sum()

        # Return the overall financials and the price_df with detailed calculations
        return total_revenue, total_cost, total_profit
    
    def initial_event_cost_df(self):
        
        return self.event_cost_df
    
    
class ModelSpecialNeedsOutreach:
    def __init__(self, total_population, conversion_rate, discount_price):

        self.total_population = total_population
        self.conversion_rate = conversion_rate
        self.discount_price = discount_price
        self.total_joined = self.total_population * (self.conversion_rate / 100)
        
        
        # Load the treatment prices CSV
        self.treatment_prices_df = pd.read_csv(r'special_needs_outreach_data\treatment_prices.csv')
        self.event_cost_df = pd.read_csv(r'special_needs_outreach_data\event_cost.csv')

    
    def initial_price_df(self):
        df = self.treatment_prices_df.copy()
        df['Discount Price (%)'] = self.discount_price
        return df
        
    
    
    def price_df(self, df):
        # Adjust prices based on discount price
        df['Adjusted Price (Rp.)'] = df['Original Price (Rp.)'] * ( 1 -  (df['Discount Price (%)'] / 100))
        
        
        
        # Create the DataFrame with necessary columns
        price_df = df.copy()
        price_df['Adjusted Price (Rp.)'] = df['Adjusted Price (Rp.)']
        price_df['Demand'] = np.ceil(self.total_joined * (df['Conversion Rate (%)'] / 100))
        # price_df = price_df[['Treatment', 'Adjusted Price (Rp.)', 'Demand']]
        
        return price_df
    
    def calculate_financials(self, price_df, total_event_cost, event_frequency):
        # Calculate total revenue for each treatment
        price_df['Total Revenue (Rp.)'] = price_df['Adjusted Price (Rp.)'] * price_df['Demand']
        
        # Calculate total cost for each treatment (Cost Material + Dentist Fee) * Demand
        price_df['Total Cost (Rp.)'] = (price_df['Cost Material (Rp.)'] + price_df['Dentist Fee (Rp.)'] + price_df['Sedation Cost (Rp.)']) * price_df['Demand']
        
        # Calculate total profit for each treatment (Total Revenue - Total Cost)
        price_df['Total Profit (Rp.)'] = price_df['Total Revenue (Rp.)'] - price_df['Total Cost (Rp.)']
        
        # Sum total revenue, total cost, and total profit across all treatments
        total_revenue = price_df['Total Revenue (Rp.)'].sum()
        total_cost = price_df['Total Cost (Rp.)'].sum() + total_event_cost * event_frequency
        total_profit = price_df['Total Profit (Rp.)'].sum()

        # Return the overall financials and the price_df with detailed calculations
        return total_revenue, total_cost, total_profit
    
    def initial_event_cost_df(self):
        
        return self.event_cost_df