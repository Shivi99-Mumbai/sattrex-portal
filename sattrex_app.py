import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="WealthGuard | Premium Portal", layout="wide")

# --- PREMIUM CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8FAFC; }
    
    /* Main Card Styling */
    .metric-card {
        background: white; padding: 20px; border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #F1F5F9;
    }
    
    /* Recommendation Cards */
    .insight-card {
        background: white; padding: 16px; border-radius: 12px;
        border-left: 4px solid #EF4444; margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    .priority-tag {
        background: #FEE2E2; color: #991B1B; padding: 2px 8px;
        border-radius: 4px; font-size: 10px; font-weight: 700;
    }

    /* Action Buttons */
    .stButton>button {
        width: 100%; border-radius: 8px; font-weight: 600;
        background-color: #1E3A8A !important; color: white !important;
    }
    
    .secondary-btn {
        background: white; border: 1px solid #E2E8F0; padding: 8px;
        border-radius: 8px; text-align: center; color: #1E3A8A; font-weight: 600;
        text-decoration: none; display: block; font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
col_logo, col_info = st.columns([2, 1])
with col_logo:
    st.title("🛡️ WealthGuard")
    st.caption("Financial Advisory Platform | Rahul Sharma")
with col_info:
    st.markdown("""
        <div style="text-align: right; background: white; padding: 10px; border-radius: 10px; border: 1px solid #E2E8F0;">
            <p style="margin:0; font-size: 12px; color: #64748B;">Your Advisor</p>
            <p style="margin:0; font-weight: 700; color: #1E3A8A;">Amit Patel</p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- HEALTH SCORE & INSIGHTS ---
c1, c2 = st.columns([1, 1.5])

with c1:
    st.subheader("Your Financial Health")
    score = 68
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': "#1E3A8A"},
            'steps': [
                {'range': [0, 40], 'color': "#FEE2E2"},
                {'range': [40, 70], 'color': "#FEF3C7"},
                {'range': [70, 100], 'color': "#D1FAE5"}
            ],
            'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': score}
        }
    ))
    fig.update_layout(height=250, margin=dict(t=0, b=0, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True)
    st.write("**You're moderately protected.** Improvements recommended to reach a 'Strong' score.")

with c2:
    st.subheader("Recommended Actions")
    
    st.markdown("""
        <div class="insight-card">
            <span class="priority-tag">HIGH PRIORITY</span>
            <p style="margin: 8px 0; font-weight: 600;">Increase Life Coverage</p>
            <p style="margin: 0; font-size: 13px; color: #64748B;">You are underinsured by ₹50L based on your current liabilities.</p>
        </div>
        <div class="insight-card" style="border-left-color: #F59E0B;">
            <span class="priority-tag" style="background:#FEF3C7; color:#92400E;">MEDIUM PRIORITY</span>
            <p style="margin: 8px 0; font-weight: 600;">Optimize Premium Outflow</p>
            <p style="margin: 0; font-size: 13px; color: #64748B;">Switching to annual payments can save you ₹18,000 yearly.</p>
        </div>
    """, unsafe_allow_html=True)
    st.button("Talk to Advisor")

# --- FAMILY COVERAGE ---
st.write("### Family Coverage Overview")
f1, f2, f3, f4 = st.columns(4)
family = [
    {"name": "Rahul Sharma", "status": "Underinsured", "color": "#EF4444", "bg": "#FEE2E2"},
    {"name": "Priya Sharma", "status": "Not Covered", "color": "#64748B", "bg": "#F1F5F9"},
    {"name": "Aarav Sharma", "status": "Well Covered", "color": "#10B981", "bg": "#D1FAE5"},
    {"name": "Meera Sharma", "status": "Well Covered", "color": "#10B981", "bg": "#D1FAE5"},
]

cols = [f1, f2, f3, f4]
for i, member in enumerate(family):
    with cols[i]:
        st.markdown(f"""
            <div class="metric-card">
                <p style="margin:0; font-size: 12px; color: #64748B;">Member</p>
                <p style="margin:0; font-weight: 700;">{member['name']}</p>
                <div style="margin-top: 10px; background: {member['bg']}; color: {member['color']}; 
                text-align: center; border-radius: 4px; font-size: 11px; font-weight: 700; padding: 4px;">
                    {member['status']}
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- STICKY ACTION BUTTONS (Sidebar/Bottom) ---
st.sidebar.markdown("### Quick Actions")
st.sidebar.button("✨ Improve My Score")
st.sidebar.button("📞 Talk to Advisor")
st.sidebar.button("➕ Add Policy")
st.sidebar.download_button("📥 Download Report", data="...", file_name="report.pdf")
