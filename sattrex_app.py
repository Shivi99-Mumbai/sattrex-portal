import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sattrex Capital Elite", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR TOP-CLASS UI ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    
    /* Metric Cards Styling */
    .metric-card {
        background-color: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 4px solid #1e3d59;
        text-align: left; margin-bottom: 20px;
    }
    .metric-label { color: #6c757d; font-size: 14px; font-weight: 500; }
    .metric-value { color: #1e3d59; font-size: 24px; font-weight: 700; }
    
    /* Notification styling */
    .notif-box {
        background-color: #fff3cd; border-left: 5px solid #ffc107;
        padding: 15px; border-radius: 8px; margin-bottom: 10px;
    }
    
    /* Action Buttons */
    div.stButton > button {
        width: 100%; border-radius: 8px; height: 3.5em;
        background-color: #1e3d59; color: white; font-weight: 600;
        border: none; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #2b567a; border: none; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def load_data():
    df = pd.read_excel("sample test.xlsx")
    for col in ['Risk Coverage', 'Premium Amount', 'Maturity Amount']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

df = load_data()

# --- SIDEBAR LOGIN ---
st.sidebar.image("logo.png", width=180)
st.sidebar.markdown("---")
email = st.sidebar.text_input("Client ID (Email)")
otp = st.sidebar.text_input("Access Key (OTP)", type="password")

if email and otp == "123456":
    client_data = df[df['Login_Email'].str.contains(email, na=False, case=False)]
    
    if not client_data.empty:
        client_name = client_data['Main Account'].iloc[0]
        
        # --- HEADER & NOTIFICATIONS ---
        col_title, col_notif = st.columns([3, 1])
        with col_title:
            st.title(f"Welcome, {client_name}")
            st.caption(f"Wealth Manager: Vinod Gupta | Sattrex Capital")
        
        with col_notif:
            with st.expander("🔔 Notifications (2)"):
                st.markdown('<div class="notif-box">Premium Due: ₹45,200 (May 15)</div>', unsafe_allow_html=True)
                st.markdown('<div class="notif-box">Maturity Alert: Policy ending in 4521</div>', unsafe_allow_html=True)

        # --- TOP METRIC ROW ---
        st.markdown("### 🏛️ Coverage Overview")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="metric-card"><span class="metric-label">Total Life Value</span><br><span class="metric-value">₹{client_data["Risk Coverage"].sum():,.0f}</span></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><span class="metric-label">Annual Savings</span><br><span class="metric-value">₹{client_data["Premium Amount"].sum():,.0f}</span></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><span class="metric-label">Wealth Maturity</span><br><span class="metric-value">₹{client_data["Maturity Amount"].sum():,.0f}</span></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="metric-card"><span class="metric-label">Active Policies</span><br><span class="metric-value">{len(client_data)}</span></div>', unsafe_allow_html=True)

        # --- GAUGE & INSIGHTS ---
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            # Score Calculation
            score = min(int((client_data['Risk Coverage'].sum() / 5000000) * 100), 100)
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = score,
                title = {'text': "Protection Score"},
                gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#1e3d59"},
                         'steps': [{'range': [0, 50], 'color': "#ffe6e6"}, {'range': [50, 100], 'color': "#e6ffed"}]}))
            fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.markdown("### 💡 Recommendations")
            st.success("✅ Your life coverage is stable for current goals.")
            st.warning("⚠️ Diversification needed: Your debt-to-equity ratio is high.")
            
            st.markdown("---")
            # CALL TO ACTION BUTTONS
            st.markdown(f'<a href="tel:9892027934"><button style="width:100%; border-radius: 8px; height: 3.5em; background-color: #1e3d59; color: white; border: none; font-weight: bold; margin-bottom:10px;">📞 Talk to Advisor</button></a>', unsafe_allow_html=True)
            if st.button("📈 Improve My Score"):
                st.write("Redirecting to meeting scheduler...")
            
            csv = client_data.to_csv(index=False).encode('utf-8')
            st.download_button(label="📄 Download Report", data=csv, file_name=f"{client_name}_Portfolio.csv")

        # --- POLICY DETAILS ---
        st.write("### 📜 Family Policy Portfolio")
        st.dataframe(client_data[['Policy Holder', 'Policy No', 'Plan', 'Premium Amount', 'Status']], use_container_width=True, hide_index=True)

    else:
        st.error("No record found. Please verify your email with Vinod Gupta.")
else:
    st.info("Log in via the sidebar to access your Sattrex VIP Digital Notebook.")
