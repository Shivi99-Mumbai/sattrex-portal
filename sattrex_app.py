import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- PAGE SETUP ---
st.set_page_config(page_title="Sattrex Capital Elite", layout="wide")

# --- ADVANCED UI STYLING (EXECUTIVE DARK THEME) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #f1f3f6; }
    
    /* Premium Metric Cards */
    .metric-card {
        background: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); border-bottom: 5px solid #1e3d59;
        transition: transform 0.3s ease; height: 100%;
    }
    .metric-card:hover { transform: translateY(-5px); }
    .label { color: #8e9aaf; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; }
    .value { color: #1e3d59; font-size: 26px; font-weight: 700; margin-top: 5px; }

    /* Pulsing Notification Alert */
    @keyframes pulse { 
        0% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 75, 75, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
    }
    .notif-pulse {
        background-color: #ff4b4b; color: white; padding: 18px; border-radius: 12px;
        animation: pulse 2s infinite; font-weight: bold; margin-bottom: 25px;
        display: flex; justify-content: space-between; align-items: center;
    }

    /* Action Buttons */
    .btn-pay {
        background-color: #00cc66 !important; color: white !important;
        font-weight: bold; border-radius: 12px; padding: 15px; text-decoration: none;
        display: block; text-align: center; font-size: 18px; margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(0,204,102,0.3);
    }
    .btn-advisor {
        background-color: #1e3d59 !important; color: white !important;
        font-weight: bold; border-radius: 10px; padding: 12px; text-decoration: none;
        display: block; text-align: center; margin-bottom: 10px; font-size: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def load_data():
    df = pd.read_excel("sample test.xlsx")
    # Comprehensive cleaning of all data points
    cols = ['Risk Coverage', 'Premium Amount', 'Maturity Amount', 'Maturity Year']
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

df = load_data()

# --- SIDEBAR & AUTH ---
st.sidebar.image("logo.png", width=220)
st.sidebar.markdown("---")
email = st.sidebar.text_input("Sattrex VIP ID (Email)")
otp = st.sidebar.text_input("Enter Access Code", type="password")

if email and otp == "123456":
    data = df[df['Login_Email'].str.contains(email, na=False, case=False)]
    
    if not data.empty:
        client = data['Main Account'].iloc[0]
        
        # --- TOP HEADER & PAY BUTTON ---
        c_head, c_btn = st.columns([3, 1.2])
        with c_head:
            st.title(f"Strategic Portfolio of {client}")
            st.markdown(f"**Advisor:** Vinod Gupta | **Firm:** Sattrex Capital")
        
        with c_btn:
            st.markdown('<a href="https://ebiz.licindia.in/D2CPM/#DirectPay" target="_blank" class="btn-pay">💳 PAY PREMIUM NOW</a>', unsafe_allow_html=True)

        # --- PULSING ATTENTION NOTIFICATION ---
        st.markdown(f"""
            <div class="notif-pulse">
                <span>🔔 ATTENTION: Portfolio has {len(data)} active entries. Next major milestone in {int(data['Maturity Year'].max())}.</span>
                <span style="font-size: 12px; border: 1px solid white; padding: 2px 8px; border-radius: 5px;">URGENT</span>
            </div>
        """, unsafe_allow_html=True)

        # --- ANALYTICAL GRAPHS SECTION ---
        st.markdown("### 📊 Wealth Analytics & Forecast")
        col_forecast, col_breakdown = st.columns([2, 1])

        with col_forecast:
            # Maturity Timeline Analysis
            timeline_data = data.groupby('Maturity Year')['Maturity Amount'].sum().reset_index()
            timeline_data = timeline_data[timeline_data['Maturity Year'] > 0]
            fig_timeline = px.area(timeline_data, x='Maturity Year', y='Maturity Amount',
                                  title="Wealth Maturity Projection",
                                  color_discrete_sequence=['#1e3d59'])
            fig_timeline.update_layout(height=350, plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_timeline, use_container_width=True)

        with col_breakdown:
            # Category Wise Breakdown
            status_counts = data['Status'].value_counts()
            fig_pie = px.pie(values=status_counts.values, names=status_counts.index, 
                            title="Portfolio Composition",
                            hole=0.6, color_discrete_sequence=['#1e3d59', '#3a7ca5', '#d1d8e0'])
            fig_pie.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)

        # --- FAMILY COVERAGE CARDS ---
        st.markdown("### 🛡️ Coverage Metrics")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="metric-card"><div class="label">Total Risk Value</div><div class="value">₹{data["Risk Coverage"].sum():,.0f}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><div class="label">Annual Commitment</div><div class="value">₹{data["Premium Amount"].sum():,.0f}</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><div class="label">Guaranteed Payouts</div><div class="value">₹{data["Maturity Amount"].sum():,.0f}</div></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="metric-card"><div class="label">Portfolio Items</div><div class="value">{len(data)} Policies</div></div>', unsafe_allow_html=True)

        st.write("---")

        # --- PROTECTION SCORE & ACTION CENTER ---
        col_g, col_a = st.columns([2, 1])
        
        with col_g:
            score = min(int((data['Risk Coverage'].sum() / 5000000) * 100), 100)
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number", value = score,
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#1e3d59"},
                    'steps': [{'range': [0, 50], 'color': '#fff0f0'}, {'range': [50, 100], 'color': '#f0fff0'}]
                },
                title = {'text': "Protection Audit Score", 'font': {'size': 18, 'color': '#8e9aaf'}}))
            fig_gauge.update_layout(height=350, margin=dict(t=50, b=0))
            st.plotly_chart(fig_gauge, use_container_width=True)

        with col_a:
            st.markdown("### ⚡ Executive Actions")
            st.markdown('<a href="tel:9892027934" class="btn-advisor">📞 TALK TO ADVISOR</a>', unsafe_allow_html=True)
            st.markdown('<a href="tel:9892027934" class="btn-advisor" style="background-color: white !important; color: #1e3d59 !important; border: 1px solid #1e3d59 !important;">🚀 IMPROVE MY SCORE</a>', unsafe_allow_html=True)
            
            # Interactive Data Insights
            st.info(f"**Insight:** Your next significant payout is scheduled for the year {int(data['Maturity Year'].mode()[0]) if not data['Maturity Year'].empty else 'N/A'}.")

        # --- FULL TABLE WITH ALL DATA ---
        st.markdown("### 📑 Detailed Family Portfolio Inventory")
        display_df = data[['Policy Holder', 'Policy No', 'Plan', 'Mode', 'Due Month', 'Premium Amount', 'Risk Coverage', 'Maturity Amount', 'Maturity Year', 'Status']]
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    else:
        st.error("Credential Error: Data not found for this Email ID.")
else:
    st.info("Log in to the Sattrex Digital Notebook using your VIP Credentials.")
