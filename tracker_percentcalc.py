import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Utility Tools", layout="centered", page_icon="🧰")

# Custom CSS for Google-esque, minimalist playground aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Google Sans', 'Roboto', sans-serif !important; }
    
    .playground-bar {
        height: 6px; width: 100%;
        background: linear-gradient(90deg, #4285F4 25%, #EA4335 25%, #EA4335 50%, #FBBC05 50%, #FBBC05 75%, #34A853 75%);
        border-radius: 4px; margin-bottom: 1rem;
    }
    
    .stTextInput > div > div > input, .stNumberInput > div > div > input, .stTimeInput > div > div > input {
        border-radius: 8px !important;
    }
    
    .stButton > button {
        border-radius: 24px !important; font-weight: 500 !important;
        padding: 0px 24px !important; transition: all 0.2s ease !important;
    }
    
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; white-space: pre-wrap; background-color: transparent;
        border-radius: 4px 4px 0px 0px; padding: 10px 16px; font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Google Playground Accent Bar
st.markdown('<div class="playground-bar"></div>', unsafe_allow_html=True)

# ==========================================
# LIVE DATE/TIME BANNER (12-Hour Format)
# ==========================================
components.html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
    body { margin: 0; font-family: 'Google Sans', sans-serif; background-color: transparent; }
    .banner {
        background-color: #F8F9FA; border-radius: 8px; padding: 16px 24px;
        display: flex; justify-content: space-between; align-items: center;
        border: 1px solid #E8EAED; color: #202124; box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .date { font-size: 16px; font-weight: 500; color: #5F6368; }
    .time { font-size: 22px; font-weight: 700; color: #4285F4; }
</style>
<div class="banner">
    <div class="date" id="date"></div>
    <div class="time" id="time"></div>
</div>
<script>
    function updateClock() {
        const now = new Date();
        document.getElementById('date').innerText = now.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
        document.getElementById('time').innerText = now.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', second: '2-digit', hour12: true });
    }
    setInterval(updateClock, 1000); updateClock();
</script>
""", height=75)


st.title("Utility Tools")
tab1, tab2 = st.tabs(["📊 Percentage Calculator", "⏱️ Session Tracker"])

# Helper function to ensure strict 12-hour format without leading zeros (e.g., 9:05 AM instead of 09:05 AM)
def format_12h(dt):
    return dt.strftime("%I:%M %p").lstrip("0")

# ==========================================
# TAB 1: PERCENTAGE CALCULATOR
# ==========================================
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
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
                data.append({"Percentage": f"{current_pct:g}%", "Value": round(base_value * (current_pct / 100), 4)})
                current_pct += step_pct
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
        else:
            st.error("Invalid range or step size.")

# ==========================================
# TAB 2: SESSION TRACKER
# ==========================================
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    if "start_time" not in st.session_state:
        st.session_state.start_time = datetime.now().time()
        
    mode = st.radio("Configuration Mode", ["MAGNETS", "MANIFEST", "Custom"], horizontal=True, label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_time, col_info = st.columns([1, 2])
    with col_time:
        # Note: st.time_input respects the browser OS settings for 12/24 display natively on the widget, 
        # but our generated schedule will definitively force a 12-hour output.
        start_time_val = st.time_input("First Session Start Time", value=st.session_state.start_time)
        st.session_state.start_time = start_time_val 
    
    with col_info:
        if mode == "MAGNETS":
            sessions, stim_dur, interval = 10, 10, 50
            st.info("**MAGNETS Preset:** 10 Sessions • 10m Stim • 50m Interval", icon="🧲")
        elif mode == "MANIFEST":
            sessions, stim_dur, interval = 5, 10, 40
            st.info("**MANIFEST Preset:** 5 Sessions • 10m Stim • 40m Interval", icon="✨")
        else:
            col1, col2, col3 = st.columns(3)
            with col1: sessions = st.number_input("Sessions", min_value=1, value=5, step=1)
            with col2: stim_dur = st.number_input("Stim (mins)", min_value=1, value=10, step=1)
            with col3: interval = st.number_input("Rest (mins)", min_value=1, value=40, step=1)
            
    start_dt = datetime.combine(datetime.today(), start_time_val)
    
    st.divider()
    
    if st.button("Generate Schedule", type="primary"):
        tracker_data = []
        current_time = start_dt
        now = datetime.now()
        active_idx = -1
        
        for i in range(1, sessions + 1):
            bring_back = current_time - timedelta(minutes=5)
            finish = current_time + timedelta(minutes=stim_dur) 
            
            # Logic to determine which session block we are currently inside
            if i == sessions:
                block_end = finish
            else:
                block_end = current_time + timedelta(minutes=interval) - timedelta(minutes=5)
                
            if bring_back <= now < block_end:
                active_idx = i - 1 # Zero-indexed for Pandas
            
            tracker_data.append({
                "Session": f"Session {i}",
                "Bring Back (-5m)": format_12h(bring_back),
                "Start Time": format_12h(current_time),
                "Finish Time": format_12h(finish)
            })
            
            current_time += timedelta(minutes=interval)
            
        tracker_df = pd.DataFrame(tracker_data)
        
        # Function to apply background color to the currently active session
        def highlight_active(x):
            df_style = pd.DataFrame('', index=x.index, columns=x.columns)
            if active_idx != -1 and active_idx in x.index:
                # Applies a Google-blue background and bold text to the active row
                df_style.iloc[active_idx] = 'background-color: #E8F0FE; color: #1967D2; font-weight: bold;'
            return df_style

        # Apply styling and display
        styled_df = tracker_df.style.apply(highlight_active, axis=None)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        if active_idx != -1:
            st.caption("🔄 *The currently active session is highlighted in blue. Click 'Generate' again to refresh the highlighting as time passes.*")
