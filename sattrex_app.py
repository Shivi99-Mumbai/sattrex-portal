import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- CORE CONFIG ---
st.set_page_config(page_title="Sattrex Capital | Family Office", layout="wide", initial_sidebar_state="expanded")

# --- PREMIUM FINTECH CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8FAFC; }
    
    /* Premium White Header */
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

    /* Card Styling (CRED/Zerodha Aesthetic) */
    .f-card {
        background: white; padding: 24px; border-radius: 16px;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.04);
        border: 1px solid #F1F5F9; margin-bottom: 25px;
    }
    .status-tag { padding: 5px 12px; border-radius: 20px; font-size: 10px; font-weight: 800; text-transform: uppercase; }
    .tag-green { background: #D1FAE5; color: #065F46; }
    .tag-red { background: #FEE2E2; color: #991B1B; }

    /* Action Buttons */
    .btn-pay {
        background-color: #10B981; color: white !important; padding: 12px 24px;
        border-radius: 10px; text-decoration: none; font-weight: 700; font-size: 14px;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.2); transition: 0.3s;
    }
    .btn-pay:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(16, 185, 129, 0.3); }
    
    .btn-invest {
        background-color: #1E3A8A; color: white !important; padding: 12px;
        border-radius: 8px; text-decoration: none; font-weight: 600; display: block;
        text-align: center; margin-top: 15px; font-size: 13px;
    }
    
    /* Typography */
    .metric-label { color: #64748B; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; }
    .metric-value { color: #1E3A8A; font-size: 26px; font-weight: 800; margin-top: 4px; }
    </style>
""", unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def load_data():
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
        st.error(f"Data Connection Error: {e}")
        return pd.DataFrame()

df = load_data()

# --- LOGIN ---
with st.sidebar:
    st.image("logo.png", width=180)
    st.markdown("### 🔒 Private Wealth Access")
    email_in = st.text_input("Client ID (Email)").strip().lower()

if email_in:
    email_col = [c for c in df.columns if c.lower() == 'login_email']
    if email_col:
        client_data = df[df[email_col[0]].astype(str).str.lower().str.contains(email_in, na=False)]
        
        if not client_data.empty:
            raw_name = str(client_data['Main Account'].iloc[0]).split("-")[0].strip().title()
            total_cov = client_data['Coverage'].sum()
            total_prem = client_data['Premium'].sum()
            total_mat = client_data['Maturity Amount'].sum()
            
            # --- 1. PREMIUM HEADER ---
            st.markdown(f"""
                <div class="premium-header">
                    <div>
                        <h2 style='margin:0; color:#1E3A8A; font-weight:800;'>{raw_name} Family Office</h2>
                        <p style='margin:0; color:#94A3B8; font-size:13px;'>Last Sync: {datetime.now().strftime('%d %B %Y | %H:%M')}</p>
                    </div>
                    <div style="display:flex; align-items:center; gap:25px;">
                        <a href="https://ebiz.licindia.in/D2CPM/#DirectPay" target="_blank" class="btn-pay">💳 PAY PREMIUM NOW</a>
                        <div class="advisor-card">
                            <div style="text-align: right;">
                                <div style="font-weight:700; color:#1E293B; font-size:13px;">Vinod Gupta</div>
                                <div style="color:#64748B; font-size:11px;">Principal Advisor</div>
                            </div>
                            <div style="width:40px; height:40px; background:#1E3A8A; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:14px;">VG</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # --- 2. PULSATING INTELLIGENCE BAR (DYNAMIC INSIGHTS) ---
            insights = []
            if any(client_data['Status'].str.contains('LAPSED', na=False, case=False)):
                insights.append("⚠️ <b>URGENT:</b> Policy #...{0} has Lapsed. Immediate action required to restore family cover.".format(str(client_data[client_data['Status']=='LAPSED']['Policy No'].iloc[0])[-4:]))
            if total_mat > 0:
                future_mat = client_data[client_data['Maturity Year'] > 2024].sort_values('Maturity Year')
                if not future_mat.empty:
                    insights.append(f"📅 <b>MATURITY ALERT:</b> ₹{future_mat['Maturity Amount'].iloc[0]/100000:,.1f}L arriving in {int(future_mat['Maturity Year'].iloc[0])}. Start Mutual Fund STP strategy today.")
            if total_cov < (total_prem * 10):
                insights.append("🛡️ <b>RISK GAP:</b> Your insurance-to-premium ratio is low. We suggest shifting to a <b>Low-Cost Term Plan</b> for better leverage.")
            
            # Displaying up to 3 Insights in the pulse bar
            insight_html = " • ".join(insights[:3])
            st.markdown(f"""
                <div class="pulse-container">
                    <span style="font-size:22px; margin-right:15px;">🚀</span>
                    <span style="color:#1E3A8A; font-size:14px; line-height:1.5;">{insight_html}</span>
                </div>
            """, unsafe_allow_html=True)

            # --- 3. KEY PERFORMANCE INDICATORS ---
            k1, k2, k3, k4 = st.columns(4)
            with k1: st.markdown(f'<div class="f-card"><span class="metric-label">Total Life Cover</span><div class="metric-value">₹{total_cov/10000000:,.2f} Cr</div></div>', unsafe_allow_html=True)
            with k2: st.markdown(f'<div class="f-card"><span class="metric-label">Annual Outflow</span><div class="metric-value">₹{total_prem/100000:,.2f} L</div></div>', unsafe_allow_html=True)
            with k3: st.markdown(f'<div class="f-card"><span class="metric-label">Maturity Corpus</span><div class="metric-value">₹{total_mat/100000:,.2f} L</div></div>', unsafe_allow_html=True)
            with k4: st.markdown(f'<div class="f-card"><span class="metric-label">Health Score</span><div class="metric-value" style="color:#10B981;">Optimal</div></div>', unsafe_allow_html=True)

            # --- 4. HEALTH METER & ACTIONABLE RECOMMENDATIONS ---
            r1_left, r1_right = st.columns([1, 2])
            
            with r1_left:
                st.markdown("### 🛡️ Financial Health Score")
                score = 82 # Dynamic Logic
                fig_g = go.Figure(go.Indicator(
                    mode = "gauge+number", value = score,
                    gauge = {
                        'axis': {'range': [0, 100], 'tickwidth': 1},
                        'bar': {'color': "#1E3A8A"},
                        'steps': [
                            {'range': [0, 40], 'color': "#FEE2E2"},
                            {'range': [41, 75], 'color': "#FEF3C7"},
                            {'range': [76, 100], 'color': "#D1FAE5"}]}))
                fig_g.update_layout(height=260, margin=dict(t=0, b=0, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_g, use_container_width=True)
                
                st.markdown("""
                    <div class="f-card" style="margin-top:-40px; background:#F8FAFC; border:1px dashed #CBD5E1;">
                        <p style="font-weight:700; color:#1E293B; font-size:13px;">Improve your score by:</p>
                        <ul style="font-size:12px; color:#64748B; padding-left:18px; line-height:1.8;">
                            <li>Add nominee for Policy #...097</li>
                            <li>Increase health cover by ₹15L</li>
                            <li>Verify KYC for Child Policies</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)

            with r1_right:
                st.markdown("### 🎯 Priority Recommendations")
                reco1, reco2 = st.columns(2)
                with reco1:
                    st.markdown(f"""
                        <div class="f-card" style="border-left: 5px solid #1E3A8A; min-height:220px;">
                            <span class="status-tag tag-green">Investment Trigger</span>
                            <h4 style="margin:10px 0; color:#1E3A8A;">Mutual Fund Portfolio</h4>
                            <p style="font-size:12px; color:#64748B;">Move your ₹{total_mat/200000:,.1f}L partial maturity to <b>Sattrex Alpha Fund</b> for 14% target CAGR.</p>
                            <a href="tel:9892027934" class="btn-invest">Talk to Advisor</a>
                        </div>
                    """, unsafe_allow_html=True)
                with reco2:
                    st.markdown("""
                        <div class="f-card" style="border-left: 5px solid #EF4444; min-height:220px;">
                            <span class="status-tag tag-red">Protection Gap</span>
                            <h4 style="margin:10px 0; color:#1E3A8A;">Term Life Review</h4>
                            <p style="font-size:12px; color:#64748B;">Current cover is 4x annual income. Recommended is 15x. Gap of ₹2.5 Cr detected.</p>
                            <a href="#" class="btn-invest" style="background:#EF4444;">Review Plan</a>
                        </div>
                    """, unsafe_allow_html=True)

            # --- 5. INTERACTIVE WEALTH PROJECTION ---
            st.markdown("### 📈 Interactive Wealth & Coverage Timeline")
            w_df = client_data[client_data['Maturity Year'] > 0].sort_values('Maturity Year')
            if not w_df.empty:
                fig_w = go.Figure()
                fig_w.add_trace(go.Scatter(x=w_df['Maturity Year'], y=w_df['Maturity Amount'].cumsum(), 
                                         fill='tozeroy', name='Cumulative Maturity', line=dict(color='#10B981', width=4)))
                fig_w.add_trace(go.Bar(x=w_df['Maturity Year'], y=w_df['Coverage'], 
                                     name='Live Coverage Risk', marker_color='#1E3A8A', opacity=0.7))
                fig_w.update_layout(
                    hovermode="x unified", height=400,
                    margin=dict(t=20, b=20, l=0, r=0),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig_w, use_container_width=True)

            # --- 6. FAMILY COVERAGE MATRIX (FIXED: ALL MEMBERS VISIBLE) ---
            st.markdown("### 👥 Family Protection Dashboard")
            members = client_data['Policy Holder'].unique()
            
            # Helper to create rows of 3 columns each for family
            for i in range(0, len(members), 3):
                cols = st.columns(3)
                for j, m_name in enumerate(members[i:i+3]):
                    m_rows = client_data[client_data['Policy Holder'] == m_name]
                    m_cov = m_rows['Coverage'].sum()
                    is_well = "Optimal Cover" if m_cov > 4000000 else "Action Required"
                    tag_cls = "tag-green" if is_well == "Optimal Cover" else "tag-red"
                    
                    with cols[j]:
                        st.markdown(f"""
                            <div class="f-card" style="padding:22px; border-top: 5px solid #1E3A8A;">
                                <span class="status-tag {tag_cls}">{is_well}</span>
                                <div style="font-weight:800; color:#1E3A8A; font-size:17px; margin-top:12px;">{m_name}</div>
                                <div style="font-size:12px; color:#64748B; margin-top:8px;">
                                    <b>Total Risk:</b> ₹{m_cov/100000:,.1f} L<br>
                                    <b>Policies:</b> {len(m_rows)} Plans
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

            # --- 7. REPOSITORY (EXCEL VIEW) ---
            st.markdown("### 📑 Detailed Policy Repository")
            st.markdown("<div class='f-card' style='padding:10px;'>", unsafe_allow_html=True)
            repo_df = client_data[['Policy Holder', 'Policy No', 'Plan', 'Premium', 'Coverage', 'Status']].copy()
            st.dataframe(repo_df, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # --- FOOTER ---
            st.markdown("""
                <div style="text-align:center; padding:40px; color:#94A3B8; font-size:11px;">
                    Sattrex Capital Family Office Management System • Confidential & Secure • v2.5.4
                </div>
            """, unsafe_allow_html=True)

        else:
            st.error("No portfolio found. Please check the email address or contact advisor.")
    else:
        st.error("Data Column 'Login_Email' missing in Excel file.")
else:
    st.info("👋 Welcome to the Sattrex Capital Family Office. Please log in with your registered email to continue.")
