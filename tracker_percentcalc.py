import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import streamlit.components.v1 as components

# ==========================================
# PAGE CONFIGURATION & SESSION STATE
# ==========================================
st.set_page_config(page_title="TMS Tools", layout="centered", page_icon="🧰")

if "tz_offset" not in st.session_state:
    st.session_state.tz_offset = -6

def set_time_to_now():
    utc_now = datetime.now(timezone.utc).replace(tzinfo=None)
    local_now = utc_now + timedelta(hours=st.session_state.tz_offset)
    st.session_state.hour = int(local_now.strftime("%I"))
    st.session_state.minute = f"{local_now.minute:02d}"
    st.session_state.ampm = local_now.strftime("%p")

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
# 80s RETRO-POP / NEO-BRUTALIST THEME CSS
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@600;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Nunito', sans-serif !important; }
    
    /* Inputs */
    .stTextInput > div > div > input, .stNumberInput > div > div > input, div[data-baseweb="select"] > div {
        border-radius: 8px !important; border: 3px solid #1E1E1E !important;
        background-color: #FAFAFA !important; font-weight: 800 !important;
        box-shadow: 4px 4px 0px #FFE66D !important; transition: all 0.1s ease !important;
    }
    
    /* Primary buttons (Generate, Now) - Fixed wrapping issue */
    button[kind="primary"] {
        background-color: #FF6B6B !important; color: white !important;
        border-radius: 8px !important; font-weight: 900 !important; font-size: 16px !important;
        border: 3px solid #1E1E1E !important; padding: 6px 16px !important; min-height: 42px !important; height: auto !important; margin: 0 !important;
        box-shadow: 4px 4px 0px #1E1E1E !important; transition: all 0.1s ease !important;
        white-space: nowrap !important; display: inline-flex !important; align-items: center !important; justify-content: center !important;
    }
    button[kind="primary"]:active { transform: translate(4px, 4px) !important; box-shadow: 0px 0px 0px #1E1E1E !important; }
    button[kind="primary"]:hover { background-color: #FF8787 !important; }

    /* Secondary buttons (Refresh) */
    button[kind="secondary"] {
        background-color: white !important; color: #1E1E1E !important;
        border-radius: 8px !important; font-weight: 900 !important; font-size: 16px !important;
        border: 3px solid #1E1E1E !important; padding: 6px 16px !important; min-height: 42px !important; height: auto !important; margin: 0 !important;
        box-shadow: 4px 4px 0px #1E1E1E !important; transition: all 0.1s ease !important;
        white-space: nowrap !important; display: inline-flex !important; align-items: center !important; justify-content: center !important;
    }
    button[kind="secondary"]:active { transform: translate(4px, 4px) !important; box-shadow: 0px 0px 0px #1E1E1E !important; }
    button[kind="secondary"]:hover { background-color: #E6FFFA !important; }

    /* Preset Info Boxes */
    div[data-testid="stAlert"] {
        border-radius: 8px !important; background-color: #F0F9FF !important;
        border: 3px solid #1E1E1E !important; color: #1E1E1E !important; 
        box-shadow: 5px 5px 0px #4ECDC4 !important; font-weight: 800 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { border-radius: 12px 12px 0 0 !important; font-weight: 900 !important; padding: 10px 20px !important; }
    
    /* 80s Table Styling */
    [data-testid="stTable"] { 
        background-color: white !important; padding: 10px; border-radius: 8px; 
        border: 3px solid #1E1E1E !important; box-shadow: 6px 6px 0px #FFE66D !important; margin-bottom: 20px;
    }
    [data-testid="stTable"] table { width: 100% !important; border-collapse: collapse !important; }
    [data-testid="stTable"] th { background-color: #FAFAFA !important; border-bottom: 3px solid #1E1E1E !important; font-weight: 900 !important; white-space: nowrap !important;}
    [data-testid="stTable"] td, [data-testid="stTable"] th { padding: 12px 10px !important; font-weight: 700; color: #1E1E1E; white-space: nowrap !important;}
    [data-testid="stTable"] tr { border-bottom: 2px solid #F3F4F6 !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# LIVE DATE/TIME BANNER
# ==========================================
components.html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@700;900&display=swap');
    body { margin: 0; padding: 5px; font-family: 'Nunito', sans-serif; background-color: transparent; }
    .banner {
        background-color: #FAFAFA; border-radius: 8px; padding: 16px 20px;
        display: flex; justify-content: center; align-items: center; gap: 40px; 
        border: 3px solid #1E1E1E; color: #1E1E1E; box-shadow: 5px 5px 0px #FF6B6B;
    }
    .date { font-size: 18px; font-weight: 700; color: #1E1E1E; }
    .time { font-size: 22px; font-weight: 900; color: #845EF7; }
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
""", height=90)

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
        st.write("##### Initial Start Time")
        
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
    
    # Action Buttons (Generate, Refresh, and Camera side-by-side)
    col_gen, col_ref, col_cam, col_spacer = st.columns([1.6, 1.2, 1.2, 1.5])
    
    with col_gen:
        if st.button("Generate Schedule", type="primary"):
            st.session_state.schedule_generated = True
            
    if st.session_state.schedule_generated:
        with col_ref:
            st.button("🔄 Refresh", help="Update the green highlight")
            
        with col_cam:
            # Styled identical to the Python buttons above, but triggers JavaScript
            components.html("""
            <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@600;800;900&display=swap');
                body { margin: 0; padding: 0; display: flex; align-items: flex-start; font-family: 'Nunito', sans-serif;}
                .camera-btn {
                    background-color: white; color: #1E1E1E; border: 3px solid #1E1E1E; border-radius: 8px;
                    padding: 6px 16px; min-height: 42px; font-size: 16px; font-weight: 900; box-shadow: 4px 4px 0px #1E1E1E; 
                    cursor: pointer; transition: all 0.1s ease; display: inline-flex; align-items: center; justify-content: center;
                    white-space: nowrap; text-decoration: none;
                }
                .camera-btn:active { transform: translate(4px, 4px); box-shadow: 0px 0px 0px #1E1E1E; }
                .camera-btn:hover { background-color: #E6FFFA; }
            </style>
            <button class="camera-btn" onclick="takePic()" title="Download Schedule Image">📷 Save</button>
            <script>
                function takePic() {
                    try {
                        const target = window.parent.document.querySelector('[data-testid="stTable"]');
                        if (target) {
                            html2canvas(target, {
                                backgroundColor: '#ffffff', 
                                scale: 2,
                                onclone: function (clonedDoc) {
                                    const cells = clonedDoc.querySelectorAll('[data-testid="stTable"] th, [data-testid="stTable"] td');
                                    cells.forEach(cell => {
                                        cell.style.fontFamily = 'Arial, sans-serif';
                                        cell.style.letterSpacing = 'normal';
                                        cell.style.whiteSpace = 'nowrap';
                                    });
                                }
                            }).then(canvas => {
                                const link = document.createElement('a');
                                link.download = 'TMS_Schedule.png';
                                link.href = canvas.toDataURL();
                                link.click();
                            });
                        } else {
                            alert('Table not found.');
                        }
                    } catch (e) {
                        alert('Browser security prevents capturing the image directly. Please take a manual screenshot.');
                    }
                }
            </script>
            """, height=50)
            
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
                bb_text = f" &nbsp;{format_12h(bring_back)}" if i > 1 else ""
                session_html = f'<span style="color: #845EF7; font-weight: 900;">Session {i}</span>'
                time_html = f'<span style="color: #3B82F6; font-weight: 900;">{bb_text}</span>' if bb_text else ""
                # Added strict HTML non-breaking spaces for a clean gap
                banner_msg = f"Next: &nbsp;&nbsp; {session_html}{time_html}"
            
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
                
        status_banner.markdown(f"""
        <div style="background-color: #E6FFFA; border: 3px solid #1E1E1E; box-shadow: 5px 5px 0px #00A389; border-radius: 8px; padding: 12px 16px; margin-top: -5px; margin-bottom: 25px; color: #1E1E1E; font-weight: 800; text-align: center; font-size: 18px;">
            {banner_msg}
        </div>
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
                            style_str += "color: #00A389; font-weight: 900;" 
                    else:
                        if c == "Session":
                            style_str += "color: #845EF7; font-weight: 900;" 
                    df_style.at[r, c] = style_str
            return df_style

        styled_df = pd.DataFrame(tracker_data).style.apply(highlight_custom_cells, axis=None).hide(axis="index")
        
        st.table(styled_df)

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
