import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sattrex Capital | Client Portal", layout="wide")

# --- CUSTOM CSS FOR THE "TOP-CLASS" LOOK ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 5px solid #1e3d59; }
    div.stButton > button { width: 100%; border-radius: 5px; height: 3em; background-color: #1e3d59; color: white; border: none; font-weight: bold; }
    div.stButton > button:hover { background-color: #2b567a; color: white; border: none; }
    .advisor-card { background-color: #ffffff; padding: 20px; border-radius: 15px; border: 1px solid #e0e0e0; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def load_data():
    df = pd.read_excel("sample test.xlsx")
    for col in ['Risk Coverage', 'Premium Amount', 'Maturity Amount']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

df = load_data()

# --- SIDEBAR & LOGIN ---
st.sidebar.image("logo.png", width=200)
st.sidebar.markdown("---")
st.sidebar.subheader("🔒 Secure Access")
email = st.sidebar.text_input("Client Email ID")
otp = st.sidebar.text_input("Enter OTP (Use 123456)", type="password")

if email and otp == "123456":
    client_data = df[df['Login_Email'].str.contains(email, na=False, case=False)]
    
    if not client_data.empty:
        client_name = client_data['Main Account'].iloc[0]
        
        # --- HEADER SECTION ---
        col_logo, col_info = st.columns([1, 4])
        with col_info:
            st.title(f"Hello, {client_name}")
            st.write("Welcome to your private Sattrex Digital Notebook.")

        # --- ADVISOR SECTION ---
        with st.container():
            st.markdown(f"""
            <div class="advisor-card">
                <p style="margin:0; color: gray; font-size: 0.9em;">Your Personal Wealth Advisor</p>
                <h3 style="margin:0; color: #1e3d59;">Vinod Gupta</h3>
                <p style="margin:0; font-weight: bold;">Sattrex Capital</p>
            </div>
            """, unsafe_allow_html=True)

        # --- DASHBOARD TABS ---
        tab1, tab2 = st.tabs(["🛡️ Wealth Protection", "📈 Wealth Creation"])

        with tab1:
            # 1. METRIC ROW
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Life Value", f"₹{client_data['Risk Coverage'].sum():,.0f}")
            m2.metric("Annual Savings", f"₹{client_data['Premium Amount'].sum():,.0f}")
            m3.metric("Expected Maturity", f"₹{client_data['Maturity Amount'].sum():,.0f}")

            st.write("---")

            # 2. GAUGE AND ACTIONS
            col_gauge, col_actions = st.columns([2, 1])
            
            with col_gauge:
                # Calculate Score
                score = min(int((client_data['Risk Coverage'].sum() / 5000000) * 100), 100)
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = score,
                    title = {'text': "Insured Score"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#1e3d59"},
                        'steps': [
                            {'range': [0, 40], 'color': "#ff4b4b"},
                            {'range': [40, 70], 'color': "#ffa500"},
                            {'range': [70, 100], 'color': "#00cc66"}]}))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

            with col_actions:
                st.write("### Quick Actions")
                # Direct Call Buttons using HTML for 9892027934
                st.markdown(f'<a href="tel:9892027934"><button style="width:100%; border-radius: 5px; height: 3em; background-color: #1e3d59; color: white; border: none; font-weight: bold; margin-bottom:10px;">📞 Talk to Advisor</button></a>', unsafe_allow_html=True)
                st.markdown(f'<a href="tel:9892027934"><button style="width:100%; border-radius: 5px; height: 3em; background-color: #1e3d59; color: white; border: none; font-weight: bold; margin-bottom:10px;">📈 Improve My Score</button></a>', unsafe_allow_html=True)
                st.markdown(f'<a href="tel:9892027934"><button style="width:100%; border-radius: 5px; height: 3em; background-color: #f0f2f6; color: #1e3d59; border: 1px solid #1e3d59; font-weight: bold; margin-bottom:10px;">➕ Add Policy</button></a>', unsafe_allow_html=True)
                
                # Download Report Button
                csv = client_data.to_csv(index=False).encode('utf-8')
                st.download_button(label="📄 Download Full Report", data=csv, file_name=f"{client_name}_Portfolio.csv", mime="text/csv")

            # 3. POLICY TABLE
            st.write("### 📋 Active Policy Inventory")
            st.dataframe(client_data[['Policy Holder', 'Policy No', 'Plan', 'Premium Amount', 'Status']], use_container_width=True, hide_index=True)

        with tab2:
            st.subheader("Wealth Creation Hub")
            st.info("Live Mutual Fund sync is coming soon. Here you will see your Portfolio Growth & XIRR.")
            # Pie Chart for Asset Allocation
            alloc_fig = px.pie(names=['Insurance/Debt', 'Mutual Funds', 'Cash'], values=[70, 20, 10], hole=0.6, color_discrete_sequence=['#1e3d59', '#3a7ca5', '#d1d8e0'])
            st.plotly_chart(alloc_fig)

    else:
        st.error("No record found. Please ensure your email is correct in the Sattrex database.")
else:
    st.write("## Welcome to Sattrex Capital")
    st.image("https://via.placeholder.com/1000x400?text=Sattrex+Capital+Client+Experience", use_column_width=True)
