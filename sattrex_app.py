import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# --- CORE CONFIG ---
st.set_page_config(page_title="Sattrex Capital | Family Office", layout="wide", initial_sidebar_state="expanded")

# --- HIGH-END UI STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8FAFC; }
    .main { background-color: #F8FAFC; }
    
    .premium-header {
        background-color: white; padding: 1.5rem 2rem; border-bottom: 1px solid #E2E8F0;
        display: flex; justify-content: space-between; align-items: center;
        margin: -4rem -4rem 2rem -4rem;
    }
    .advisor-card {
        background: #F1F5F9; padding: 8px 16px; border-radius: 12px;
        display: flex; align-items: center; gap: 10px;
    }
    .f-card {
        background: white; padding: 24px; border-radius: 16px;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.05);
        border: 1px solid #F1F5F9; margin-bottom: 20px;
    }
    .insight-card {
        background: white; border-radius: 16px; padding: 20px;
        border-left: 6px solid #1E3A8A; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .fix-btn {
        background-color: #1E3A8A; color: white !important; padding: 8px 16px;
        border-radius: 8px; text-decoration: none; font-size: 13px; font-weight: 600;
        display: inline-block; margin-top: 10px;
    }
    .status-tag-well { background: #DCFCE7; color: #15803D; padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 600; }
    .status-tag-under { background: #FEE2E2; color: #B91C1C; padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# --- DATA PROCESSING (REFINED) ---
@st.cache_data
def load_and_process():
    try:
        df = pd.read_excel("sample test.xlsx")
        
        # Clean column names: remove hidden spaces and make a mapping
        df.columns = df.columns.str.strip()
        
        # Mapping your specific Excel column names
        col_map = {
            'Maturity Yee': 'Maturity Year',
            'Maturity Amo': 'Maturity Amount',
            'Premium Amount': 'Premium',
            'Risk Coverage': 'Coverage'
        }
        df = df.rename(columns=col_map)
        
        # Standardize numeric columns
        for col in ['Coverage', 'Premium', 'Maturity Amount']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return pd.DataFrame()

df = load_and_process()

# --- LOGIN (ERROR-RESISTANT) ---
with st.sidebar:
    st.image("logo.png", width=150)
    st.markdown("### 🔐 Secure Login")
    email_input = st.text_input("Enter Registered Email")

if email_input:
    # Dynamically find the email column regardless of case (login_email vs login_Email)
    email_col = [c for c in df.columns if c.lower() == 'login_email']
    
    if email_col:
        # Use the first matching column found
        client_data = df[df[email_col[0]].str.contains(email_input, na=False, case=False)]
        
        if not client_data.empty:
            # --- DASHBOARD RENDER CODE STARTS HERE ---
            name = client_data['Main Account'].iloc[0].replace("-", "").strip()
            st.success(f"Welcome, {name}")
            # ... (Rest of the UI code from the previous response)
        else:
            st.warning("No records found for this email.")
    else:
        st.error("Critical Error: The Excel file is missing a 'login_Email' column.")
        # --- HEADER ---
        st.markdown(f"""
            <div class="premium-header">
                <div>
                    <h2 style='margin:0; color:#1E3A8A;'>{name} | Family Office</h2>
                    <p style='margin:0; color:#64748B; font-size:13px;'>Last Sync: {datetime.now().strftime('%d %b, %Y')}</p>
                </div>
                <div class="advisor-card">
                    <div style="text-align: right;">
                        <div style="font-weight:700; color:#1E293B; font-size:14px;">Vinod Gupta</div>
                        <div style="color:#64748B; font-size:11px;">Primary Advisor</div>
                    </div>
                    <div style="width:36px; height:36px; background:#1E3A8A; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold;">VG</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # --- TABS ---
        t_prot, t_wealth, t_ins = st.tabs(["🛡️ Protection", "📈 Wealth", "💡 Insights"])

        with t_prot:
            # Metrics Row
            m1, m2, m3, m4 = st.columns(4)
            total_cov = client_data['Coverage'].sum()
            total_prem = client_data['Premium'].sum()
            
            m1.markdown(f'<div class="f-card"><span style="color:#64748B; font-size:11px; font-weight:600;">LIFE COVER</span><div style="color:#1E3A8A; font-size:22px; font-weight:700;">₹{total_cov/10000000:,.2f} Cr</div></div>', unsafe_allow_html=True)
            m2.markdown(f'<div class="f-card"><span style="color:#64748B; font-size:11px; font-weight:600;">ANNUAL OUTFLOW</span><div style="color:#1E3A8A; font-size:22px; font-weight:700;">₹{total_prem/100000:,.2f} L</div></div>', unsafe_allow_html=True)
            m3.markdown(f'<div class="f-card"><span style="color:#64748B; font-size:11px; font-weight:600;">TOTAL POLICIES</span><div style="color:#1E3A8A; font-size:22px; font-weight:700;">{len(client_data)}</div></div>', unsafe_allow_html=True)
            m4.markdown(f'<div class="f-card"><span style="color:#64748B; font-size:11px; font-weight:600;">AVG STATUS</span><div style="color:#10B981; font-size:22px; font-weight:700;">Healthy</div></div>', unsafe_allow_html=True)

            c_left, c_right = st.columns([1, 2])
            
            with c_left:
                st.markdown("#### Health Score")
                score = 78 # Example score
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number", value = score,
                    gauge = {
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#1E3A8A"},
                        'steps': [
                            {'range': [0, 40], 'color': '#FEE2E2'},
                            {'range': [40, 70], 'color': '#FEF3C7'},
                            {'range': [70, 100], 'color': '#D1FAE5'}]}))
                fig.update_layout(height=220, margin=dict(t=0, b=0, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("""
                    <div class="f-card" style="margin-top:-20px; padding:15px;">
                        <p style="font-weight:700; font-size:13px;">How to improve:</p>
                        <p style="font-size:12px; color:#475569;">• Add Critical Illness rider to Policy ending in ...8803<br>• Increase cover for spouse</p>
                    </div>
                """, unsafe_allow_html=True)

            with c_right:
                st.markdown("#### Family Member Status")
                f_cols = st.columns(3)
                members = client_data['Policy Holder'].unique()
                for i, m_name in enumerate(members[:3]):
                    m_cov = client_data[client_data['Policy Holder'] == m_name]['Coverage'].sum()
                    is_well = "Well Covered" if m_cov > 5000000 else "Underinsured"
                    is_class = "status-tag-well" if is_well == "Well Covered" else "status-tag-under"
                    with f_cols[i]:
                        st.markdown(f"""
                            <div class="f-card" style="padding:15px; border-top:4px solid #1E3A8A;">
                                <div style="font-weight:700; color:#1E3A8A; font-size:14px;">{m_name}</div>
                                <div style="font-size:11px; color:#64748B; margin-bottom:10px;">Cover: ₹{m_cov/100000:,.1f} L</div>
                                <span class="{is_class}">{is_well}</span>
                            </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("#### Priority Actions")
                st.markdown("""
                    <div style="display:flex; gap:15px;">
                        <div class="insight-card" style="flex:1; border-color:#F59E0B;">
                            <div style="font-weight:700; color:#92400E; font-size:14px;">Review Coverage</div>
                            <div style="font-size:12px;">Based on your age (Commencement 2009), a top-up is advised.</div>
                            <a href="#" class="fix-btn" style="background:#F59E0B;">Talk to Advisor</a>
                        </div>
                        <div class="insight-card" style="flex:1; border-color:#10B981;">
                            <div style="font-weight:700; color:#065F46; font-size:14px;">Maturity Incoming</div>
                            <div style="font-size:12px;">Policy #...4097 matures in 2039. Plan reinvestment now.</div>
                            <a href="#" class="fix-btn" style="background:#10B981;">View Plan</a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        with t_wealth:
            st.markdown("### Estimated Maturity Timeline")
            wealth_data = client_data[client_data['Maturity Year'] != 0].sort_values('Maturity Year')
            if not wealth_data.empty:
                fig_wealth = px.bar(wealth_data, x='Maturity Year', y='Maturity Amount', 
                                    color_discrete_sequence=['#1E3A8A'], title="Projected Inflows")
                fig_wealth.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_wealth, use_container_width=True)
            else:
                st.info("No future maturity dates found in records.")

        with t_ins:
            st.markdown("### Policy Repository")
            # Cleaning the display dataframe
            disp = client_data[['Policy Holder', 'Policy No', 'Plan', 'Premium', 'Coverage', 'Status']].copy()
            st.dataframe(disp, use_container_width=True, hide_index=True)

    else:
        st.warning("No records found for this email. Please check the spelling.")
else:
    st.info("👋 Welcome! Please enter your email in the sidebar to access your Family Office dashboard.")
