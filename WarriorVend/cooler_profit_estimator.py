import streamlit as st
import os
import sys

# App Title
st.title("Smart Cooler Profit Estimator")
st.write("See how much you can make with a Smart Cooler!")

# Apply White Background and Black Text
st.markdown(
    """
    <style>
        body {
            background-color: white; /* White Background */
            color: black;
        }
        .stApp {
            background-color: white; /* White Background */
            color: black;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Improved Layout with Three Full-Width Columns
col1, col2, col3 = st.columns(3)

with col1:
    st.header("🔧 Selection Options")
    cooler_type = st.radio("Cooler Type", ("Drink-Only", "Drink & Snack Mix"))
    use_employee = st.checkbox("Are you paying someone to service the location?")
    has_financing = st.checkbox("Are there any monthly financing costs associated with the location?")

with col2:
    st.header("📝 Input Data")
    foot_traffic = st.number_input("Daily Foot Traffic", min_value=1, max_value=5000, value=50, step=10)
    data_cost_per_cooler = st.number_input("Data Cost Per Cooler ($)", min_value=0, max_value=500, value=45, step=5)
    refill_threshold_percent = st.number_input("Stock Levels Until Refill (%)", min_value=10, max_value=100, value=65, step=5)
    time_per_refill = st.number_input("Time Per Refill (Hours)", min_value=1, max_value=5, value=2, step=1)
    avg_drink_profit_margin = st.number_input("Drink Profit Margin (%)", min_value=10, max_value=100, value=60, step=1)
    avg_snack_profit_margin = st.number_input("Snack Profit Margin (%)", min_value=10, max_value=100, value=58, step=1)
    
    employee_wage = 0
    if use_employee:
        employee_wage = st.number_input("Enter hourly wage for employee", min_value=1, max_value=100, value=18, step=1)
    
    financing_cost = 0
    if has_financing:
        financing_cost = st.number_input("Enter monthly financing cost", min_value=0, max_value=10000, value=0, step=10)

# Constants
cooler_capacity_drink_only = 240
cooler_capacity_mixed = 279
refill_threshold = (refill_threshold_percent / 100)

if cooler_type == "Drink-Only":
    cooler_capacity = cooler_capacity_drink_only
    profit_margin = avg_drink_profit_margin / 100
    # Adjust for drink selections impact
    option_correlation_factor = 1.65  # Sales increase based on vending machine vs. cooler options
    estimated_daily_revenue = foot_traffic * 0.23 * option_correlation_factor
else:
    cooler_capacity = cooler_capacity_mixed
    profit_margin = avg_snack_profit_margin / 100
    estimated_daily_revenue = foot_traffic * 0.39

# Function to calculate net profit and number of coolers needed
def calculate_net_profit():
    projected_monthly_sales_value = estimated_daily_revenue * 31
    estimated_refills_per_month = projected_monthly_sales_value / ((1 - refill_threshold) * cooler_capacity * 2.61)
    monthly_labor_hours = estimated_refills_per_month * time_per_refill
    monthly_labor_cost = monthly_labor_hours * employee_wage if use_employee else 0
    coolers_needed = max(1, round(foot_traffic / 100))
    data_cost = coolers_needed * data_cost_per_cooler
    projected_monthly_profit = projected_monthly_sales_value * profit_margin
    total_operating_costs = monthly_labor_cost + data_cost + financing_cost
    net_profit = projected_monthly_profit - total_operating_costs
    
    return projected_monthly_sales_value, total_operating_costs, projected_monthly_profit, net_profit, coolers_needed

monthly_sales, operating_costs, monthly_profit, net_profit, coolers_needed = calculate_net_profit()

with col3:
    st.header("📊 Results")
    st.write(f"### Projected Monthly Sales: **${monthly_sales:,.2f}**")
    st.write(f"### Operating Costs: **${operating_costs:,.2f}**")
    st.write(f"### Projected Monthly Profit: **${monthly_profit:,.2f}**")
    st.write(f"### Estimated Monthly Net Profit: **${net_profit:,.2f}**")
    st.write(f"### Estimated Coolers Needed: **{coolers_needed}**")

if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    os.chdir(script_dir)
    if not any("streamlit" in arg for arg in sys.argv):
        os.system(f"streamlit run {script_path}")
