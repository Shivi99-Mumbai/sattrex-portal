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
    
    /* Premium Header */
    .premium-header {
        background-color: white; padding: 1.5rem 2rem; border-bottom: 1px solid #E2E8F0;
        display: flex; justify-content: space-between; align-items: center;
        margin: -4rem -4rem 1rem -4rem;
    }
    .advisor-card {
        background: #F1F5F9; padding: 8px 16px; border-radius: 12px;
        display: flex; align-items: center; gap: 10px;
    }

    /* Pulsating Notification */
    .pulse-container {
        background: #EFF6FF; border: 1px solid #DBEAFE; border-radius: 12px;
        padding: 12px 20px; margin-bottom: 25px; display: flex; align-items: center;
        animation: pulse-blue 3s infinite;
    }
    @keyframes pulse-blue {
        0% { box-shadow: 0 0 0 0 rgba(30, 58, 138, 0.1); }
        70% { box-shadow: 0 0 0 10px rgba(30, 58, 138, 0); }
        100% { box-shadow: 0 0 0 0 rgba(30, 58, 138, 0); }
    }

    /* Card Styling */
    .f-card {
        background: white; padding: 24px; border-radius: 16px;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.05);
        border: 1px solid #F1F5F9; margin-bottom: 20px;
    }
    .status-tag { padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 700; }
    .tag-green { background: #DCFCE7; color: #15803D; }
    .tag-red { background: #FEE2E2; color: #B91C1C; }

    /* Buttons */
    .btn-pay {
        background-color: #10B981; color: white !important; padding: 10px 20px;
        border-radius: 8px; text-decoration: none; font-weight: 700; font-size: 14px;
    }
    .btn-invest {
        background-color: #1E3A8A; color: white !important; padding: 12px 24px;
        border-radius: 8px; text-decoration: none; font-weight: 600; display: block;
        text-align: center; margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def load_data():
    try:
        # Load and clean column names immediately
        df = pd.read_excel("sample test.xlsx")
        df.columns = df.columns.str.strip()
        
        # Mapping specific names from your Excel
        df = df.rename(columns={
            'Maturity Yee': 'Maturity Year',
            'Maturity Amo': 'Maturity Amount',
            'Premium Amount': 'Premium',
            'Risk Coverage': 'Coverage'
        })
        
        # Convert types
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
    st.image("logo.png", width=150)
    st.markdown("### 🔒 Private Client Login")
    email_in = st.text_input("Registered Email").strip().lower()

if email_in:
    # Find email column dynamically
    email_col = [c for c in df.columns if c.lower() == 'login_email']
    
    if email_col:
        client_data = df[df[email_col[0]].astype(str).str.lower().str.contains(email_in, na=False)]
        
        if not client_data.empty:
            # Client specific variables
            raw_name = str(client_data['Main Account'].iloc[0]).split("-")[0].strip().title()
            total_cov = client_data['Coverage'].sum()
            total_prem = client_data['Premium'].sum()
            max_maturity = client_data['Maturity Amount'].max()
            
            # --- 1. HEADER ---
            st.markdown(f"""
                <div class="premium-header">
                    <div>
                        <h2 style='margin:0; color:#1E3A8A;'>{raw_name} Family Office</h2>
                        <p style='margin:0; color:#64748B; font-size:13px;'>Secure Portal • {datetime.now().strftime('%d %b, %Y')}</p>
                    </div>
                    <div style="display:flex; align-items:center; gap:20px;">
                        <a href="https://ebiz.licindia.in/D2CPM/#DirectPay" class="btn-pay">💳 PAY PREMIUM</a>
                        <div class="advisor-card">
                            <div style="text-align: right;">
                                <div style="font-weight:700; color:#1E293B; font-size:13px;">Vinod Gupta</div>
                                <div style="color:#64748B; font-size:11px;">Wealth Manager</div>
                            </div>
                            <div style="width:36px; height:36px; background:#1E3A8A; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:12px;">VG</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # --- 2. DYNAMIC INSIGHT NOTIFICATION (Drives Investment) ---
            insight_msg = ""
            if any(client_data['Status'] == 'LAPSED'):
                insight_msg = "⚠️ <b>CRITICAL:</b> Some policies have lapsed. Your risk cover is compromised. Fix now."
            elif max_maturity > 5000000:
                insight_msg = f"📈 <b>SATTREX STRATEGY:</b> High maturity of ₹{max_maturity/100000:,.1f}L expected. We recommend a <b>Mutual Fund STP</b> for wealth creation."
            elif total_cov < 5000000:
                insight_msg = "🛡️ <b>ADVISORY:</b> Your family is underinsured relative to income. Consider a Term Plan top-up."
            else:
                insight_msg = "✅ <b>PORTFOLIO HEALTH:</b> Your assets are well-aligned. Reviewing Mutual Fund SIPs for next quarter."

            st.markdown(f"""
                <div class="pulse-container">
                    <span style="font-size:20px; margin-right:15px;">💡</span>
                    <span style="color:#1E3A8A; font-size:14px;">{insight_msg}</span>
                </div>
            """, unsafe_allow_html=True)

            # --- 3. CORE METRICS ---
            m1, m2, m3, m4 = st.columns(4)
            m1.markdown(f'<div class="f-card"><span style="color:#64748B; font-size:11px; font-weight:700;">TOTAL COVERAGE</span><div style="color:#1E3A8A; font-size:24px; font-weight:700;">₹{total_cov/10000000:,.2f} Cr</div></div>', unsafe_allow_html=True)
            m2.markdown(f'<div class="f-card"><span style="color:#64748B; font-size:11px; font-weight:700;">ANNUAL OUTFLOW</span><div style="color:#1E3A8A; font-size:24px; font-weight:700;">₹{total_prem/100000:,.2f} L</div></div>', unsafe_allow_html=True)
            m3.markdown(f'<div class="f-card"><span style="color:#64748B; font-size:11px; font-weight:700;">POLICIES</span><div style="color:#1E3A8A; font-size:24px; font-weight:700;">{len(client_data)} Active</div></div>', unsafe_allow_html=True)
            m4.markdown(f'<div class="f-card"><span style="color:#64748B; font-size:11px; font-weight:700;">MATURITY PROJECTION</span><div style="color:#10B981; font-size:24px; font-weight:700;">₹{client_data["Maturity Amount"].sum()/100000:,.1f} L</div></div>', unsafe_allow_html=True)

            # --- 4. WEALTH & INSIGHTS (SPLIT VIEW) ---
            c_left, c_right = st.columns([1.8, 1.2])
            
            with c_left:
                st.markdown("### 📊 Wealth & Risk Projection")
                # Advanced Interactive Graph
                w_df = client_data[client_data['Maturity Year'] > 0].sort_values('Maturity Year')
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=w_df['Maturity Year'], y=w_df['Maturity Amount'], fill='tozeroy', name='Maturity Value', line=dict(color='#10B981', width=3)))
                fig.add_trace(go.Bar(x=w_df['Maturity Year'], y=w_df['Coverage'], name='Active Life Cover', marker_color='#1E3A8A', opacity=0.6))
                
                fig.update_layout(
                    hovermode="x unified",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    margin=dict(t=0, b=0, l=0, r=0),
                    height=350,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    yaxis=dict(title="Value (INR)", gridcolor="#F1F5F9")
                )
                st.plotly_chart(fig, use_container_width=True)

            with c_right:
                st.markdown("### 🎯 Recommendations")
                st.markdown(f"""
                    <div class="f-card" style="background: linear-gradient(145deg, #ffffff, #f8faff); border-left: 5px solid #1E3A8A;">
                        <h4 style="margin-top:0; color:#1E3A8A;">Mutual Fund Opportunity</h4>
                        <p style="font-size:13px; color:#475569;">Your maturing policy in {int(w_df['Maturity Year'].min()) if not w_df.empty else '2029'} can be optimized for 12-14% returns via <b>Sattrex Focused Funds</b>.</p>
                        <a href="tel:9892027934" class="btn-invest">Contact Advisor to Invest</a>
                    </div>
                """, unsafe_allow_html=True)
                
                # Small score gauge
                fig_score = go.Figure(go.Indicator(
                    mode = "gauge+number", value = 78,
                    title = {'text': "Portfolio Health", 'font': {'size': 14}},
                    gauge = {'bar': {'color': "#1E3A8A"}, 'axis': {'range': [0, 100]},
                             'steps': [{'range': [0, 50], 'color': "#FEE2E2"}, {'range': [50, 100], 'color': "#D1FAE5"}]}))
                fig_score.update_layout(height=180, margin=dict(t=30, b=0))
                st.plotly_chart(fig_score, use_container_width=True)

            # --- 5. FAMILY OVERVIEW ---
            st.markdown("### 👥 Family Coverage Matrix")
            f_cols = st.columns(3)
            members = client_data['Policy Holder'].unique()
            for i, m_name in enumerate(members[:3]): # Showing top 3 members
                m_rows = client_data[client_data['Policy Holder'] == m_name]
                m_cov = m_rows['Coverage'].sum()
                m_count = len(m_rows)
                is_well = "WELL COVERED" if m_cov > 5000000 else "UNDERINSURED"
                tag_cls = "tag-green" if is_well == "WELL COVERED" else "tag-red"
                
                with f_cols[i]:
                    st.markdown(f"""
                        <div class="f-card" style="padding:20px; border-top: 4px solid #1E3A8A;">
                            <span class="status-tag {tag_cls}">{is_well}</span>
                            <div style="font-weight:700; color:#1E3A8A; font-size:16px; margin-top:10px;">{m_name}</div>
                            <div style="font-size:13px; color:#64748B; margin-top:5px;">
                                Total Risk: ₹{m_cov/100000:,.1f} L<br>
                                Active Plans: {m_count}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            # --- 6. DETAILED REPOSITORY ---
            st.markdown("### 📑 Policy Repository")
            disp_df = client_data[['Policy Holder', 'Policy No', 'Plan', 'Premium', 'Coverage', 'Status']].copy()
            st.dataframe(disp_df, use_container_width=True, hide_index=True)
            
            st.markdown("<br><p style='text-align:center; color:#94A3B8; font-size:12px;'>Sattrex Capital Family Office Management System v2.1</p>", unsafe_allow_html=True)

        else:
            st.error("No portfolio found for this email address.")
    else:
        st.error("Data Column 'Login_Email' not detected in Excel.")
else:
    st.info("👋 Welcome. Please enter your registered email in the sidebar to securely access your portfolio.")
