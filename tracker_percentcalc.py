import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import streamlit.components.v1 as components

# ==========================================
# PAGE CONFIGURATION & SESSION STATE
# ==========================================
st.set_page_config(page_title="TMS Tools", layout="centered", page_icon="🧰")

# Initialize timezone offset first (Defaults to -6 for MDT)
if "tz_offset" not in st.session_state:
    st.session_state.tz_offset = -6

# Helper callback to set time dropdowns to current LOCAL time
def set_time_to_now():
    utc_now = datetime.now(timezone.utc).replace(tzinfo=None)
    local_now = utc_now + timedelta(hours=st.session_state.tz_offset)
    st.session_state.hour = int(local_now.strftime("%I"))
    st.session_state.minute = f"{local_now.minute:02d}"
    st.session_state.ampm = local_now.strftime("%p")

# Initialize session state variables 
if "schedule_generated" not in st.session_state:
    st.session_state.schedule_generated = False

if "hour" not in st.session_state:
    utc_now = datetime.now(timezone.utc).replace(tzinfo=None)
    local_now = utc_now + timedelta(hours=st.session_state.tz_offset)
    st.session_state.hour = int(local_now.strftime("%I"))
    st.session_state.minute = f"{(local_now.minute // 5 * 5):02d}"
    st.session_state.ampm = local_now.strftime("%p")
    
if "mode" not in st.session_state:
    st.session_state.mode = "MAGNETS"

