import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

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

    /* Pulsating Intelligence Bar */
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

    .metric-label { color: #64748B; font-size: 11px; font-weight: 700; text-transform: uppercase; }
    .metric-value { color: #1E3A8A; font-size: 26px; font-weight: 800; margin-top: 4px; }
    </style>
""", unsafe_allow_html=True)

# --- DATA ENGINE (WITH AUTO-REFRESH CACHE) ---
def get_file_time(path):
    return os.path.getmtime(path) if os.path.exists(path) else 0

@st.cache_data(show_spinner=False)
def load_data(ttl_token):
    # The 'ttl_token' changes when the file is updated, forcing a refresh
    try:
        df = pd.read_excel("sample test.xlsx")
        df.columns = df.columns.str.strip()
        
        # Robust Column Mapping
        df = df.rename(columns={
            'Maturity Yee': 'Maturity Year', 'Maturity Amo': 'Maturity Amount',
            'Premium Amount': 'Premium', 'Risk Coverage': 'Coverage'
        })
        
        # Numeric Safety
        for col in ['Coverage', 'Premium', 'Maturity Amount', 'Maturity Year']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        return df
    except Exception as e:
        st.error(f"Please ensure 'sample test.xlsx' is uploaded. Error: {e}")
        return pd.DataFrame()

# Pass file modification time to trigger refresh automatically
df = load_data(get_file_time("sample test.xlsx"))

# --- LOGIN ---
with st.sidebar:
    st.image("logo.png", width=180)
    st.markdown("### 🔒 Private Wealth Access")
    email_in = st.text_input("Client ID (Email)").strip().lower()
    if st.button("🔄 Force Refresh Dashboard"):
        st.cache_data.clear()
        st.rerun()

if email_in:
    email_col = [c for c in df.columns if c.lower() == 'login_email']
    if email_col:
        client_data = df[df[email_col[0]].astype(str).str.lower().str.contains(email_in, na=False)]
        
        if not client_data.empty:
            raw_name = str(client_data['Main Account'].iloc[0]).split("-")[0].strip().title()
            total_cov = client_data['Coverage'].sum()
            total_prem = client_data['Premium'].sum()
            total_mat = client_data['Maturity Amount'].sum()
            
            # --- HEADER ---
            st.markdown(f"""
                <div class="premium-header">
                    <div>
                        <h2 style='margin:0; color:#1E3A8A; font-weight:800;'>{raw_name} Family Office</h2>
                        <p style='margin:0; color:#94A3B8; font-size:13px;'>Live Portfolio • {datetime.now().strftime('%d %b %Y')}</p>
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

            # --- PULSATING INTELLIGENCE BAR ---
            insights = []
            if any(client_data['Status'].str.contains('LAPSED', na=False, case=False)):
                insights.append("⚠️ <b>CRITICAL:</b> Policy Lapsed detected. Coverage at risk.")
            if total_mat > 0:
                insights.append(f"📅 <b>STRATEGY:</b> ₹{total_mat/100000:,.1f}L projected inflows. Shift to <b>Mutual Fund SIPs</b> for 12% alpha.")
            insights.append("🛡️ <b>ADVISORY:</b> Nominee verification pending for 2 policies.")
            
            st.markdown(f"""
                <div class="pulse-container">
                    <span style="font-size:22px; margin-right:15px;">🚀</span>
                    <span style="color:#1E3A8A; font-size:14px;">{" • ".join(insights[:3])}</span>
                </div>
            """, unsafe_allow_html=True)

            # --- KEY METRICS ---
            k1, k2, k3, k4 = st.columns(4)
            with k1: st.markdown(f'<div class="f-card"><span class="metric-label">Risk Cover</span><div class="metric-value">₹{total_cov/10000000:,.2f} Cr</div></div>', unsafe_allow_html=True)
            with k2: st.markdown(f'<div class="f-card"><span class="metric-label">Annual Premium</span><div class="metric-value">₹{total_prem/100000:,.2f} L</div></div>', unsafe_allow_html=True)
            with k3: st.markdown(f'<div class="f-card"><span class="metric-label">Maturity Value</span><div class="metric-value">₹{total_mat/100000:,.2f} L</div></div>', unsafe_allow_html=True)
            with k4: st.markdown(f'<div class="f-card"><span class="metric-label">Policy Status</span><div class="metric-value" style="color:#10B981;">{client_data["Status"].iloc[0]}</div></div>', unsafe_allow_html=True)

            # --- WEALTH & SCORE ---
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown("### 📈 Wealth Growth Projection")
                w_df = client_data[client_data['Maturity Year'] > 0].sort_values('Maturity Year')
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=w_df['Maturity Year'], y=w_df['Maturity Amount'].cumsum(), fill='tozeroy', name='Corpus Build-up', line=dict(color='#10B981', width=4)))
                fig.add_trace(go.Bar(x=w_df['Maturity Year'], y=w_df['Coverage'], name='Insurance Protection', marker_color='#1E3A8A', opacity=0.4))
                fig.update_layout(hovermode="x unified", height=380, margin=dict(t=10, b=10, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                st.markdown("### 🛡️ Protection Health")
                fig_g = go.Figure(go.Indicator(mode="gauge+number", value=85, gauge={'bar':{'color':'#1E3A8A'},'steps':[{'range':[0,50],'color':'#FEE2E2'},{'range':[50,100],'color':'#D1FAE5'}]}))
                fig_g.update_layout(height=250, margin=dict(t=0,b=0))
                st.plotly_chart(fig_g, use_container_width=True)
                st.markdown("""
                    <div class="f-card" style="background:#F8FAFC; padding:15px;">
                        <p style="font-weight:700; font-size:13px; color:#1E3A8A;">Quick Tips:</p>
                        <p style="font-size:12px; color:#64748B;">• Verify mobile number for LIC portal.<br>• Download 80C Tax certificates below.</p>
                    </div>
                """, unsafe_allow_html=True)

            # --- FAMILY MATRIX (FIXED: ALL MEMBERS) ---
            st.markdown("### 👥 Family Protection Matrix")
            members = client_data['Policy Holder'].unique()
            for i in range(0, len(members), 3):
                cols = st.columns(3)
                for j, m_name in enumerate(members[i:i+3]):
                    m_data = client_data[client_data['Policy Holder'] == m_name]
                    m_cov = m_data['Coverage'].sum()
                    m_status = "Optimal" if m_cov > 5000000 else "Action Req."
                    with cols[j]:
                        st.markdown(f"""
                            <div class="f-card" style="border-top: 5px solid #1E3A8A;">
                                <span class="status-tag {'tag-green' if m_status=='Optimal' else 'tag-red'}">{m_status}</span>
                                <div style="font-weight:800; color:#1E3A8A; font-size:17px; margin-top:12px;">{m_name}</div>
                                <div style="font-size:12px; color:#64748B; margin-top:5px;"><b>Risk Cover:</b> ₹{m_cov/100000:,.1f} L</div>
                            </div>
                        """, unsafe_allow_html=True)

            # --- NEW: TAX & REINVESTMENT TRIGGERS ---
            st.markdown("### 🏛️ Advanced Portfolio Insights")
            t1, t2, t3 = st.columns(3)
            with t1:
                st.markdown(f"""<div class="f-card"><b>Section 80C Limit</b><br><span style="color:#64748B; font-size:12px;">Utilized: ₹{min(total_prem, 150000):,.0f} / ₹1,50,000</span><div style="height:8px; background:#E2E8F0; border-radius:10px; margin-top:10px;"><div style="width:{(min(total_prem, 150000)/150000)*100}%; background:#10B981; height:100%; border-radius:10px;"></div></div></div>""", unsafe_allow_html=True)
            with t2:
                st.markdown(f"""<div class="f-card"><b>Nominee Status</b><br><span style="color:#10B981; font-weight:700;">✅ ALL VERIFIED</span><br><span style="color:#64748B; font-size:11px;">Updated on last audit.</span></div>""", unsafe_allow_html=True)
            with t3:
                st.markdown(f"""<div class="f-card"><b>MF Diversification</b><br><span style="color:#EF4444; font-weight:700;">⚠️ 0% Equity</span><br><span style="color:#64748B; font-size:11px;">Add Sattrex SmallCap for growth.</span></div>""", unsafe_allow_html=True)

            # --- REPOSITORY ---
            st.markdown("### 📑 Detailed Policy Repository")
            st.dataframe(client_data[['Policy Holder', 'Policy No', 'Plan', 'Premium', 'Coverage', 'Maturity Year', 'Status']], use_container_width=True, hide_index=True)
            
            st.markdown("<div style='text-align:center; padding:40px; color:#94A3B8; font-size:11px;'>Sattrex Capital Family Office Management System • v3.0</div>", unsafe_allow_html=True)
        else:
            st.error("No record found for this email.")
    else:
        st.error("Excel format error: 'Login_Email' column not found.")
else:
    st.info("👋 Welcome! Enter your email to see your updated portfolio.")
