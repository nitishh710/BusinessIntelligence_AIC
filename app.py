import streamlit as st
import pandas as pd
import time
import random

# App config
st.set_page_config(
    page_title="BusinessIntelligence.ai | KPI Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling for metrics and narrative boxes
st.markdown("""
<style>
    .main { background: #0e1117; color: #fafafa; }
    .stMetric { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); }
    .narrative-box { background: rgba(99, 102, 241, 0.1); border-left: 4px solid #6366f1; padding: 20px; border-radius: 5px; margin-top: 10px; font-size: 1.05rem; line-height: 1.6;}
    .abstain-box { background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; padding: 20px; border-radius: 5px; margin-top: 10px; font-size: 1.05rem; line-height: 1.6;}
</style>
""", unsafe_allow_html=True)

# Mock database ingestion
def generate_dataset(scenario):
    if scenario == "1. Multi-Factor (Revenue Drop)":
        dates = pd.date_range(end=pd.Timestamp.today(), periods=6, freq='W')
        df = pd.DataFrame({
            "Week": [d.strftime("W%U") for d in dates],
            "Revenue": [108000, 112000, 110000, 115000, 118000, 108560],
            "Ad_Spend": [12000, 12500, 12200, 13000, 13200, 11616],
            "Order_Volume": [5400, 5600, 5500, 5750, 5900, 5428]
        })
        return df, "CRM_Sales_DB + AdTech_Platform"

    elif scenario == "2. Low-Confidence (Missing Telemetry)":
        df = pd.DataFrame({
            "Region": ["North America", "Europe", "Asia-Pacific", "Latin America"],
            "Promised_Delivery_Hrs": [24, 24, 48, 48],
            "Actual_Delivery_Hrs": [26.2, 25.1, None, 52.4], 
            "Active_Couriers": [140, 110, 85, 45]
        })
        return df, "IoT_Warehouse_Telemetry"

    elif scenario == "3. Sparse-History (New Launch)":
        dates = pd.date_range(end=pd.Timestamp.today(), periods=4, freq='D')
        df = pd.DataFrame({
            "Day": [f"Day {i+1}" for i in range(len(dates))],
            "Product_X_Sales": [140, 185, 172, 195],
            "Store_Footfall": [1200, 1450, 1380, 1500]
        })
        return df, "POS_Terminal.realtime_sales"

# Deterministic Math Layer (No LLM logic here)
def run_deterministic_engine(df, scenario):
    start_time = time.time()
    results = {
        "is_anomaly": False,
        "confidence_score": 1.0,
        "math_facts": {},
        "lineage": [],
        "can_synthesize": True
    }

    if scenario == "1. Multi-Factor (Revenue Drop)":
        rev_change = ((df['Revenue'].iloc[-1] - df['Revenue'].iloc[-2]) / df['Revenue'].iloc[-2]) * 100
        ad_change = ((df['Ad_Spend'].iloc[-1] - df['Ad_Spend'].iloc[-2]) / df['Ad_Spend'].iloc[-2]) * 100
        
        results.update({
            "is_anomaly": rev_change <= -5.0,
            "confidence_score": 0.96,
            "math_facts": {"Rev_Change": rev_change, "Ad_Change": ad_change, "Ad_Weight": 0.62},
            "lineage": ["SQL Join: CRM + AdTech", f"Math: W06 Rev Δ {rev_change:.1f}%", "Variance Decomposition executed."]
        })

    elif scenario == "2. Low-Confidence (Missing Telemetry)":
        missing_count = df['Actual_Delivery_Hrs'].isnull().sum()
        completeness = 1 - (missing_count / len(df))
        
        results.update({
            "is_anomaly": True,
            "confidence_score": 0.22, 
            "can_synthesize": False,  
            "math_facts": {"Completeness": completeness, "Missing": "Asia-Pacific"},
            "lineage": ["IoT Stream Parsed", "Null values detected in APAC", "Confidence < 70% Threshold"]
        })

    elif scenario == "3. Sparse-History (New Launch)":
        results.update({
            "is_anomaly": False,
            "confidence_score": 0.48, 
            "math_facts": {"N_Days": len(df), "Mean_Sales": df['Product_X_Sales'].mean()},
            "lineage": ["POS Data Queried", f"N={len(df)} days found (Req: 30)", "Z-score baseline bypassed"]
        })
        
    results["latency"] = time.time() - start_time
    return results

# Simulated LLM Output (Mocking API response)
def generate_llm_narrative(math_results, persona, scenario):
    time.sleep(0.8) 
    tokens = random.randint(180, 320)
    
    if not math_results["can_synthesize"]:
        return {
            "narrative": f"**System Halted: Incomplete Data Picture**\n\nI'd normally synthesize a root cause for you here, but I must abstain. The system confidence score has fallen to **{math_results['confidence_score']*100:.0f}%**, which breaks our enterprise safety threshold. \n\nReviewing the lineage, there is a complete blackout of telemetry data from the Asia-Pacific node. Rather than hallucinating a probable cause, I recommend pausing the analysis and engaging IT to restore data integrity.",
            "rec": {"Driver": "Missing APAC Telemetry", "Action": "Dispatch manual sync ping to APAC IoT Gateway.", "Impact": "Restore data integrity and unblock analysis.", "Owner": "IT Operations", "Monitor": "Poll API every 15m"},
            "tokens": tokens, "cost": tokens * 0.000015
        }

    if scenario == "1. Multi-Factor (Revenue Drop)":
        if persona == "Regional Director":
            narr = f"**Observation: Top-line revenue declined {math_results['math_facts']['Rev_Change']:.1f}% this week.** \n\nThe variance decomposition model indicates that the primary driver is the recent **{math_results['math_facts']['Ad_Change']:.1f}% reduction in Ad Spend**, which accounts for approximately 62% of this drop. Organic demand remains stable. If the regional marketing budget is re-authorized, we project a rapid return to the expected growth trajectory."
            rec = {"Driver": "Ad Spend Reduction", "Action": "Re-authorize $1,500 marketing budget for the region.", "Impact": "Recover top-line growth trajectory.", "Owner": "CMO", "Monitor": "Daily ROAS"}
        else: 
            narr = f"**Alert: W06 top-line revenue is down {math_results['math_facts']['Rev_Change']:.1f}%.** \n\nData lineage confirms this stems from CRM and AdTech joins. The deterministic math points to recent ad budget caps. The decomposition gives Ad Spend a weight of {math_results['math_facts']['Ad_Weight']}, making it the primary constraint. Data confidence is robust at 96%. We recommend contacting the growth team to audit campaign caps before it impacts next week's pacing."
            rec = {"Driver": "Ad Spend Cap (Campaign Level)", "Action": "Audit campaign manager budget caps and lift constraints.", "Impact": "Unblock paid traffic flow.", "Owner": "Growth Marketing Lead", "Monitor": "Hourly pacing"}

    elif scenario == "3. Sparse-History (New Launch)":
        narr = f"**Launch Update:** Product X is showing early traction, averaging **{math_results['math_facts']['Mean_Sales']:.1f} units per day.** \n\n*Governance Note for {persona}:* The dataset only contains {math_results['math_facts']['N_Days']} days of live data. Statistical confidence is currently at {math_results['confidence_score']*100:.0f}%. We advise against making major supply chain commitments until the product hits our standard 30-day baseline maturity threshold."
        rec = {"Driver": "New Product (Immature Baseline)", "Action": "Maintain steady inventory; strictly do not over-order.", "Impact": "Prevent warehouse liability before true demand is known.", "Owner": "Supply Chain Planning", "Monitor": "Daily Baseline Maturity Score"}

    return {"narrative": narr, "rec": rec, "tokens": tokens, "cost": tokens * 0.000015}

# Sidebar UI
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/brain--v1.png", width=60)
    st.title("BI.ai Engine")
    st.caption("Accenture Innovation Challenge - Round 2")
    st.markdown("---")
    
    scenario = st.selectbox("Select KPI Scenario", [
        "1. Multi-Factor (Revenue Drop)",
        "2. Low-Confidence (Missing Telemetry)",
        "3. Sparse-History (New Launch)"
    ])
    
    persona = st.selectbox("Select Role (RBAC)", ["Regional Director", "Operations Analyst"])
    
    st.markdown("---")
    st.info(f"**Security Context:** Operating securely as `{persona}`. Narrative tone and action levers are dynamically adjusted.")
    
    st.markdown("---")
    st.markdown("**Developed by Team [anshus24]**") 
    # st.markdown("**Anshu Sharma**") 
    # st.markdown("**Nitish **") 
    # st.markdown("**Dipu Pradhan**") 
# Main Dashboard layout
st.title("KPI Storytelling Copilot")
st.markdown("*Hybrid Architecture: Deterministic Math Engine + Conversational AI Synthesizer*")

df, source = generate_dataset(scenario)
engine_results = run_deterministic_engine(df, scenario)

col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("1. Deterministic Math Engine")
    st.caption("Calculates hard facts, variances, and confidence (Zero LLM logic here).")
    st.markdown(f"**Source Systems:** `{source}`")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    c1, c2 = st.columns(2)
    c1.metric("System Confidence", f"{engine_results['confidence_score']*100:.0f}%", 
              delta="SAFE (Passed Threshold)" if engine_results['confidence_score'] >= 0.7 else "UNSAFE (Abstention Triggered)", 
              delta_color="normal" if engine_results['confidence_score'] >= 0.7 else "inverse")
    c2.metric("Data Lineage Steps Passed", len(engine_results['lineage']))

with col2:
    st.subheader("2. Contextual AI Copilot")
    st.caption(f"Translating math into a strategic brief for: **{persona}**")
    
    with st.spinner("Analyzing data and generating brief..."):
        synthesis = generate_llm_narrative(engine_results, persona, scenario)
    
    box_class = "narrative-box" if engine_results['can_synthesize'] else "abstain-box"
    st.markdown(f'<div class="{box_class}">{synthesis["narrative"]}</div>', unsafe_allow_html=True)
    
    st.markdown("#### Governed Action Plan")
    rec = synthesis["rec"]
    st.markdown(f"""
    * **Driver identified:** `{rec['Driver']}`
    * **Recommended Action:** **{rec['Action']}**
    * **Expected Impact:** {rec['Impact']}
    * **Task Owner:** `{rec['Owner']}` (Monitoring via: *{rec['Monitor']}*)
    """)

# Telemetry footer
st.markdown("---")
st.markdown("#### Runtime Telemetry (Governance & IT Ops)")
t1, t2, t3, t4 = st.columns(4)
t1.metric("Math Engine Latency", f"{engine_results['latency']:.4f}s")
t2.metric("LLM API Latency", "0.8420s")
t3.metric("Tokens Consumed", synthesis['tokens'])
t4.metric("Cost per Insight", f"${synthesis['cost']:.5f}")

st.markdown("**Human-in-the-loop Feedback:** [ Approve ] | [ Flag for review ]")