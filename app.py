import streamlit as st
import pulp
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from itertools import product

# ========================= CONFIG =========================
st.set_page_config(
    page_title="Indian Supply Chain Optimizer",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Multi-Echelon Supply Chain Optimization")
st.markdown("**Transportation Problem** — Factories → Warehouses → Distribution Centers (Realistic Indian Data)")

# ====================== DATA (exactly from your Colab) ======================
locations = {
    'F1': (19.0760, 72.8777),  # Mumbai
    'F2': (28.6139, 77.2090),  # Delhi
    'F3': (12.9716, 77.5946),  # Bengaluru
    'W1': (23.0225, 72.5714),  # Ahmedabad
    'W2': (17.3850, 78.4867),  # Hyderabad
    'W3': (13.0827, 80.2707),  # Chennai
    'W4': (22.5726, 88.3639),  # Kolkata
    'W5': (26.8467, 80.9462),  # Lucknow
    'D1': (18.5204, 73.8567), 'D2': (21.1702, 72.8311), 'D3': (26.9124, 75.7873),
    'D4': (30.7333, 76.7794), 'D5': (23.2599, 77.4126), 'D6': (25.5941, 85.1376),
    'D7': (26.1445, 91.7362), 'D8': (11.0168, 76.9558), 'D9': (9.9312, 76.2673),
    'D10': (17.6868, 83.2185)
}

factories = ['F1', 'F2', 'F3']
warehouses = ['W1', 'W2', 'W3', 'W4', 'W5']
dcs = ['D1','D2','D3','D4','D5','D6','D7','D8','D9','D10']
products = ['P1', 'P2']

def haversine(coord1, coord2):
    R = 6371.0
    lat1, lon1 = np.radians(coord1)
    lat2, lon2 = np.radians(coord2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c

# Costs and Capacities
production_cost = {'F1': {'P1': 8.5, 'P2': 15.0}, 'F2': {'P1': 9.0, 'P2': 12.5}, 'F3': {'P1': 10.0, 'P2': 13.0}}
factory_capacity = {'F1': {'P1': 8000, 'P2': 1800}, 'F2': {'P1': 7000, 'P2': 2200}, 'F3': {'P1': 6000, 'P2': 1400}}
demand = {
    'D1': {'P1': 2800, 'P2': 420}, 'D2': {'P1': 2100, 'P2': 310}, 'D3': {'P1': 1350, 'P2': 480},
    'D4': {'P1': 1650, 'P2': 260}, 'D5': {'P1': 2400, 'P2': 380}, 'D6': {'P1': 950, 'P2': 620},
    'D7': {'P1': 850, 'P2': 220}, 'D8': {'P1': 1550, 'P2': 460}, 'D9': {'P1': 1200, 'P2': 330},
    'D10': {'P1': 1750, 'P2': 280}
}
warehouse_capacity = {w: 8500 for w in warehouses}
default_rail_rate = 1.05
default_road_rate = 2.65
holding_cost = 1.80
handling_cost = 0.75

# ====================== OPTIMIZATION FUNCTION ======================
def optimize_supply_chain(custom_demand, custom_rail_rate, custom_road_rate):
    prob = pulp.LpProblem("Multi_Echelon_Supply_Chain", pulp.LpMinimize)

    # Variables
    x = pulp.LpVariable.dicts("F_to_W", ((f, w, p) for f in factories for w in warehouses for p in products), lowBound=0, cat='Continuous')
    y = pulp.LpVariable.dicts("W_to_D", ((w, d, p) for w in warehouses for d in dcs for p in products), lowBound=0, cat='Continuous')

    # Objective
    total_cost = (
        pulp.lpSum([production_cost[f][p] * pulp.lpSum(x[f, w, p] for w in warehouses) for f in factories for p in products]) +
        pulp.lpSum([custom_rail_rate * haversine(locations[f], locations[w]) * x[f, w, p] for f in factories for w in warehouses for p in products]) +
        pulp.lpSum([custom_road_rate * haversine(locations[w], locations[d]) * y[w, d, p] for w in warehouses for d in dcs for p in products]) +
        pulp.lpSum([(handling_cost + holding_cost) * pulp.lpSum(x[f, w, p] for f in factories for p in products) for w in warehouses])
    )
    prob += total_cost

    # Constraints
    for f, p in product(factories, products):
        prob += pulp.lpSum(x[f, w, p] for w in warehouses) <= factory_capacity[f][p]

    for w in warehouses:
        prob += pulp.lpSum(x[f, w, p] for f in factories for p in products) <= warehouse_capacity[w]

    for d, p in product(dcs, products):
        prob += pulp.lpSum(y[w, d, p] for w in warehouses) == custom_demand[d][p]

    for w, p in product(warehouses, products):
        prob += pulp.lpSum(x[f, w, p] for f in factories) == pulp.lpSum(y[w, d, p] for d in dcs)

    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    status = pulp.LpStatus[prob.status]

    if status != "Optimal":
        return None, None, None, None, None, None, None

    total = pulp.value(prob.objective)

    # Cost breakdown
    prod_c = sum(production_cost[f][p] * sum(x[f,w,p].varValue for w in warehouses) for f in factories for p in products)
    rail_c = sum(custom_rail_rate * haversine(locations[f], locations[w]) * x[f,w,p].varValue for f,w,p in product(factories, warehouses, products))
    road_c = sum(custom_road_rate * haversine(locations[w], locations[d]) * y[w,d,p].varValue for w,d,p in product(warehouses, dcs, products))
    wh_c   = sum((handling_cost + holding_cost) * sum(x[f,w,p].varValue for f in factories for p in products) for w in warehouses)

    # Flows (non-zero only)
    flows_fw = [(f, w, p, round(x[f,w,p].varValue, 1)) for f,w,p in product(factories, warehouses, products) if x[f,w,p].varValue > 0.1]
    flows_wd = [(w, d, p, round(y[w,d,p].varValue, 1)) for w,d,p in product(warehouses, dcs, products) if y[w,d,p].varValue > 0.1]

    # Network Visualization
    G = nx.DiGraph()
    for f in factories: G.add_node(f, layer='Factory')
    for w in warehouses: G.add_node(w, layer='Warehouse')
    for d in dcs: G.add_node(d, layer='DC')

    for f, w, p, val in flows_fw:
        G.add_edge(f, w, weight=val, color='blue')
    for w, d, p, val in flows_wd:
        G.add_edge(w, d, weight=val, color='green')

    pos = {n: (0, factories.index(n)) if n.startswith('F') else
           (1, warehouses.index(n)) if n.startswith('W') else
           (2, dcs.index(n)) for n in G.nodes()}

    fig = plt.figure(figsize=(15, 10))
    colors = ['#a8d4ff' if n.startswith('F') else '#b3f0c0' if n.startswith('W') else '#ffd9a8' for n in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=2200, font_size=10, font_weight='bold',
            arrows=True, arrowsize=25, edge_color=[d.get('color','gray') for _,_,d in G.edges(data=True)])

    edge_labels = {(u,v): f"{d.get('weight',0):.0f}" for u,v,d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("Optimal Supply Chain Flows\nBlue = Rail (Factory → Warehouse) | Green = Road (Warehouse → DC)")
    plt.axis('off')
    plt.tight_layout()

    # Convert flows to DataFrames for nice tables
    fw_df = pd.DataFrame(flows_fw, columns=["Factory", "Warehouse", "Product", "Quantity"])
    wd_df = pd.DataFrame(flows_wd, columns=["Warehouse", "DC", "Product", "Quantity"])

    return total, prod_c, rail_c, road_c, wh_c, fw_df, wd_df, fig

# ====================== STREAMLIT UI ======================
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    demand_mult = st.slider("Demand Multiplier", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
with col2:
    rail_rate = st.number_input("Rail Rate (₹ per km per unit)", value=default_rail_rate, step=0.05)
with col3:
    road_rate = st.number_input("Road Rate (₹ per km per unit)", value=default_road_rate, step=0.05)

st.caption(f"Current scenario: Base Demand × {demand_mult} | Total P1 demand = {int(sum(d['P1'] for d in demand.values()) * demand_mult)} | Total P2 demand = {int(sum(d['P2'] for d in demand.values()) * demand_mult)}")

if st.button("🚀 Run Optimization", type="primary", use_container_width=True):
    with st.spinner("Solving Linear Programming model with PuLP (CBC solver)..."):
        # Create custom demand
        custom_demand = {
            dc: {
                'P1': int(demand[dc]['P1'] * demand_mult),
                'P2': int(demand[dc]['P2'] * demand_mult)
            } for dc in dcs
        }
        
        result = optimize_supply_chain(custom_demand, rail_rate, road_rate)
        
        if result[0] is None:
            st.error("⚠️ Model is Infeasible. Please reduce the Demand Multiplier.")
        else:
            total, prod_c, rail_c, road_c, wh_c, fw_df, wd_df, fig = result
            
            st.success(f"🎯 Total Minimum Cost: ₹{total:,.2f}")
            
            # Cost breakdown
            st.subheader("Cost Breakdown")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Production Cost", f"₹{prod_c:,.0f}")
            c2.metric("Rail Transport (F→W)", f"₹{rail_c:,.0f}")
            c3.metric("Road Transport (W→D)", f"₹{road_c:,.0f}")
            c4.metric("Warehousing + Holding", f"₹{wh_c:,.0f}")
            
            # Visualization
            st.subheader("Optimal Supply Chain Network")
            st.pyplot(fig)
            
            # Flows tables
            tab1, tab2 = st.tabs(["Factory → Warehouse Flows", "Warehouse → DC Flows"])
            with tab1:
                st.dataframe(fw_df, use_container_width=True, hide_index=True)
            with tab2:
                st.dataframe(wd_df, use_container_width=True, hide_index=True)

st.divider()
st.caption("Built with PuLP + Streamlit • Free forever on Streamlit Community Cloud • Original Colab project by Prabodh")
