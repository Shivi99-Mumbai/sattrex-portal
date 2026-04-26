import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- CORE CONFIG ---
st.set_page_config(page_title="Sattrex Capital | Family Office", layout="wide")

# --- PROFESSIONAL FINTECH STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8FAFC; }
    
    /* Global Card Style */
    .f-card {
        background: white; padding: 24px; border-radius: 16px;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.04);
        border: 1px solid #E2E8F0; margin-bottom: 20px;
    }
    
    /* Family Member Cards */
    .member-card {
        background: #FFFFFF; border: 1px solid #E2E8F0;
        padding: 15px; border-radius: 12px; margin-bottom: 10px;
        border-left: 5px solid #1E3A8A;
    }
    .status-tag {
        padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700;
        text-transform: uppercase; float: right;
    }
    
    /* Typography */
    .stat-label { color: #64748B; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .stat-value { color: #1E293B; font-size: 22px; font-weight: 700; }
    .stat-sub { color: #94A3B8; font-size: 11px; }

    /* Professional Buttons */
    .btn-primary { background-color: #1E3A8A; color: white; padding: 12px; border-radius: 8px; text-align: center; text-decoration: none; display: block; font-weight: 600; margin-top: 10px; }
    .btn-pay { background-color: #10B981; color: white; padding: 14px; border-radius: 8px; text-align: center; text-decoration: none; display: block; font-weight: 700; font-size: 16px; }
    
    /* Pulse Notification */
    .pulse-notif {
        background: #FFFBEB; border: 1px solid #FEF3C7; color: #92400E;
        padding: 15px; border-radius: 12px; border-left: 6px solid #F59E0B;
        margin-bottom: 25px; font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATA PROCESSING ---
@st.cache_data
def load_and_process():
    df = pd.read_excel("sample test.xlsx")
    # Mapping missing values to "Not Available" for professional look
    num_cols = ['Risk Coverage', 'Premium Amount', 'Maturity Amount', 'Maturity Year']
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

df = load_and_process()

# --- LOGIN SIMULATION ---
st.sidebar.image("logo.png", width=200)
st.sidebar.markdown("### 🔐 Client Authentication")
email = st.sidebar.text_input("Registered Email ID")
otp = st.sidebar.text_input("Access PIN", type="password")

if email and otp == "123456":
    client_data = df[df['Login_Email'].str.contains(email, na=False, case=False)]
    
    if not client_data.empty:
        name = client_data['Main Account'].iloc[0]
        
        # --- TOP HEADER ---
        h1, h2 = st.columns([3, 1])
        with h1:
            st.title(f"Portfolio of {name}")
            st.markdown("**Advisor:** Vinod Gupta | **Firm:** Sattrex Capital")
        with h2:
            st.markdown('<br><a href="https://ebiz.licindia.in/D2CPM/#DirectPay" class="btn-pay">PAY PREMIUM NOW</a>', unsafe_allow_html=True)

        # --- DYNAMIC INTELLIGENCE BAR ---
        st.markdown(f"""
            <div class="pulse-notif">
                💼 <b>SATTREX INSIGHT:</b> 1 policy is reaching maturity in {int(client_data['Maturity Year'].max())}. 
                We recommend a reinvestment strategy review.
            </div>
        """, unsafe_allow_html=True)

        # --- KEY METRICS (With Short-Approx labels) ---
        st.markdown("### 🏛️ Key Financial Metrics")
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f'<div class="f-card"><span class="stat-label">Total Coverage</span><div class="stat-value">₹{client_data["Risk Coverage"].sum()/10000000:,.2f} Cr <span class="stat-sub">(Approx)</span></div></div>', unsafe_allow_html=True)
        with k2:
            st.markdown(f'<div class="f-card"><span class="stat-label">Annual Premium</span><div class="stat-value">₹{client_data["Premium Amount"].sum()/100000:,.2f} L <span class="stat-sub">(Approx)</span></div></div>', unsafe_allow_html=True)
        with k3:
            st.markdown(f'<div class="f-card"><span class="stat-label">Maturity Value</span><div class="stat-value">₹{client_data["Maturity Amount"].sum()/100000:,.2f} L <span class="stat-sub">(Approx)</span></div></div>', unsafe_allow_html=True)
        with k4:
            st.markdown(f'<div class="f-card"><span class="stat-label">Active Policies</span><div class="stat-value">{len(client_data)} <span class="stat-sub">Across Members</span></div></div>', unsafe_allow_html=True)

        # --- MIDDLE SECTION: SCORE & ANALYTICS ---
        col_left, col_right = st.columns([1, 2])
        
        with col_left:
            st.markdown("### 🛡️ Insured Score")
            score = 68 # Static for demo, can be dynamic
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = score,
                gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#1E3A8A"},
                         'steps': [{'range': [0, 50], 'color': "#FEE2E2"}, {'range': [50, 100], 'color': "#ECFDF5"}]}))
            fig.update_layout(height=280, margin=dict(t=30, b=0, l=10, r=10))
            st.plotly_chart(fig, use_container_width=True)
            st.info("**Sattrex Analysis:** You are moderately protected. Health insurance gap of ₹10L detected.")

        with col_right:
            st.markdown("### 📊 Wealth Projections")
            # Sample Growth Graph
            growth_df = pd.DataFrame({'Year': [2022, 2023, 2024, 2025, 2026], 'Wealth': [10, 25, 45, 68, 82.5]})
            fig_growth = px.area(growth_df, x='Year', y='Wealth', color_discrete_sequence=['#1E3A8A'])
            fig_growth.update_layout(height=300, plot_bgcolor='rgba(0,0,0,0)', yaxis_title="Value in Lakhs")
            st.plotly_chart(fig_growth, use_container_width=True)

        # --- FAMILY COVERAGE OVERVIEW (THE MISSING PIECE) ---
        st.write("---")
        st.markdown("### 👥 Family Coverage Overview")
        f1, f2, f3, f4 = st.columns(4)
        
        # Iterating through unique members in the data
        members = client_data['Policy Holder'].unique()
        cols = [f1, f2, f3, f4]
        
        for i, member in enumerate(members[:4]): # Showing up to 4 family members
            member_total = client_data[client_data['Policy Holder'] == member]['Risk Coverage'].sum()
            with cols[i]:
                st.markdown(f"""
                <div class="member-card">
                    <span class="status-tag" style="background:#ECFDF5; color:#065F46;">Covered</span>
                    <div style="font-weight:700; color:#1E3A8A;">{member}</div>
                    <div style="font-size:11px; color:#64748B;">Total Risk: ₹{member_total/100000:,.1f} L</div>
                    <a href="tel:9892027934" style="font-size:10px; color:#1E3A8A; font-weight:700;">UPDATE INFO</a>
                </div>
                """, unsafe_allow_html=True)

        # --- DETAILED REPOSITORY ---
        st.write("---")
        st.markdown("### 📑 Policy Repository")
        # Replace 0 with "Not Available" for the table
        display_df = client_data[['Policy Holder', 'Policy No', 'Plan', 'Premium Amount', 'Risk Coverage', 'Maturity Amount', 'Status']].copy()
        for col in ['Risk Coverage', 'Maturity Amount']:
            display_df[col] = display_df[col].apply(lambda x: f"₹{x:,.0f}" if x > 0 else "Not Available")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # --- ADVISOR CTA ---
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c2:
            st.markdown('<a href="tel:9892027934" class="btn-primary">📞 TALK TO VINOD GUPTA</a>', unsafe_allow_html=True)

    else:
        st.error("Credential Error: Data not found.")
else:
    st.info("Welcome to the Sattrex Family Office. Please enter your credentials to begin.")
