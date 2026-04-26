import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# --- SYSTEM SETTINGS ---
st.set_page_config(page_title="Sattrex Elite | Portfolio OS", layout="wide")

# --- EXECUTIVE UI STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #f4f7f9; }
    
    /* Modern Glass Cards */
    .glass-card {
        background: white; padding: 25px; border-radius: 24px;
        box-shadow: 0 15px 35px rgba(30, 61, 89, 0.05); border: 1px solid rgba(255,255,255,0.3);
        margin-bottom: 25px;
    }
    
    /* Luxury Metrics */
    .metric-title { color: #8e9aaf; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; }
    .metric-value { color: #1e3d59; font-size: 32px; font-weight: 700; margin: 5px 0; }
    
    /* Pulsing Recommendation Bar */
    @keyframes attention { 
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(30, 61, 89, 0.4); }
        70% { transform: scale(1.01); box-shadow: 0 0 0 10px rgba(30, 61, 89, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(30, 61, 89, 0); }
    }
    .intel-bar {
        background: linear-gradient(90deg, #1e3d59 0%, #3a7ca5 100%);
        color: white; padding: 20px; border-radius: 15px; margin-bottom: 30px;
        animation: attention 3s infinite ease-in-out; border-left: 8px solid #00cc66;
    }

    /* Professional Buttons */
    .btn-main { background-color: #1e3d59; color: white; padding: 15px; border-radius: 12px; display: block; text-align: center; text-decoration: none; font-weight: 700; margin-bottom: 10px; }
    .btn-pay { background-color: #00cc66; color: white; padding: 15px; border-radius: 12px; display: block; text-align: center; text-decoration: none; font-weight: 700; font-size: 18px; box-shadow: 0 5px 15px rgba(0,204,102,0.3); }
    </style>
""", unsafe_allow_html=True)

# --- INTELLIGENT DATA ENGINE ---
@st.cache_data
def load_and_clean():
    df = pd.read_excel("sample test.xlsx")
    numeric_cols = ['Risk Coverage', 'Premium Amount', 'Maturity Amount', 'Maturity Year', 'Age at Maturity']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

df = load_and_clean()

# --- AUTHENTICATION ---
st.sidebar.image("logo.png", width=220)
st.sidebar.markdown("### 🔒 Secure Vault")
email = st.sidebar.text_input("Client ID")
otp = st.sidebar.text_input("Access Key (OTP)", type="password")

if email and otp == "123456":
    user_data = df[df['Login_Email'].str.contains(email, na=False, case=False)]
    
    if not user_data.empty:
        client_name = user_data['Main Account'].iloc[0]
        
        # --- TOP SECTION: IDENTITY & GLOBAL PAY ---
        col_id, col_action = st.columns([3, 1])
        with col_id:
            st.title(f"Hello, {client_name}")
            st.markdown(f"**Advisor Executive:** Vinod Gupta | Sattrex Capital")
        with col_action:
            st.markdown('<a href="https://ebiz.licindia.in/D2CPM/#DirectPay" target="_blank" class="btn-pay">💳 PAY PREMIUM NOW</a>', unsafe_allow_html=True)

        # --- DYNAMIC INTELLIGENCE (LOGIC-BASED RECOMMENDATIONS) ---
        total_risk = user_data['Risk Coverage'].sum(skipna=True)
        max_maturity = user_data['Maturity Year'].max()
        
        st.markdown('<div class="intel-bar">', unsafe_allow_html=True)
        # Recommendation 1: Underinsured check
        if total_risk < 10000000:
            st.markdown("🚀 **STRATEGIC GAP:** Your total life value is currently below our VIP benchmark of ₹1Cr. Protect your family's future with a Sum Assured Top-up.")
        # Recommendation 2: Maturity opportunity
        elif max_maturity > 0:
            st.markdown(f"💰 **LIQUIDITY ALERT:** Large maturities are scheduled for {int(max_maturity)}. Let's plan your Mutual Fund reinvestment strategy now to avoid tax leakage.")
        # Recommendation 3: Age-based (General)
        st.markdown("📈 **OPPORTUNITY:** Reviewing your asset mix—consider shifting 20% to Equity Mutual Funds for aggressive wealth creation.")
        st.markdown('</div>', unsafe_allow_html=True)

        # --- SECTION 1: KEY PERFORMANCE CARDS ---
        st.markdown("### 🏛️ Portfolio Snapshot")
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f'<div class="glass-card"><span class="metric-title">Total Life Value</span><div class="metric-value">₹{total_risk:,.0f}</div></div>', unsafe_allow_html=True)
        with k2:
            st.markdown(f'<div class="glass-card"><span class="metric-title">Annual Savings</span><div class="metric-value">₹{user_data["Premium Amount"].sum():,.0f}</div></div>', unsafe_allow_html=True)
        with k3:
            st.markdown(f'<div class="glass-card"><span class="metric-title">Guaranteed Wealth</span><div class="metric-value">₹{user_data["Maturity Amount"].sum():,.0f}</div></div>', unsafe_allow_html=True)
        with k4:
            active_count = len(user_data[user_data['Status'].str.contains('IN FORCE', na=False, case=False)])
            st.markdown(f'<div class="glass-card"><span class="metric-title">Active Assets</span><div class="metric-value">{active_count} Policies</div></div>', unsafe_allow_html=True)

        # --- SECTION 2: INTERACTIVE MODERN GRAPHS (THE MIDDLE SECTION) ---
        st.write("---")
        st.markdown("### 📊 Interactive Wealth Analytics")
        g_left, g_right = st.columns([2, 1])
        
        with g_left:
            # High-end Maturity Forecast
            timeline = user_data.groupby('Maturity Year')['Maturity Amount'].sum().reset_index()
            timeline = timeline[timeline['Maturity Year'] > 0]
            fig_bar = px.bar(timeline, x='Maturity Year', y='Maturity Amount', 
                             title="Family Maturity Forecast (Annual Cashflows)",
                             template="plotly_white", color_discrete_sequence=['#1e3d59'])
            fig_bar.update_layout(bargap=0.4, plot_bgcolor='rgba(0,0,0,0)', yaxis_title="Payout Amount (₹)")
            st.plotly_chart(fig_bar, use_container_width=True)

        with g_right:
            # Modern Gauge / Score
            score = min(int((total_risk / 7500000) * 100), 100)
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number", value = score,
                gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#1e3d59"},
                         'steps': [{'range': [0, 50], 'color': "#ffecec"}, {'range': [50, 100], 'color': "#e8f5e9"}]},
                title = {'text': "Insured Score", 'font': {'size': 20}}))
            fig_gauge.update_layout(height=350, margin=dict(t=50, b=0))
            st.plotly_chart(fig_gauge, use_container_width=True)

        # --- SECTION 3: FAMILY ACTION CENTER ---
        st.markdown("### ⚡ Executive Suite")
        a1, a2, a3 = st.columns(3)
        with a1:
            st.markdown('<a href="tel:9892027934" class="btn-main">📞 CALL VINOD GUPTA</a>', unsafe_allow_html=True)
        with a2:
            st.markdown('<a href="tel:9892027934" class="btn-main" style="background:#fff; color:#1e3d59; border:1px solid #1e3d59;">🚀 IMPROVE MY SCORE</a>', unsafe_allow_html=True)
        with a3:
            csv = user_data.to_csv(index=False).encode('utf-8')
            st.download_button(label="📄 DOWNLOAD ANALYTICAL REPORT", data=csv, file_name=f"{client_name}_Sattrex_Audit.csv", use_container_width=True)

        # --- SECTION 4: FULL DATA INVENTORY (NO ZEROS) ---
        st.write("---")
        st.markdown("### 📋 Detailed Asset Inventory")
        # Cleaning display data: Replace 0 or NaN with "Not Available"
        display_df = user_data[['Policy Holder', 'Policy No', 'Plan', 'Mode', 'Premium Amount', 'Risk Coverage', 'Maturity Amount', 'Maturity Year', 'Status']].copy()
        
        # This part ensures clients aren't scared by 0s
        for col in display_df.columns:
            display_df[col] = display_df[col].apply(lambda x: "Not Available" if (x == 0 or pd.isna(x)) else x)
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    else:
        st.error("Authentication Error: Record not found in Elite Database.")
else:
    st.title("Sattrex Capital | Portfolio OS")
    st.info("Authorized Personnel Only. Please log in to access the Family Office Dashboard.")
