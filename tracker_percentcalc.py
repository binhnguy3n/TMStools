import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# ==========================================
# PAGE CONFIGURATION & SESSION STATE
# ==========================================
st.set_page_config(page_title="Utility Tools", layout="centered", page_icon="🧰")

# Initialize session state variables to remember inputs and generated schedules
if "schedule_generated" not in st.session_state:
    st.session_state.schedule_generated = False

now = datetime.now()
if "hour" not in st.session_state:
    st.session_state.hour = int(now.strftime("%I"))
if "minute" not in st.session_state:
    st.session_state.minute = f"{(now.minute // 5 * 5):02d}" # Rounds to nearest 5 mins
if "ampm" not in st.session_state:
    st.session_state.ampm = now.strftime("%p")
if "mode" not in st.session_state:
    st.session_state.mode = "MAGNETS"

# ==========================================
# PLAYGROUND THEME CSS
# ==========================================
st.markdown("""
<style>
    /* Playful rounded font */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { 
        font-family: 'Nunito', sans-serif !important; 
    }
    
    /* Chunky, rounded inputs */
    .stTextInput > div > div > input, 
    .stNumberInput > div > div > input, 
    div[data-baseweb="select"] > div {
        border-radius: 16px !important;
        border: 2px solid #FFE66D !important;
        background-color: #FAFAFA !important;
        font-weight: 600 !important;
    }
    
    /* Playful 'Bouncy' Button */
    .stButton > button {
        background-color: #FF6B6B !important;
        color: white !important;
        border-radius: 30px !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        border: none !important;
        padding: 8px 28px !important;
        box-shadow: 0 5px 0px #E63946 !important;
        transition: all 0.1s ease !important;
        margin-top: 10px;
    }
    .stButton > button:active {
        transform: translateY(5px) !important;
        box-shadow: 0 0px 0px #E63946 !important;
    }
    .stButton > button:hover {
        background-color: #FF8787 !important;
    }

    /* Dashed alert boxes for presets */
    div[data-testid="stAlert"] {
        border-radius: 16px !important;
        background-color: #F0F9FF !important;
        border: 2px dashed #4ECDC4 !important;
        color: #2D3748 !important;
        border-left: 2px dashed #4ECDC4 !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 16px 16px 0 0 !important;
        font-weight: 800 !important;
        padding: 10px 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# LIVE DATE/TIME BANNER (Playground Style)
# ==========================================
components.html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@600;800&display=swap');
    body { margin: 0; font-family: 'Nunito', sans-serif; background-color: transparent; }
    .banner {
        background-color: #FAFAFA; border-radius: 16px; padding: 12px 20px;
        display: flex; justify-content: space-between; align-items: center;
        border: 2px dashed #4ECDC4; color: #2D3748;
    }
    .date { font-size: 16px; font-weight: 600; color: #6B7280; }
    .time { font-size: 20px; font-weight: 800; color: #FF6B6B; }
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
""", height=70)

st.title("🧰 Utility Tools")
tab1, tab2 = st.tabs(["📊 Percentage Calculator", "⏱️ Session Tracker"])

# Helper function for strictly 12-hour formatted output in the table
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
        st.info(f"**Base Value (100%):** {base_value:g} &nbsp;&nbsp;|&nbsp;&nbsp; **{step_pct:g}% increment:** {step_value:g}", icon="💡")
        
        data = []
        current_pct = start_pct
        if step_pct > 0 and (end_pct - start_pct) / step_pct <= 1000:
            while current_pct <= end_pct:
                data.append({"Percentage": f"{current_pct:g}%", "Value": round(base_value * (current_pct / 100), 4)})
                current_pct += step_pct
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

# ==========================================
# TAB 2: SESSION TRACKER
# ==========================================
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 1. Mode Selection (Automatically remembered via 'key')
    mode = st.radio("Configuration Mode", ["MAGNETS", "MANIFEST", "Custom"], horizontal=True, key="mode", label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_time, col_info = st.columns([1.2, 2])
    
    # 2. Custom 12-Hour Dropdown Picker (Bypasses browser military time)
    with col_time:
        st.write("##### First Session Time")
        t1, t2, t3 = st.columns(3)
        with t1:
            hour_val = st.selectbox("Hr", options=list(range(1, 13)), key="hour", label_visibility="collapsed")
        with t2:
            min_val = st.selectbox("Min", options=[f"{m:02d}" for m in range(60)], key="minute", label_visibility="collapsed")
        with t3:
            ampm_val = st.selectbox("AM/PM", options=["AM", "PM"], key="ampm", label_visibility="collapsed")
            
        # Convert the dropdowns into a datetime object for today
        time_str = f"{hour_val}:{min_val} {ampm_val}"
        start_time_obj = datetime.strptime(time_str, "%I:%M %p").time()
        start_dt = datetime.combine(datetime.today(), start_time_obj)
    
    # 3. Setup variables based on mode
    with col_info:
        if mode == "MAGNETS":
            sessions, stim_dur, interval = 10, 10, 50
            st.info("**MAGNETS Preset:** 10 Sessions • 10m Stim • 50m Interval", icon="🧲")
        elif mode == "MANIFEST":
            sessions, stim_dur, interval = 5, 10, 40
            st.info("**MANIFEST Preset:** 5 Sessions • 10m Stim • 40m Interval", icon="✨")
        else:
            c1, c2, c3 = st.columns(3)
            with c1: sessions = st.number_input("Sessions", min_value=1, value=5, step=1, key="c_sess")
            with c2: stim_dur = st.number_input("Stim (mins)", min_value=1, value=10, step=1, key="c_stim")
            with c3: interval = st.number_input("Rest (mins)", min_value=1, value=40, step=1, key="c_rest")
    
    st.divider()
    
    # Generate Button updates the session state
    if st.button("Generate Schedule"):
        st.session_state.schedule_generated = True
        
    # 4. Display the schedule if it has been generated
    if st.session_state.schedule_generated:
        tracker_data = []
        current_time = start_dt
        current_real_time = datetime.now()
        active_idx = -1
        
        for i in range(1, sessions + 1):
            bring_back = current_time - timedelta(minutes=5)
            finish = current_time + timedelta(minutes=stim_dur) 
            
            # Highlight logic logic 
            if i == sessions:
                block_end = finish
            else:
                block_end = current_time + timedelta(minutes=interval) - timedelta(minutes=5)
                
            if bring_back <= current_real_time < block_end:
                active_idx = i - 1 
            
            tracker_data.append({
                "Session": f"Session {i}",
                "Bring Back (-5m)": format_12h(bring_back),
                "Start Time": format_12h(current_time),
                "Finish Time": format_12h(finish)
            })
            current_time += timedelta(minutes=interval)
            
        # Styling function for the playful theme
        def highlight_active(x):
            df_style = pd.DataFrame('', index=x.index, columns=x.columns)
            if active_idx != -1 and active_idx in x.index:
                # Applies a soft mint background to the active row
                df_style.iloc[active_idx] = 'background-color: #E6FFFA; color: #00A389; font-weight: 800;'
            return df_style

        styled_df = pd.DataFrame(tracker_data).style.apply(highlight_active, axis=None)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
