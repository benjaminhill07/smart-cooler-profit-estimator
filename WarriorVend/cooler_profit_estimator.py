import streamlit as st
import os
import sys

# App Title
st.title("Smart Cooler Profit Estimator")
st.write("Enter the estimated daily foot traffic to calculate projected monthly net profit.")

# Apply Dark Green Background and White Text
st.markdown(
    """
    <style>
        body {
            background-color: #013220; /* Dark Green */
            color: white;
        }
        .stApp {
            background-color: #013220; /* Dark Green */
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Constants
cooler_capacity_drink_only = 240  # Total drinks per drink-only cooler
cooler_capacity_mixed = 279  # (144 drinks + 135 snacks) for mixed cooler
refill_threshold_drink_only = cooler_capacity_drink_only * 0.65  # Refill threshold for drink-only coolers
refill_threshold_mixed = cooler_capacity_mixed * 0.65  # Refill threshold for mixed coolers
snack_sales_percentage = 0.38  # 38% of sales are snacks
drink_sales_percentage = 0.62  # 62% of sales are drinks
average_snack_price = 2.13  # Average price per snack sold
average_drink_price = 2.61  # Average price per drink sold
real_world_revenue_per_person_mixed = 0.39  # Real-world average revenue per person for Drink & Snack Mix coolers
real_world_revenue_per_person_drink_only = 0.76  # Adjusted based on real vending machine sales
time_per_refill = 2  # Each refill takes 2 hours
default_employee_wage = 18  # Default wage per hour
profit_margin_drinks = 0.60  # Profit margin on drinks
profit_margin_mixed = 0.58  # Profit margin on mixed coolers
data_cost_per_cooler = 45  # Monthly data cost per cooler
days_in_month = 31  # Number of days in a month

# User Inputs
foot_traffic = st.number_input("Daily Foot Traffic", min_value=1, max_value=5000, value=50, step=10)

# Cooler Type Selection
cooler_type = st.radio("What type of cooler will you use?", ("Drink-Only", "Drink & Snack Mix"))
if cooler_type == "Drink-Only":
    cooler_capacity = cooler_capacity_drink_only
    refill_threshold = refill_threshold_drink_only
    profit_margin = profit_margin_drinks
    estimated_daily_revenue = foot_traffic * real_world_revenue_per_person_drink_only
else:
    cooler_capacity = cooler_capacity_mixed
    refill_threshold = refill_threshold_mixed
    profit_margin = profit_margin_mixed
    estimated_daily_revenue = foot_traffic * real_world_revenue_per_person_mixed

use_employee = st.checkbox("Are you paying someone to service the location?")
employee_wage = default_employee_wage
if use_employee:
    employee_wage = st.number_input("Enter hourly wage for employee", min_value=1, max_value=100, value=default_employee_wage, step=1)

has_financing = st.checkbox("Are there any monthly financing costs associated with the location?")
financing_cost = 0
if has_financing:
    financing_cost = st.number_input("Enter monthly financing cost", min_value=0, max_value=10000, value=0, step=10)

# Function to calculate net profit and number of coolers needed
def calculate_net_profit(employee_wage, financing_cost, cooler_capacity, refill_threshold, profit_margin):
    projected_monthly_sales_value = estimated_daily_revenue * days_in_month

    estimated_refills_per_month = projected_monthly_sales_value / (cooler_capacity * 0.65 * average_drink_price)
    monthly_labor_hours = estimated_refills_per_month * time_per_refill
    monthly_labor_cost = monthly_labor_hours * employee_wage if use_employee else 0

    # Simplified calculation for coolers needed
    coolers_needed = max(1, round(foot_traffic / 100))

    # Adjust data cost based on coolers needed
    data_cost = coolers_needed * data_cost_per_cooler

    projected_monthly_profit = projected_monthly_sales_value * profit_margin
    total_operating_costs = monthly_labor_cost + data_cost + financing_cost
    net_profit = projected_monthly_profit - total_operating_costs

    return projected_monthly_sales_value, projected_monthly_profit, total_operating_costs, net_profit, monthly_labor_cost, data_cost, coolers_needed

# Calculate results
monthly_sales, monthly_profit, operating_costs, net_profit, labor_cost, data_cost, coolers_needed = calculate_net_profit(
    employee_wage, financing_cost, cooler_capacity, refill_threshold, profit_margin
)

# Display Results
st.write(f"### 📊 Projected Monthly Sales: **${monthly_sales:,.2f}**")
st.write(f"### 💰 Projected Monthly Profit: **${monthly_profit:,.2f}**")
st.write(f"### 🔧 Operating Costs: **${operating_costs:,.2f}**")
st.write(f"### ✅ Estimated Monthly Net Profit: **${net_profit:,.2f}**")
st.write(f"### 🧊 Estimated Coolers Needed: **{coolers_needed}**")

# Detailed Assumptions
st.write("#### **Assumptions and Cost Breakdown:**")
st.write(f"- **Cooler Type Selected:** {cooler_type}")
st.write(f"- **Each Cooler Capacity:** {cooler_capacity} items")
st.write(f"- **Refill Threshold:** {refill_threshold:.0f} items per cooler")
st.write(f"- **Estimated Daily Revenue Per Person (Mixed):** ${real_world_revenue_per_person_mixed:.2f}")
st.write(f"- **Estimated Daily Revenue Per Person (Drink-Only):** ${real_world_revenue_per_person_drink_only:.2f}")
st.write(f"- **Time Per Refill:** {time_per_refill} hours")
st.write(f"- **Profit Margin:** {profit_margin * 100:.0f}%")
st.write(f"- **Employee Wage:** ${employee_wage:.2f} per hour" if use_employee else "- **Self-service: No labor cost applied")
st.write(f"- **Estimated Monthly Labor Cost:** ${labor_cost:,.2f}")
st.write(f"- **Data Cost:** ${data_cost:,.2f} (Based on {coolers_needed} coolers at ${data_cost_per_cooler} per cooler)")
st.write(f"- **Financing Cost:** ${financing_cost:,.2f}")

if __name__ == "__main__":
    script_path = os.path.abspath(__file__)  # Get the absolute path of the script
    script_dir = os.path.dirname(script_path)  # Get the directory containing the script

    # Change to the script directory so Streamlit runs correctly
    os.chdir(script_dir)

    # Prevent infinite loop
    if not any("streamlit" in arg for arg in sys.argv):
        os.system(f"streamlit run {script_path}")