# ==========================================
# PLAYGROUND THEME CSS
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Nunito', sans-serif !important; }
    
    .stTextInput > div > div > input, .stNumberInput > div > div > input, div[data-baseweb="select"] > div {
        border-radius: 16px !important; border: 2px solid #FFE66D !important;
        background-color: #FAFAFA !important; font-weight: 600 !important;
    }
    
    /* Primary buttons (Generate, Now) */
    button[kind="primary"] {
        background-color: #FF6B6B !important; color: white !important;
        border-radius: 30px !important; font-weight: 800 !important; font-size: 16px !important;
        border: none !important; padding: 4px 20px !important; height: 42px !important; margin: 0 !important;
        box-shadow: 0 5px 0px #E63946 !important; transition: all 0.1s ease !important;
    }
    button[kind="primary"]:active { transform: translateY(5px) !important; box-shadow: 0 0px 0px #E63946 !important; }
    button[kind="primary"]:hover { background-color: #FF8787 !important; }

    /* Secondary buttons (Refresh) made into cute circles */
    button[kind="secondary"] {
        background-color: transparent !important; color: #00A389 !important;
        border: 2px solid #00A389 !important; border-radius: 50% !important;
        width: 42px !important; height: 42px !important;
        padding: 0 !important; font-size: 20px !important;
        box-shadow: 0 3px 0px #007A66 !important; transition: all 0.1s ease !important;
        display: flex !important; align-items: center !important; justify-content: center !important; margin: 0 !important;
    }
    button[kind="secondary"]:active { transform: translateY(3px) !important; box-shadow: 0 0px 0px #007A66 !important; }
    button[kind="secondary"]:hover { background-color: #E6FFFA !important; }

    /* Camera HTML button styled exactly like secondary button */
    .camera-btn {
        background-color: transparent; color: #00A389; border: 2px solid #00A389; border-radius: 50%;
        width: 42px; height: 42px; padding: 0; font-size: 20px; box-shadow: 0 3px 0px #007A66; 
        transition: all 0.1s ease; display: flex; align-items: center; justify-content: center;
        text-decoration: none; margin: 0;
    }
    .camera-btn:active { transform: translateY(3px); box-shadow: 0 0px 0px #007A66; }
    .camera-btn:hover { background-color: #E6FFFA; }

    div[data-testid="stAlert"] {
        border-radius: 16px !important; background-color: #F0F9FF !important;
        border: 2px dashed #4ECDC4 !important; color: #2D3748 !important; border-left: 2px dashed #4ECDC4 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { border-radius: 16px 16px 0 0 !important; font-weight: 800 !important; padding: 10px 20px !important; }
    
    /* Force white background for the table so the downloaded image looks clean */
    [data-testid="stTable"] { background-color: white !important; padding: 10px; border-radius: 12px; }
    [data-testid="stTable"] table { width: 100% !important; border-collapse: collapse !important; }
    [data-testid="stTable"] th { background-color: #FAFAFA !important; border-bottom: 2px dashed #4ECDC4 !important; font-weight: 800 !important; }
    [data-testid="stTable"] td, [data-testid="stTable"] th { padding: 12px 10px !important; }
    [data-testid="stTable"] tr { border-bottom: 1px solid #F3F4F6 !important; }

    /* Container injection styling to unify the banner */
    div[data-testid="stHorizontalBlock"]:has(.banner-text-target) {
        background-color: #E6FFFA; border: 2px dashed #00A389; border-radius: 12px;
        padding: 8px 16px; align-items: center; margin-bottom: 15px; margin-top: -10px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# LIVE DATE/TIME BANNER
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

status_banner = st.empty()

st.title("🧰 TMS Tools")

tab1, tab2 = st.tabs(["⏱️ Session Tracker", "📊 Percentage Calculator"])

def format_12h(dt):
    return dt.strftime("%I:%M %p").lstrip("0")

# ==========================================
# TAB 1: SESSION TRACKER
# ==========================================
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    mode = st.radio("Configuration Mode", ["MAGNETS", "MANIFEST", "Custom"], horizontal=True, key="mode", label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_time, col_info = st.columns([1.2, 2])
    
    with col_time:
        st.write("##### First Session Time")
        
        col_btn, col_tz = st.columns([0.8, 1.2], gap="small")
        with col_btn:
            st.button("🕒 Now", on_click=set_time_to_now, type="primary")
        with col_tz:
            st.selectbox(
                "Local TZ Offset", 
                options=[i for i in range(-12, 13)], 
                index=6, 
                format_func=lambda x: f"UTC{'+' if x >= 0 else ''}{x}", 
                key="tz_offset",
                label_visibility="collapsed"
            )
        
        t1, t2, t3 = st.columns(3)
        with t1:
            hour_val = st.selectbox("Hr", options=list(range(1, 13)), key="hour", label_visibility="collapsed")
        with t2:
            min_val = st.selectbox("Min", options=[f"{m:02d}" for m in range(60)], key="minute", label_visibility="collapsed")
        with t3:
            ampm_val = st.selectbox("AM/PM", options=["AM", "PM"], key="ampm", label_visibility="collapsed")
            
        time_str = f"{hour_val}:{min_val} {ampm_val}"
        start_time_obj = datetime.strptime(time_str, "%I:%M %p").time()
        start_dt = datetime.combine(datetime.today(), start_time_obj)
    
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
    
    if st.button("Generate Schedule", type="primary"):
        st.session_state.schedule_generated = True
        
    if st.session_state.schedule_generated:
        tracker_data = []
        current_time = start_dt
        
        utc_now = datetime.now(timezone.utc).replace(tzinfo=None)
        local_now = utc_now + timedelta(hours=st.session_state.tz_offset)
        
        active_idx = -1
        banner_msg = ""
        
        for i in range(1, sessions + 1):
            bring_back = current_time - timedelta(minutes=5)
            finish = current_time + timedelta(minutes=stim_dur) 
            
            if i < sessions:
                next_bring_back = current_time + timedelta(minutes=interval) - timedelta(minutes=5)
                if bring_back <= local_now < next_bring_back:
                    active_idx = i - 1
            else:
                if bring_back <= local_now <= finish:
                    active_idx = i - 1
            
            if banner_msg == "" and local_now < current_time:
                bb_text = f" {format_12h(bring_back)}" if i > 1 else ""
                session_html = f'<span style="color: #845EF7; font-weight: 900;">Session {i}</span>'
                time_html = f'<span style="color: #3B82F6; font-weight: 900;">{bb_text}</span>' if bb_text else ""
                banner_msg = f"Next: {session_html}{time_html}"
            
            bring_back_str = "" if i == 1 else format_12h(bring_back)
            
            tracker_data.append({
                "Session": f"Session {i}",
                "Bring Back": bring_back_str,
                "Start Time": format_12h(current_time),
                "Finish Time": format_12h(finish)
            })
            current_time += timedelta(minutes=interval)
        
        if banner_msg == "":
            banner_msg = "All sessions started for today!"
                
        # Builds the banner with the Text taking most space, and the two emoji buttons hugging the right side
        with status_banner.container():
            col_text, col_ref, col_cam = st.columns([7, 0.7, 0.7])
            
            with col_text:
                st.markdown(f"<div class='banner-text-target' style='color: #007A66; font-weight: 700; font-size: 16px; margin-top: 8px;'>{banner_msg}</div>", unsafe_allow_html=True)
            
            with col_ref:
                st.button("🔄", key="refresh_banner", help="Refresh Highlight")
                
            with col_cam:
                st.markdown("""
                <a class="camera-btn" href="javascript:(function(){ 
                    var script = document.createElement('script'); 
                    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js'; 
                    script.onload = function(){ 
                        html2canvas(document.querySelector('[data-testid=\\'stTable\\']')).then(canvas => { 
                            var link = document.createElement('a'); 
                            link.download = 'TMS_Schedule.png'; 
                            link.href = canvas.toDataURL(); 
                            link.click(); 
                        }); 
                    }; 
                    document.head.appendChild(script); 
                })()" title="Download Schedule Image">📷</a>
                """, unsafe_allow_html=True)
            
        def highlight_custom_cells(x):
            df_style = pd.DataFrame('', index=x.index, columns=x.columns)
            for r in x.index:
                for c in x.columns:
                    style_str = ""
                    if r == active_idx:
                        style_str += "background-color: #E6FFFA; "
                        if c == "Session":
                            style_str += "color: #845EF7; font-weight: 900;" 
                        else:
                            style_str += "color: #00A389; font-weight: 800;" 
                    else:
                        if c == "Session":
                            style_str += "color: #845EF7; font-weight: 800;" 
                    df_style.at[r, c] = style_str
            return df_style

        styled_df = pd.DataFrame(tracker_data).style.apply(highlight_custom_cells, axis=None).hide(axis="index")
        
        st.table(styled_df)
        st.caption("The current block is highlighted in green. The banner at the top updates the moment a session starts.")

# ==========================================
# TAB 2: PERCENTAGE CALCULATOR
# ==========================================
with tab2:
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
            st.dataframe(pd.DataFrame(data), width="stretch", hide_index=True)
