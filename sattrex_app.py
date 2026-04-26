import streamlit as st
import pandas as pd

# 1. Professional Page Setup
st.set_page_config(page_title="Sattrex Capital | Client Portal", layout="wide")

# 2. Modern FinTech Styling
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #f0f2f6; border-radius: 5px; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #1e3d59; color: white; }
    .metric-card { background-color: #ffffff; padding: 20px; border-radius: 10px; border-top: 5px solid #1e3d59; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# 3. Load the Sample Data
# Make sure "sample test.xlsx" is in the same folder as this script
@st.cache_data
def load_data():
    df = pd.read_excel("sample test.xlsx")
    df['Risk Coverage'] = pd.to_numeric(df['Risk Coverage'], errors='coerce').fillna(0)
    df['Premium Amount'] = pd.to_numeric(df['Premium Amount'], errors='coerce').fillna(0)
    df['Maturity Amount'] = pd.to_numeric(df['Maturity Amount'], errors='coerce').fillna(0)
    return df

df = load_data()

# 4. Website Login Simulation (Email + OTP)
st.sidebar.image("logo.png", width=150) # Use your logo here
st.sidebar.title("Client Login")
email_user = st.sidebar.text_input("Registered Email ID")

if email_user:
    st.sidebar.info("Verification code sent to your email.")
    otp = st.sidebar.text_input("Enter 6-digit OTP", type="password")
    
    # We will use '123456' as the test OTP for now
    if otp == "123456":
        client_data = df[df['Login_Email'].str.contains(email_user, na=False, case=False)]
        
        if not client_data.empty:
            name = client_data['Main Account'].iloc[0]
            st.title(f"Welcome back, {name}")
            
            # --- THE TWO TABS ---
            tab1, tab2 = st.tabs(["🛡️ Wealth Protection (Insurance)", "📈 Wealth Creation (Mutual Funds)"])
            
            with tab1:
                st.subheader("Your Insurance Protection Status")
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Sum Assured", f"₹{client_data['Risk Coverage'].sum():,.0f}")
                col2.metric("Annual Savings", f"₹{client_data['Premium Amount'].sum():,.0f}")
                col3.metric("Maturity Wealth", f"₹{client_data['Maturity Amount'].sum():,.0f}")
                
                st.write("### Policy Details")
                st.dataframe(client_data[['Policy Holder', 'Policy No', 'Plan', 'Premium End Date', 'Status']], use_container_width=True, hide_index=True)
                
                # Pop-up Recommendation Logic
                if client_data['Risk Coverage'].sum() < 5000000:
                    st.warning("💡 **Sattrex Recommendation:** Your life protection is below 50 Lakhs. Based on your profile, we suggest a Term Insurance audit.")

            with tab2:
                st.subheader("Your Wealth Creation Portfolio")
                st.info("Live Mutual Fund tracking is being integrated. Soon you will see your XIRR and Portfolio growth here.")
                st.image("https://via.placeholder.com/1000x300?text=Mutual+Fund+Wealth+Growth+Chart")
        else:
            st.error("Access Denied: Email not registered.")
else:
    st.title("🏛️ Sattrex Capital Digital Notebook")
    st.write("Log in to view your complete financial protection and wealth creation journey.")