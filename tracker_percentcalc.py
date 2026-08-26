import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Utility Tools", layout="centered", page_icon="🧰")

# Custom CSS for Google-esque, minimalist playground aesthetic
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Google Sans', 'Roboto', sans-serif !important;
    }
    
    /* Playground color accent bar */
    .playground-bar {
        height: 6px;
        width: 100%;
        background: linear-gradient(90deg, #4285F4 25%, #EA4335 25%, #EA4335 50%, #FBBC05 50%, #FBBC05 75%, #34A853 75%);
        border-radius: 4px;
        margin-bottom: 1.5rem;
    }
    
    /* Soften container edges */
    .stTextInput > div > div > input, .stNumberInput > div > div > input, .stTimeInput > div > div > input {
        border-radius: 8px !important;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 24px !important;
        font-weight: 500 !important;
        padding: 0px 24px !important;
        transition: all 0.2s ease !important;
    }
    
    /* Sleek tab headers */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Google Playground Accent Bar
st.markdown('<div class="playground-bar"></div>', unsafe_allow_html=True)

st.title("Utility Tools")

# Create sleek tabs
tab1, tab2 = st.tabs(["📊 Percentage Calculator", "⏱️ Session Tracker"])

# ==========================================
# TAB 1: PERCENTAGE CALCULATOR
# ==========================================
with tab1:
    st.markdown("<br>", unsafe_allow_html=True) # visual spacing
    col_a, col_b = st.columns(2, gap="large")
    
    with col_a:
        st.write("##### 1. Known Values")
        known_pct = st.number_input("Known Percentage (%)", min_value=0.1, value=120.0, step=1.0)
        known_val = st.number_input("Known Value", value=78.0, step=1.0)
    
    with col_b:
        st.write("##### 2. Table Settings")
        start_pct = st.number_input("Start Percentage (%)", value=30.0, step=1.0)
        end_pct = st.number_input("End Percentage (%)", value=120.0, step=1.0)
        step_pct = st.number_input("Step Percentage (%)", min_value=0.1, value=5.0, step=1.0)
    
    st.divider()
    
    if known_pct > 0:
        base_value = known_val / (known_pct / 100)
        step_value = base_value * (step_pct / 100)
        
        st.success(f"**Base Value (100%):** {base_value:g} &nbsp;&nbsp;|&nbsp;&nbsp; **{step_pct:g}% increment:** {step_value:g}", icon="💡")
        
        data = []
        current_pct = start_pct
        
        if step_pct > 0 and (end_pct - start_pct) / step_pct <= 1000:
            while current_pct <= end_pct:
                val = base_value * (current_pct / 100)
                data.append({
                    "Percentage": f"{current_pct:g}%",
                    "Value": round(val, 4)
                })
                current_pct += step_pct
                
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.error("Invalid range or step size.")
    else:
        st.error("Known percentage must be greater than 0.")

# ==========================================
# TAB 2: SESSION TRACKER
# ==========================================
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Store initial time in session state so it doesn't constantly jump to 'now' when tweaking inputs
    if "start_time" not in st.session_state:
        st.session_state.start_time = datetime.now().time()
        
    mode = st.radio(
        "Configuration Mode", 
        ["MAGNETS", "MANIFEST", "Custom"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Start time is always editable, regardless of preset
    col_time, col_info = st.columns([1, 2])
    with col_time:
        start_time_val = st.time_input("First Session Start Time", value=st.session_state.start_time)
        st.session_state.start_time = start_time_val # Save changes
    
    # Setup variables based on mode
    with col_info:
        if mode == "MAGNETS":
            sessions, stim_dur, interval = 10, 10, 50
            st.info("**MAGNETS Preset:** 10 Sessions • 10m Stim • 50m Interval", icon="🧲")
        elif mode == "MANIFEST":
            sessions, stim_dur, interval = 5, 10, 40
            st.info("**MANIFEST Preset:** 5 Sessions • 10m Stim • 40m Interval", icon="✨")
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                sessions = st.number_input("Sessions", min_value=1, value=5, step=1)
            with col2:
                stim_dur = st.number_input("Stim (mins)", min_value=1, value=10, step=1)
            with col3:
                interval = st.number_input("Rest (mins)", min_value=1, value=40, step=1)
            
    start_dt = datetime.combine(datetime.today(), start_time_val)
    
    st.divider()
    
    # Generate Schedule Button
    if st.button("Generate Schedule", type="primary"):
        tracker_data = []
        current_time = start_dt
        
        for i in range(1, sessions + 1):
            bring_back = current_time - timedelta(minutes=5)
            finish = current_time + timedelta(minutes=stim_dur) 
            
            tracker_data.append({
                "Session": f"Session {i}",
                "Bring Back (-5m)": bring_back.strftime("%I:%M %p"),
                "Start Time": current_time.strftime("%I:%M %p"),
                "Finish Time": finish.strftime("%I:%M %p")
            })
            
            current_time += timedelta(minutes=interval)
            
        tracker_df = pd.DataFrame(tracker_data)
        st.dataframe(tracker_df, use_container_width=True, hide_index=True)
