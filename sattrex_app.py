import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- PAGE SETUP ---
st.set_page_config(page_title="Sattrex Capital Elite", layout="wide")

# --- ADVANCED UI STYLING (THE "FINTECH" LOOK) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #f1f3f6; }
    
    /* Executive Metric Cards */
    .metric-card {
        background: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); border-bottom: 5px solid #1e3d59;
        transition: transform 0.3s ease;
    }
    .metric-card:hover { transform: translateY(-5px); }
    .label { color: #8e9aaf; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }
    .value { color: #1e3d59; font-size: 28px; font-weight: 700; margin-top: 5px; }

    /* Pulsing Notification Alert */
    @keyframes pulse { 
        0% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 75, 75, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
    }
    .notif-pulse {
        background-color: #ff4b4b; color: white; padding: 15px; border-radius: 12px;
        animation: pulse 2s infinite; font-weight: bold; margin-bottom: 20px;
        display: flex; justify-content: space-between; align-items: center;
    }

    /* Action Buttons */
    .btn-pay {
        background-color: #00cc66 !important; color: white !important;
        font-weight: bold; border-radius: 10px; padding: 15px; text-decoration: none;
        display: block; text-align: center; font-size: 18px; margin-bottom: 10px;
    }
    .btn-advisor {
        background-color: #1e3d59 !important; color: white !important;
        font-weight: bold; border-radius: 10px; padding: 15px; text-decoration: none;
        display: block; text-align: center; margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_excel("sample test.xlsx")
    for col in ['Risk Coverage', 'Premium Amount', 'Maturity Amount']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

df = load_data()

# --- SIDEBAR & AUTH ---
st.sidebar.image("logo.png", width=220)
st.sidebar.markdown("---")
email = st.sidebar.text_input("VIP Client Login (Email)")
otp = st.sidebar.text_input("Secure OTP", type="password")

if email and otp == "123456":
    data = df[df['Login_Email'].str.contains(email, na=False, case=False)]
    
    if not data.empty:
        client = data['Main Account'].iloc[0]
        
        # --- TOP HEADER ---
        c_head, c_btn = st.columns([3, 1])
        with c_head:
            st.title(f"Hello, {client}")
            st.write("Strategic Overview by **Vinod Gupta | Sattrex Capital**")
        
        with c_btn:
            st.markdown('<a href="https://ebiz.licindia.in/D2CPM/?_ga=2.224810202.1772775132.1777206873-482751922.1777206873#DirectPay" target="_blank" class="btn-pay">💳 PAY PREMIUM NOW</a>', unsafe_allow_html=True)

        # --- PULSING NOTIFICATION (AUTO-OPEN) ---
        st.markdown("""
            <div class="notif-pulse">
                <span>🔔 ACTION REQUIRED: You have 1 Premium Due and 1 Policy reaching Maturity soon.</span>
                <span style="font-size: 12px;">Tap to view</span>
            </div>
        """, unsafe_allow_html=True)

        # --- EXECUTIVE METRICS ---
        st.markdown("### 🏛️ Protection Overview")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="metric-card"><div class="label">Total Life Value</div><div class="value">₹{data["Risk Coverage"].sum():,.0f}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><div class="label">Annual Savings</div><div class="value">₹{data["Premium Amount"].sum():,.0f}</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><div class="label">Wealth Maturity</div><div class="value">₹{data["Maturity Amount"].sum():,.0f}</div></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="metric-card"><div class="label">Policies Active</div><div class="value">{len(data)}</div></div>', unsafe_allow_html=True)

        st.write("---")

        # --- GAUGE & ACTIONS ---
        col_g, col_a = st.columns([2, 1])
        
        with col_g:
            # Modern Gauge Chart
            score = min(int((data['Risk Coverage'].sum() / 5000000) * 100), 100)
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#1e3d59"},
                    'bar': {'color': "#1e3d59"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "#e0e0e0",
                    'steps': [
                        {'range': [0, 50], 'color': '#fff0f0'},
                        {'range': [50, 100], 'color': '#f0fff0'}],
                },
                title = {'text': "INSURED SCORE", 'font': {'size': 20, 'color': '#8e9aaf'}}))
            fig.update_layout(height=350, margin=dict(t=50, b=0))
            st.plotly_chart(fig, use_container_width=True)

        with col_a:
            st.markdown("### ⚡ Quick Actions")
            st.markdown('<a href="tel:9892027934" class="btn-advisor">📞 TALK TO VINOD GUPTA</a>', unsafe_allow_html=True)
            st.markdown('<a href="tel:9892027934" class="btn-advisor" style="background-color: #f8f9fa !important; color: #1e3d59 !important; border: 1px solid #1e3d59 !important;">🚀 IMPROVE MY SCORE</a>', unsafe_allow_html=True)
            st.markdown('<a href="tel:9892027934" class="btn-advisor" style="background-color: transparent !important; color: gray !important; border: 1px dashed gray !important;">➕ ADD NEW POLICY</a>', unsafe_allow_html=True)

        # --- DATA TABS ---
        t1, t2 = st.tabs(["📄 Detailed Policy Inventory", "📈 Wealth Creation Strategy"])
        
        with t1:
            st.dataframe(data[['Policy Holder', 'Policy No', 'Plan', 'Premium Amount', 'Status']], use_container_width=True, hide_index=True)
        
        with t2:
            st.info("Sattrex Mutual Fund Integration in progress. Your live NAV and XIRR will be updated here.")

    else:
        st.error("Credential Error: Please contact Sattrex Capital to update your registered Email.")
else:
    st.info("VIP Access Only. Please enter your credentials on the sidebar to unlock your dashboard.")
