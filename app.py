import streamlit as st
import pulp
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from itertools import product

st.set_page_config(page_title="Indian Supply Chain Optimizer", layout="wide")
st.title("🚚 Multi-Echelon Supply Chain Optimization (India)")
st.markdown("**Realistic Transportation Problem** — Factories → Warehouses → Distribution Centers")

# ====================== YOUR DATA (copy-paste from your notebook) ======================
# (Paste all your locations, factories, warehouses, dcs, products, production_cost,
# factory_capacity, demand, warehouse_capacity, default rates, haversine function here)

# ====================== OPTIMIZATION FUNCTION (slightly cleaned) ======================
def optimize_supply_chain(custom_demand=None, custom_rail_rate=None, custom_road_rate=None):
    # (Your entire optimize function from CELL 3 — just remove the print statements
    # and replace plt.show() with return fig at the end)
    
    # ... (your prob = pulp.LpProblem ... all the way to solving)
    
    if pulp.LpStatus[prob.status] != "Optimal":
        st.error("Model infeasible. Try lower demand.")
        return None, None
    
    # Instead of plt.show(), do this at the end:
    fig, ax = plt.subplots(figsize=(15, 10))  # your networkx drawing code
    # ... nx.draw(...) etc.
    plt.title("Optimal Supply Chain Flows")
    plt.axis('off')
    return total, fig   # return cost and figure

# ====================== STREAMLIT UI ======================
col1, col2 = st.columns(2)
with col1:
    demand_mult = st.slider("Demand Multiplier", 0.5, 2.0, 1.0, 0.1)
with col2:
    rail_rate = st.number_input("Rail Rate (₹/km/unit)", value=1.05, step=0.05)
    road_rate = st.number_input("Road Rate (₹/km/unit)", value=2.65, step=0.05)

if st.button("🚀 Run Optimization", type="primary", use_container_width=True):
    with st.spinner("Solving LP model with PuLP..."):
        custom_demand = {dc: {'P1': int(demand[dc]['P1'] * demand_mult),
                              'P2': int(demand[dc]['P2'] * demand_mult)} for dc in dcs}
        
        total_cost, fig = optimize_supply_chain(custom_demand, rail_rate, road_rate)
        
        if total_cost:
            st.success(f"🎯 Total Minimum Cost: ₹{total_cost:,.2f}")
            
            # Cost breakdown (use st.metric or columns)
            # ... (show your prod_c, rail_c, road_c, wh_c)
            
            st.subheader("Network Visualization")
            st.pyplot(fig)
            
            # Optional: show flows as nice tables
            st.subheader("Sample Flows")
            # convert flows_fw and flows_wd to pandas DataFrames and st.dataframe

st.caption("Built with PuLP + Streamlit • Free forever on Streamlit Community Cloud")
