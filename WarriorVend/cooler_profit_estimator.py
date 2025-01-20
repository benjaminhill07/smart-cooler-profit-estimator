import streamlit as st
import os
import sys

# Apply Video Background
st.markdown(
    """
    <style>
        body, .stApp {
            background: url('smartcoolerimage.png') no-repeat center center fixed;
            background-size: cover;
            color: white; /* Ensure text remains visible */
        }
        .stApp::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.3); /* Adds a subtle dark overlay for contrast */
            z-index: -1;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title
st.markdown("""
    <h1 style='text-align: center; color: white; font-weight: bold;'>Smart Cooler Profit Estimator</h1>
""", unsafe_allow_html=True)
st.markdown("""
    <h3 style='text-align: center; color: white; font-weight: bold;'>See how much you can make with a Smart Cooler!</h3>
""", unsafe_allow_html=True)

# Improved Layout with Three Full-Width Columns
col1, col2, col3 = st.columns(3)

with col1:
    st.header("🔧 Selection Options")
    use_employee = st.checkbox("Are you paying someone to service the location?")
    has_financing = st.checkbox("Are there any monthly financing costs associated with the location?")

with col2:
    st.header("📝 Input Data")
    foot_traffic = st.number_input("Daily Foot Traffic", min_value=1, max_value=5000, value=50, step=10)
    refill_threshold_percent = st.number_input("Stock Levels Until Refill (%)", min_value=10, max_value=100, value=65, step=5)
    time_per_refill = st.number_input("Time Per Refill (Hours)", min_value=1.0, max_value=5.0, value=2.0, step=0.1)
    avg_product_profit_margin = st.number_input("Average Product Profit Margin (%)", min_value=10, max_value=100, value=59, step=1)
    data_cost_per_cooler = st.number_input("Data Cost Per Cooler ($)", min_value=0, max_value=500, value=45, step=5)
    state_sales_tax = st.number_input("State Sales Tax Rate (%)", min_value=0.0, max_value=15.0, value=7.75, step=0.1)
    credit_card_fee = st.number_input("Credit Card Service Fee (%)", min_value=0.0, max_value=10.0, value=5.95, step=0.1)
    
    employee_wage = 0
    if use_employee:
        employee_wage = st.number_input("Enter hourly wage for employee", min_value=1.0, max_value=100.0, value=18.0, step=0.1)
    
    financing_cost = 0
    if has_financing:
        financing_cost = st.number_input("Enter monthly financing cost", min_value=0, max_value=10000, value=0, step=10)

# Constants
cooler_capacity = 279
profit_margin = avg_product_profit_margin / 100
estimated_daily_revenue = foot_traffic * 0.39

# Function to calculate net profit and number of coolers needed
def calculate_net_profit():
    global monthly_labor_cost, sales_tax_cost, credit_card_cost, data_cost
    projected_monthly_sales_value = estimated_daily_revenue * 31
    estimated_refills_per_month = projected_monthly_sales_value / ((1 - refill_threshold_percent/100) * cooler_capacity * 2.61)
    monthly_labor_hours = estimated_refills_per_month * time_per_refill
    monthly_labor_cost = monthly_labor_hours * employee_wage if use_employee else 0
    coolers_needed = max(1, round(foot_traffic / 100))
    data_cost = coolers_needed * data_cost_per_cooler
    projected_monthly_profit = projected_monthly_sales_value * profit_margin
    sales_tax_cost = (state_sales_tax / 100) * projected_monthly_sales_value
    credit_card_cost = (credit_card_fee / 100) * projected_monthly_sales_value
    total_operating_costs = monthly_labor_cost + data_cost + financing_cost + sales_tax_cost + credit_card_cost
    net_profit = projected_monthly_profit - total_operating_costs
    
    return projected_monthly_sales_value, total_operating_costs, projected_monthly_profit, net_profit, coolers_needed, monthly_labor_cost, sales_tax_cost, credit_card_cost, data_cost

monthly_sales, operating_costs, monthly_profit, net_profit, coolers_needed, monthly_labor_cost, sales_tax_cost, credit_card_cost, data_cost = calculate_net_profit()

with col3:
    st.header("📊 Results")
    st.write(f"### Projected Monthly Sales: **${monthly_sales:,.2f}**")
    st.write(f"### Projected Monthly Profit: **${monthly_profit:,.2f}**")
    st.write(f"### Operating Costs: **${operating_costs:,.2f}**")
    st.write(f"- Labor Cost: **${monthly_labor_cost:,.2f}**")
    st.write(f"- Data Cost: **${data_cost:,.2f}**")
    st.write(f"- Financing Cost: **${financing_cost:,.2f}**")
    st.write(f"- Sales Tax Cost: **${sales_tax_cost:,.2f}**")
    st.write(f"- Credit Card Fees: **${credit_card_cost:,.2f}**")
    st.write(f"### Estimated Monthly Net Profit: **${net_profit:,.2f}**")
    st.write(f"### Estimated Coolers Needed: **{coolers_needed}**")

if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    os.chdir(script_dir)
    if not any("streamlit" in arg for arg in sys.argv):
        os.system(f"streamlit run {script_path}")
