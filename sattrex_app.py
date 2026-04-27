import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os
import random

# --- CORE CONFIG ---
st.set_page_config(page_title="Sattrex Capital | Family Office", layout="wide", initial_sidebar_state="expanded")

# --- PREMIUM FINTECH CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8FAFC; }
    
    .premium-header {
        background-color: white; padding: 1.2rem 2.5rem; border-bottom: 1px solid #E2E8F0;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; margin: -4rem -4rem 1.5rem -4rem;
    }
    .advisor-card {
        background: #F1F5F9; padding: 8px 16px; border-radius: 12px;
        display: flex; align-items: center; gap: 10px; border: 1px solid #E2E8F0;
    }

    .pulse-container {
        background: #FFFFFF; border-left: 6px solid #1E3A8A; border-radius: 12px;
        padding: 16px 24px; margin-bottom: 30px; display: flex; align-items: center;
        box-shadow: 0 10px 15px -3px rgba(30, 58, 138, 0.1);
        animation: pulse-shadow 2.5s infinite;
    }
    @keyframes pulse-shadow {
        0% { box-shadow: 0 0 0 0 rgba(30, 58, 138, 0.2); }
        70% { box-shadow: 0 0 0 12px rgba(30, 58, 138, 0); }
        100% { box-shadow: 0 0 0 0 rgba(30, 58, 138, 0); }
    }

    .f-card {
        background: white; padding: 24px; border-radius: 16px;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.04);
        border: 1px solid #F1F5F9; margin-bottom: 25px;
    }
    .status-tag { padding: 5px 12px; border-radius: 20px; font-size: 10px; font-weight: 800; text-transform: uppercase; }
    .tag-green { background: #D1FAE5; color: #065F46; }
    .tag-red { background: #FEE2E2; color: #991B1B; }
    .tag-blue { background: #DBEAFE; color: #1E40AF; }

    .btn-pay {
        background-color: #10B981; color: white !important; padding: 12px 24px;
        border-radius: 10px; text-decoration: none; font-weight: 700; font-size: 14px;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.2); transition: 0.3s;
    }
    .btn-invest {
        background-color: #1E3A8A; color: white !important; padding: 12px;
        border-radius: 8px; text-decoration: none; font-weight: 600; display: block;
        text-align: center; margin-top: 15px; font-size: 13px;
    }
    .metric-label { color: #64748B; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; }
    .metric-value { color: #1E3A8A; font-size: 26px; font-weight: 800; margin-top: 4px; }
    </style>
""", unsafe_allow_html=True)

# --- CACHE REFRESH ENGINE ---
def get_file_mtime(filepath):
    return os.path.getmtime(filepath) if os.path.exists(filepath) else 0

@st.cache_data
def load_data(mtime):
    try:
        df = pd.read_excel("sample test.xlsx")
        df.columns = df.columns.str.strip()
        df = df.rename(columns={
            'Maturity Yee': 'Maturity Year',
            'Maturity Amo': 'Maturity Amount',
            'Premium Amount': 'Premium',
            'Risk Coverage': 'Coverage'
        })
        for col in ['Coverage', 'Premium', 'Maturity Amount', 'Maturity Year']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        return df
    except Exception as e:
        st.error(f"Data Load Error: {e}")
        return pd.DataFrame()

# Automatically refresh if file on disk changes
df = load_data(get_file_mtime("sample test.xlsx"))

# --- AUTHENTICATION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False
if 'generated_otp' not in st.session_state:
    st.session_state.generated_otp = None

# --- SIDEBAR LOGIN ---
with st.sidebar:
    st.image("logo.png", width=180)
    st.markdown("### 🔒 Private Wealth Access")
    
    if not st.session_state.authenticated:
        email_in = st.text_input("Registered Email").strip().lower()
        
        if not st.session_state.otp_sent:
            if st.button("Send Access OTP"):
                if email_in in df['Login_Email'].str.lower().values:
                    st.session_state.generated_otp = str(random.randint(100000, 999999))
                    st.session_state.otp_sent = True
                    # In a real app, you would call an email API here. 
                    # For demo, we show it in a temporary info box.
                    st.info(f"OTP sent to {email_in} (Code: {st.session_state.generated_otp})")
                else:
                    st.error("Email not recognized.")
        else:
            otp_in = st.text_input("Enter 6-Digit OTP", type="password")
            if st.button("Verify & Login"):
                if otp_in == st.session_state.generated_otp:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email_in
                    st.rerun()
                else:
                    st.error("Invalid OTP.")
            if st.button("Back to Email"):
                st.session_state.otp_sent = False
                st.rerun()
    else:
        st.success(f"Logged in: {st.session_state.user_email}")
        if st.button("Log Out"):
            st.session_state.authenticated = False
            st.session_state.otp_sent = False
            st.rerun()

# --- DASHBOARD RENDER ---
if st.session_state.authenticated:
    email_col = [c for c in df.columns if c.lower() == 'login_email'][0]
    client_all_data = df[df[email_col].astype(str).str.lower().str.contains(st.session_state.user_email, na=False)]
    
    # Logic for Matured vs Active
    active_data = client_all_data[client_all_data['Status'].str.upper() != 'MATURED']
    matured_data = client_all_data[client_all_data['Status'].str.upper() == 'MATURED']
    
    if not client_all_data.empty:
        raw_name = str(client_all_data['Main Account'].iloc[0]).split("-")[0].strip().title()
        
        # Metrics based on ACTIVE policies only
        total_cov = active_data['Coverage'].sum()
        total_prem = active_data['Premium'].sum()
        active_mat_future = active_data['Maturity Amount'].sum()
        
        # Metric based on MATURED policies
        realized_wealth = matured_data['Maturity Amount'].sum() if not matured_data.empty else 0

        # --- 1. HEADER ---
        st.markdown(f"""
            <div class="premium-header">
                <div>
                    <h2 style='margin:0; color:#1E3A8A; font-weight:800;'>{raw_name} Family Office</h2>
                    <p style='margin:0; color:#94A3B8; font-size:13px;'>Secure Portal • {datetime.now().strftime('%d %b %Y')}</p>
                </div>
                <div style="display:flex; align-items:center; gap:25px;">
                    <a href="https://ebiz.licindia.in/D2CPM/#DirectPay" target="_blank" class="btn-pay">💳 PAY PREMIUM NOW</a>
                    <div class="advisor-card">
                        <div style="text-align: right;">
                            <div style="font-weight:700; color:#1E293B; font-size:13px;">Vinod Gupta</div>
                            <div style="color:#64748B; font-size:11px;">Principal Advisor</div>
                        </div>
                        <div style="width:40px; height:40px; background:#1E3A8A; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold;">VG</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # --- 2. PULSATING INSIGHT BAR ---
        insights = []
        if any(active_data['Status'].str.contains('LAPSED', na=False, case=False)):
            insights.append("⚠️ <b>CRITICAL:</b> Protection Gap detected. Please pay grace premiums to avoid cover loss.")
        if not matured_data.empty:
            insights.append(f"💰 <b>REALIZED WEALTH:</b> ₹{realized_wealth/100000:,.1f}L already received from matured plans.")
        insights.append("🛡️ <b>ADVISORY:</b> All family nominees are currently verified.")
        
        st.markdown(f"""
            <div class="pulse-container">
                <span style="font-size:22px; margin-right:15px;">🚀</span>
                <span style="color:#1E3A8A; font-size:14px;">{" • ".join(insights[:3])}</span>
            </div>
        """, unsafe_allow_html=True)

        # --- 3. CORE METRICS ---
        k1, k2, k3, k4 = st.columns(4)
        with k1: st.markdown(f'<div class="f-card"><span class="metric-label">Active Risk Cover</span><div class="metric-value">₹{total_cov/10000000:,.2f} Cr</div></div>', unsafe_allow_html=True)
        with k2: st.markdown(f'<div class="f-card"><span class="metric-label">Matured (Received)</span><div class="metric-value" style="color:#10B981;">₹{realized_wealth/100000:,.1f} L</div></div>', unsafe_allow_html=True)
        with k3: st.markdown(f'<div class="f-card"><span class="metric-label">Annual Outflow</span><div class="metric-value">₹{total_prem/100000:,.2f} L</div></div>', unsafe_allow_html=True)
        with k4: st.markdown(f'<div class="f-card"><span class="metric-label">Future Maturity</span><div class="metric-value">₹{active_mat_future/100000:,.1f} L</div></div>', unsafe_allow_html=True)

        # --- 4. HEALTH & RECOS ---
        r_left, r_right = st.columns([1, 2])
        with r_left:
            st.markdown("### 🛡️ Protection Health")
            fig_g = go.Figure(go.Indicator(mode="gauge+number", value=82, gauge={'bar':{'color':'#1E3A8A'},'steps':[{'range':[0,50],'color':'#FEE2E2'},{'range':[50,100],'color':'#D1FAE5'}]}))
            fig_g.update_layout(height=260, margin=dict(t=0, b=0), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_g, use_container_width=True)
        
        with r_right:
            st.markdown("### 🎯 Strategic Insights")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""<div class="f-card" style="border-left:5px solid #1E3A8A;"><b>Investment Trigger</b><br><span style="font-size:12px; color:#64748B;">Use your matured corpus of ₹{realized_wealth/100000:,.1f}L for <b>Sattrex Equity SIPs</b> to beat inflation.</span><a href="tel:9892027934" class="btn-invest">Contact Advisor</a></div>""", unsafe_allow_html=True)
            with c2:
                st.markdown("""<div class="f-card" style="border-left:5px solid #10B981;"><b>Tax Benefit (80C)</b><br><span style="font-size:12px; color:#64748B;">You have fully utilized the ₹1.5L tax limit through current premiums. No extra ELSS needed.</span></div>""", unsafe_allow_html=True)

        # --- 5. WEALTH CHART ---
        st.markdown("### 📈 Wealth & Protection Timeline")
        w_df = active_data[active_data['Maturity Year'] > 0].sort_values('Maturity Year')
        fig_w = go.Figure()
        fig_w.add_trace(go.Scatter(x=w_df['Maturity Year'], y=w_df['Maturity Amount'].cumsum(), fill='tozeroy', name='Projected Corpus', line=dict(color='#10B981', width=4)))
        fig_w.add_trace(go.Bar(x=w_df['Maturity Year'], y=w_df['Coverage'], name='Active Life Cover', marker_color='#1E3A8A', opacity=0.7))
        fig_w.update_layout(hovermode="x unified", height=350, margin=dict(t=20, b=20, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_w, use_container_width=True)

        # --- 6. FAMILY PROTECTION (ALL MEMBERS) ---
        st.markdown("### 👥 Family Protection Matrix")
        all_holders = client_all_data['Policy Holder'].unique()
        for i in range(0, len(all_holders), 3):
            cols = st.columns(3)
            for j, m_name in enumerate(all_holders[i:i+3]):
                m_rows = client_all_data[client_all_data['Policy Holder'] == m_name]
                m_cov = m_rows[m_rows['Status'].str.upper() != 'MATURED']['Coverage'].sum()
                tag_cls = "tag-green" if m_cov > 3000000 else "tag-red"
                with cols[j]:
                    st.markdown(f"""
                        <div class="f-card" style="border-top: 5px solid #1E3A8A;">
                            <span class="status-tag {tag_cls}">{'Optimal' if m_cov > 3000000 else 'Action Required'}</span>
                            <div style="font-weight:800; color:#1E3A8A; font-size:16px; margin-top:12px;">{m_name}</div>
                            <div style="font-size:12px; color:#64748B; margin-top:5px;">Risk Cover: ₹{m_cov/100000:,.1f} L</div>
                            <div style="font-size:10px; color:#94A3B8; margin-top:5px;">Managed By: Sattrex Capital (LIC)</div>
                        </div>
                    """, unsafe_allow_html=True)

        # --- 7. REPOSITORY ---
        st.markdown("### 📑 Detailed Portfolio Repository")
        st.dataframe(client_all_data[['Policy Holder', 'Policy No', 'Plan', 'Premium', 'Coverage', 'Maturity Year', 'Status']], use_container_width=True, hide_index=True)
        
        st.markdown("<div style='text-align:center; padding:40px; color:#94A3B8; font-size:11px;'>Sattrex Capital Family Office Management System • v2.6</div>", unsafe_allow_html=True)
else:
    st.info("👋 Welcome. Please use the sidebar to log in with your registered email and OTP.")
