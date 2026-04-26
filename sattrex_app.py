import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# --- CORE CONFIG ---
st.set_page_config(page_title="Sattrex Capital | Family Office", layout="wide", initial_sidebar_state="collapsed")

# --- HIGH-END UI STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root Styles */
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif; 
        background-color: #F8FAFC; 
    }
    
    .main { background-color: #F8FAFC; }

    /* Custom Header */
    .premium-header {
        background-color: white;
        padding: 1rem 2rem;
        border-bottom: 1px solid #E2E8F0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: -4rem -4rem 2rem -4rem;
    }
    
    .advisor-card {
        background: #F1F5F9;
        padding: 8px 16px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Professional Cards */
    .f-card {
        background: white; padding: 24px; border-radius: 16px;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.05);
        border: 1px solid #F1F5F9; margin-bottom: 20px;
    }

    /* Actionable Insight Cards */
    .insight-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        border-left: 6px solid #1E3A8A;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    
    .fix-btn {
        background-color: #1E3A8A;
        color: white !important;
        padding: 8px 16px;
        border-radius: 8px;
        text-decoration: none;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        margin-top: 10px;
    }

    /* Family Tags */
    .status-tag-well { background: #DCFCE7; color: #15803D; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 600; }
    .status-tag-under { background: #FEE2E2; color: #B91C1C; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 600; }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #F8FAFC; }
    ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- DATA PROCESSING ---
@st.cache_data
def load_and_process():
    # Simulated load for the demo - replace with: df = pd.read_excel("sample test.xlsx")
    # Generating dummy data structure to match your requirements
    data = {
        'Login_Email': ['test@sattrex.com'],
        'Main Account': ['Aditya Sharma'],
        'Policy Holder': ['Aditya Sharma', 'Priya Sharma', 'Junior Sharma', 'Aditya Sharma'],
        'Risk Coverage': [50000000, 20000000, 5000000, 10000000],
        'Premium Amount': [120000, 85000, 15000, 45000],
        'Maturity Amount': [15000000, 0, 2500000, 5000000],
        'Maturity Year': [2032, 2040, 2045, 2026],
        'Policy No': ['LIC123', 'HDFC99', 'MAX77', 'LIC44'],
        'Plan': ['Jeevan Anand', 'Term Life', 'Child Plan', 'Money Back'],
        'Status': ['Active', 'Active', 'Active', 'Lapsing Soon']
    }
    return pd.DataFrame(data)

df = load_and_process()

# --- AUTHENTICATION ---
with st.sidebar:
    st.markdown("### 🔐 Client Portal")
    email = st.text_input("Registered Email ID", value="test@sattrex.com")
    otp = st.text_input("Access PIN", type="password", value="123456")

if email and otp == "123456":
    client_data = df[df['Login_Email'].str.contains(email, na=False, case=False)]
    
    if not client_data.empty:
        name = client_data['Main Account'].iloc[0]

        # --- PREMIUM HEADER ---
        st.markdown(f"""
            <div class="premium-header">
                <div>
                    <h2 style='margin:0; color:#1E3A8A;'>Sattrex Family Office</h2>
                    <p style='margin:0; color:#64748B; font-size:14px;'>Last Updated: {datetime.now().strftime('%d %b, %H:%M')}</p>
                </div>
                <div class="advisor-card">
                    <div style="text-align: right;">
                        <div style="font-weight:700; color:#1E293B; font-size:14px;">Vinod Gupta</div>
                        <div style="color:#64748B; font-size:12px;">Wealth Advisor</div>
                    </div>
                    <div style="width:40px; height:40px; background:#1E3A8A; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold;">VG</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # --- NAVIGATION TABS ---
        tab_prot, tab_wealth, tab_ins = st.tabs(["🛡️ Protection", "📈 Wealth", "💡 Insights"])

        with tab_prot:
            # Metrics Row
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.markdown(f'<div class="f-card"><span style="color:#64748B; font-size:12px; font-weight:600;">TOTAL COVERAGE</span><div style="color:#1E3A8A; font-size:24px; font-weight:700;">₹{client_data["Risk Coverage"].sum()/10000000:,.2f} Cr</div></div>', unsafe_allow_html=True)
            with k2:
                st.markdown(f'<div class="f-card"><span style="color:#64748B; font-size:12px; font-weight:600;">ANNUAL PREMIUM</span><div style="color:#1E3A8A; font-size:24px; font-weight:700;">₹{client_data["Premium Amount"].sum()/100000:,.2f} L</div></div>', unsafe_allow_html=True)
            with k3:
                st.markdown(f'<div class="f-card"><span style="color:#64748B; font-size:12px; font-weight:600;">POLICIES</span><div style="color:#1E3A8A; font-size:24px; font-weight:700;">{len(client_data)} Active</div></div>', unsafe_allow_html=True)
            with k4:
                st.markdown('<div class="f-card"><span style="color:#64748B; font-size:12px; font-weight:600;">NOMINEES</span><div style="color:#1E3A8A; font-size:24px; font-weight:700;">Verified</div></div>', unsafe_allow_html=True)

            col_score, col_family = st.columns([1, 2])

            with col_score:
                st.markdown("### Financial Health")
                score = 72 # Dynamic logic can be added
                
                # SLEEK SEMI-CIRCLE GAUGE
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = score,
                    number = {'font': {'size': 40, 'color': "#1E3A8A"}},
                    gauge = {
                        'axis': {'range': [0, 100], 'tickwidth': 1},
                        'bar': {'color': "#1E3A8A"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "#F1F5F9",
                        'steps': [
                            {'range': [0, 40], 'color': '#FEE2E2'},
                            {'range': [41, 70], 'color': '#FEF3C7'},
                            {'range': [71, 100], 'color': '#D1FAE5'}
                        ],
                    }
                ))
                fig.update_layout(height=250, margin=dict(t=0, b=0, l=20, r=20))
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown(f"""
                    <div class="f-card" style="margin-top:-30px;">
                        <p style="font-weight:600; font-size:14px; color:#1E293B;">Improve your score by:</p>
                        <ul style="font-size:13px; color:#475569; padding-left:20px;">
                            <li>Increasing life cover for Priya by ₹50L</li>
                            <li>Adding a critical illness rider</li>
                            <li>Consolidating overlapping policies</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)

            with col_family:
                st.markdown("### Family Coverage Status")
                # Horizontal Family Cards
                m_cols = st.columns(3)
                members = client_data['Policy Holder'].unique()
                for i, member in enumerate(members[:3]):
                    total_risk = client_data[client_data['Policy Holder'] == member]['Risk Coverage'].sum()
                    status = "Well Covered" if total_risk > 10000000 else "Underinsured"
                    tag_class = "status-tag-well" if status == "Well Covered" else "status-tag-under"
                    
                    with m_cols[i]:
                        st.markdown(f"""
                            <div class="f-card" style="padding:15px; border-left: 4px solid #10B981;">
                                <div style="font-weight:700; color:#1E3A8A; margin-bottom:5px;">{member}</div>
                                <div style="font-size:12px; color:#64748B; margin-bottom:10px;">Risk: ₹{total_risk/100000:,.1f} L</div>
                                <span class="{tag_class}">{status}</span>
                            </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("### Actionable Recommendations")
                r1, r2 = st.columns(2)
                with r1:
                    st.markdown("""
                        <div class="insight-card" style="border-color: #EF4444;">
                            <div style="font-weight:700; color:#B91C1C;">Policy Lapsing</div>
                            <div style="font-size:13px; color:#475569;">Policy #LIC44 is in grace period. Pay now to avoid loss of cover.</div>
                            <a href="#" class="fix-btn">Fix Now</a>
                        </div>
                    """, unsafe_allow_html=True)
                with r2:
                    st.markdown("""
                        <div class="insight-card" style="border-color: #F59E0B;">
                            <div style="font-weight:700; color:#92400E;">Increase Life Cover</div>
                            <div style="font-size:13px; color:#475569;">Your current income justifies an additional ₹1Cr coverage.</div>
                            <a href="#" class="fix-btn" style="background:#F59E0B;">Talk to Advisor</a>
                        </div>
                    """, unsafe_allow_html=True)

        with tab_wealth:
            st.markdown("### Portfolio Growth")
            growth_df = pd.DataFrame({'Year': [2022, 2023, 2024, 2025, 2026], 'Wealth': [10, 25, 45, 68, 82.5]})
            fig_growth = px.area(growth_df, x='Year', y='Wealth', color_discrete_sequence=['#1E3A8A'])
            fig_growth.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#E2E8F0'),
                margin=dict(t=20, b=20)
            )
            st.plotly_chart(fig_growth, use_container_width=True)

        with tab_ins:
            st.markdown("### Detailed Policy Analysis")
            st.dataframe(
                client_data[['Policy Holder', 'Policy No', 'Plan', 'Premium Amount', 'Risk Coverage', 'Status']],
                use_container_width=True,
                hide_index=True
            )

    else:
        st.error("Credential Error: Data not found.")
else:
    st.info("Welcome to the Sattrex Family Office. Please enter your credentials to begin.")
