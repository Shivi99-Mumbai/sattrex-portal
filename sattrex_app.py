import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sattrex Capital Portal", layout="wide")

# --- CUSTOM CSS FOR FINTECH LOOK ---
st.markdown("""
    <style>
    .metric-container { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center; border-bottom: 4px solid #1e3d59; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 10px 10px 0 0; padding: 10px 20px; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #1e3d59; color: white ! impossant; }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_excel("sample test.xlsx")
    # Clean numbers for math
    for col in ['Risk Coverage', 'Premium Amount', 'Maturity Amount']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

df = load_data()

# --- SIDEBAR LOGIN ---
st.sidebar.image("logo.png", width=180)
st.sidebar.title("VIP Access")
email = st.sidebar.text_input("Registered Email ID")
otp = st.sidebar.text_input("Enter OTP", type="password")

if email and otp == "123456":
    client_data = df[df['Login_Email'].str.contains(email, na=False, case=False)]
    
    if not client_data.empty:
        client_name = client_data['Main Account'].iloc[0]
        st.title(f"🏛️ Sattrex VIP Dashboard: {client_name}")
        
        # --- TABBED VIEW ---
        tab1, tab2, tab3 = st.tabs(["🛡️ Protection Audit", "📈 Wealth Strategy", "🔔 Notification Center"])

        with tab1:
            # 1. Protection Score Logic
            total_risk = client_data['Risk Coverage'].sum()
            total_prem = client_data['Premium Amount'].sum()
            protection_score = min(int((total_risk / (total_prem * 15)) * 100), 100) if total_prem > 0 else 0
            
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f'<div class="metric-container"><h3>Protection Score</h3><h1 style="color:#1e3d59;">{protection_score}%</h1></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="metric-container"><h3>Total Life Cover</h3><h1>₹{total_risk/100000:,.1f}L</h1></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="metric-container"><h3>Future Wealth</h3><h1>₹{client_data["Maturity Amount"].sum()/100000:,.1f}L</h1></div>', unsafe_allow_html=True)
            with c4:
                st.markdown(f'<div class="metric-container"><h3>Annual Savings</h3><h1>₹{total_prem:,.0f}</h1></div>', unsafe_allow_html=True)

            # 2. Maturity Timeline Graph
            st.write("### 📊 Wealth Maturity Timeline")
            # Cleaning Maturity Year for Chart
            client_data['Year'] = pd.to_numeric(client_data['Maturity Year'], errors='coerce')
            timeline_df = client_data.groupby('Year')['Maturity Amount'].sum().reset_index()
            fig = px.bar(timeline_df, x='Year', y='Maturity Amount', 
                         title="When your money comes back to you",
                         color_discrete_sequence=['#1e3d59'])
            st.plotly_chart(fig, use_container_width=True)

            # 3. Recommendations (The "Genius" Prompts)
            st.write("### 💡 AI Recommendations")
            if protection_score < 70:
                st.error(f"⚠️ **Action Required:** Your Protection Score is {protection_score}%. You are under-insured. We recommend adding a ₹1Cr Term Cover.")
            else:
                st.success("🌟 **Excellent:** Your family is well-protected. We recommend focusing on 'Wealth Creation' now.")

        with tab2:
            st.subheader("Asset Allocation & Wealth Growth")
            st.info("Syncing Mutual Fund Data... Your live XIRR and Goal Tracking will appear here shortly.")
            # Dummy Pie Chart
            pie_fig = px.pie(names=['Fixed Income', 'Equities', 'Gold'], values=[70, 20, 10], hole=0.5)
            st.plotly_chart(pie_fig)

        with tab3:
            st.subheader("Your Reminders")
            st.write("✅ All premiums for April 2026 are cleared.")
            st.warning("Upcoming: ₹45,000 due on 15th May 2026 (HDFC Life).")

    else:
        st.error("Access Denied: Email not registered.")
else:
    st.info("Welcome to Sattrex Capital. Please use the sidebar to access your private wealth notebook.")
