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
    
    /* Header & Navbar */
    .premium-header {
        background-color: white; padding: 1.2rem 2rem; border-bottom: 1px solid #E2E8F0;
        display: flex; justify-content: space-between; align-items: center;
        margin: -4rem -4rem 2rem -4rem;
    }
    .advisor-card {
        background: #F1F5F9; padding: 8px 16px; border-radius: 12px;
        display: flex; align-items: center; gap: 10px;
    }

    /* Cards & Insights */
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
        background-color: #1E3A8A; color: white !important; padding: 8px 18px;
        border-radius: 8px; text-decoration: none; font-size: 13px; font-weight: 600;
        display: inline-block; margin-top: 10px; transition: 0.3s;
    }
    .fix-btn:hover { opacity: 0.8; }

    /* Tags */
    .status-tag-well { background: #DCFCE7; color: #15803D; padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 700; }
    .status-tag-under { background: #FEE2E2; color: #B91C1C; padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# --- DATA PROCESSING ---
@st.cache_data
def load_and_process():
    try:
        # Load file (assuming it's in the same directory on GitHub)
        df = pd.read_excel("sample test.xlsx")
        
        # 1. Clean Column Names (Remove spaces/newlines)
        df.columns = df.columns.str.strip()
        
        # 2. Map Column Names based on your specific Excel structure
        col_map = {
            'Maturity Yee': 'Maturity Year',
            'Maturity Amo': 'Maturity Amount',
            'Premium Amount': 'Premium',
            'Risk Coverage': 'Coverage'
        }
        df = df.rename(columns=col_map)
        
        # 3. Numeric Cleaning
        numeric_targets = ['Coverage', 'Premium', 'Maturity Amount', 'Maturity Year']
        for col in numeric_targets:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # 4. Global Cleanup
        df = df.fillna("N/A")
        return df
    except Exception as e:
        st.error(f"⚠️ Error reading 'sample test.xlsx': {e}")
        return pd.DataFrame()

df = load_and_process()

# --- LOGIN LOGIC ---
with st.sidebar:
    st.image("logo.png", width=160)
    st.markdown("---")
    st.markdown("### 🔒 Client Access")
    email_input = st.text_input("Registered Email Address").strip().lower()

if email_input:
    # Find email column dynamically (handles login_email, Login_Email, etc)
    email_col_list = [c for c in df.columns if c.lower().strip() == 'login_email']
    
    if email_col_list:
        email_col = email_col_list[0]
        client_data = df[df[email_col].astype(str).str.lower().str.contains(email_input, na=False)]
        
        if not client_data.empty:
            # Cleanup Name for display
            raw_name = str(client_data['Main Account'].iloc[0])
            display_name = raw_name.split("-")[0].strip().title()

            # --- HEADER ---
            st.markdown(f"""
                <div class="premium-header">
                    <div>
                        <h2 style='margin:0; color:#1E3A8A;'>{display_name} | Family Office</h2>
                        <p style='margin:0; color:#64748B; font-size:13px;'>Last Updated: {datetime.now().strftime('%d %b, %Y')}</p>
                    </div>
                    <div class="advisor-card">
                        <div style="text-align: right;">
                            <div style="font-weight:700; color:#1E293B; font-size:14px;">Vinod Gupta</div>
                            <div style="color:#64748B; font-size:11px;">Senior Advisor</div>
                        </div>
                        <div style="width:38px; height:38px; background:#1E3A8A; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold;">VG</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # --- NAVIGATION TABS ---
            tab_prot, tab_wealth, tab_ins = st.tabs(["🛡️ Protection", "💰 Wealth", "📊 Insights"])

            with tab_prot:
                # Top Key Metrics
                m1, m2, m3, m4 = st.columns(4)
                tot_cov = client_data['Coverage'].sum()
                tot_prem = client_data['Premium'].sum()
                
                m1.markdown(f'<div class="f-card"><span style="color:#64748B; font-size:11px; font-weight:700;">TOTAL RISK COVER</span><div style="color:#1E3A8A; font-size:24px; font-weight:700;">₹{tot_cov/10000000:,.2f} Cr</div></div>', unsafe_allow_html=True)
                m2.markdown(f'<div class="f-card"><span style="color:#64748B; font-size:11px; font-weight:700;">ANNUAL PREMIUM</span><div style="color:#1E3A8A; font-size:24px; font-weight:700;">₹{tot_prem/100000:,.2f} L</div></div>', unsafe_allow_html=True)
                m3.markdown(f'<div class="f-card"><span style="color:#64748B; font-size:11px; font-weight:700;">ACTIVE POLICIES</span><div style="color:#1E3A8A; font-size:24px; font-weight:700;">{len(client_data)}</div></div>', unsafe_allow_html=True)
                m4.markdown(f'<div class="f-card"><span style="color:#64748B; font-size:11px; font-weight:700;">INSURANCE SCORE</span><div style="color:#10B981; font-size:24px; font-weight:700;">Optimal</div></div>', unsafe_allow_html=True)

                col_gauge, col_family = st.columns([1, 2])
                
                with col_gauge:
                    st.markdown("### Financial Health Score")
                    # Semi-Circle Gauge (Plotly)
                    score = 74 
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number", value = score,
                        gauge = {
                            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                            'bar': {'color': "#1E3A8A"},
                            'steps': [
                                {'range': [0, 40], 'color': "#FEE2E2"},
                                {'range': [41, 70], 'color': "#FEF3C7"},
                                {'range': [71, 100], 'color': "#D1FAE5"}]}))
                    fig.update_layout(height=250, margin=dict(t=10, b=0, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("""
                        <div class="f-card" style="margin-top:-30px;">
                            <p style="font-weight:700; color:#1E293B; font-size:14px; margin-bottom:10px;">Improve your score by:</p>
                            <ul style="font-size:13px; color:#475569; padding-left:18px; line-height:1.6;">
                                <li>Increasing cover for family members</li>
                                <li>Reviewing maturing policies in 2029</li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)

                with col_family:
                    st.markdown("### Family Member Overview")
                    f_cols = st.columns(3)
                    members = client_data['Policy Holder'].unique()
                    for i, m_name in enumerate(members[:3]):
                        m_cov = client_data[client_data['Policy Holder'] == m_name]['Coverage'].sum()
                        is_well = "Well Covered" if m_cov > 4000000 else "Underinsured"
                        tag_color = "status-tag-well" if is_well == "Well Covered" else "status-tag-under"
                        
                        with f_cols[i]:
                            st.markdown(f"""
                                <div class="f-card" style="padding:18px; border-top: 5px solid #1E3A8A;">
                                    <div style="font-weight:700; color:#1E3A8A; font-size:15px; margin-bottom:5px;">{m_name}</div>
                                    <div style="font-size:12px; color:#64748B; margin-bottom:12px;">Cover: ₹{m_cov/100000:,.1f} L</div>
                                    <span class="{tag_color}">{is_well}</span>
                                </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown("### Actionable Insights")
                    i1, i2 = st.columns(2)
                    with i1:
                        st.markdown("""
                            <div class="insight-card" style="border-color: #EF4444;">
                                <div style="font-weight:700; color:#B91C1C; font-size:14px;">High Priority Review</div>
                                <div style="font-size:12px; color:#475569; margin-top:5px;">A significant gap detected in health cover vs inflation.</div>
                                <a href="tel:9892027934" class="fix-btn">Fix Now</a>
                            </div>
                        """, unsafe_allow_html=True)
                    with i2:
                        st.markdown("""
                            <div class="insight-card" style="border-color: #10B981;">
                                <div style="font-weight:700; color:#065F46; font-size:14px;">Policy Maturity</div>
                                <div style="font-size:12px; color:#475569; margin-top:5px;">Policy ending in 2029 is nearing maturity. Plan reinvestment.</div>
                                <a href="#" class="fix-btn" style="background:#10B981;">Talk to Advisor</a>
                            </div>
                        """, unsafe_allow_html=True)

            with tab_wealth:
                st.markdown("### Maturity & Wealth Projections")
                w_df = client_data[client_data['Maturity Year'] > 2023].sort_values('Maturity Year')
                if not w_df.empty:
                    fig_w = px.area(w_df, x='Maturity Year', y='Maturity Amount', 
                                    line_shape='spline', color_discrete_sequence=['#1E3A8A'])
                    fig_w.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_w, use_container_width=True)
                else:
                    st.info("No future maturity data available for projection.")

            with tab_ins:
                st.markdown("### Policy Repository")
                # Clean table for display
                table_df = client_data[['Policy Holder', 'Policy No', 'Plan', 'Premium', 'Coverage', 'Status']].copy()
                st.dataframe(table_df, use_container_width=True, hide_index=True)

        else:
            st.error(f"Access Denied: No data found for '{email_input}'.")
    else:
        st.error("System Error: 'login_Email' column missing from data source.")
else:
    st.info("👋 Welcome to Sattrex Capital. Please enter your email in the sidebar to view your portfolio.")
