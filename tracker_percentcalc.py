import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone

# ==========================================
# PAGE CONFIGURATION & SESSION STATE
# ==========================================
st.set_page_config(page_title="TMS Tools", layout="centered", page_icon="🧰")

if "tz_offset" not in st.session_state:
    st.session_state.tz_offset = -6

if "synthwave_toggle" not in st.session_state:
    st.session_state.synthwave_toggle = False

def set_time_to_now():
    utc_now = datetime.now(timezone.utc).replace(tzinfo=None)
    local_now = utc_now + timedelta(hours=st.session_state.tz_offset)
    st.session_state.hour = int(local_now.strftime("%I"))
    st.session_state.minute = f"{local_now.minute:02d}"
    st.session_state.ampm = local_now.strftime("%p")

def set_mode(m):
    st.session_state.mode = m

def toggle_theme():
    st.session_state.synthwave_toggle = not st.session_state.synthwave_toggle

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
# DYNAMIC THEME DICTIONARY
# ==========================================
is_synthwave = st.session_state.synthwave_toggle

if is_synthwave:
    theme = {
        "bg_color": "#090A0F",
        "panel_bg": "#151821",
        "border": "#05D9E8",
        "shadow_1": "#FF2A6D",
        "shadow_2": "#B100E8",
        "text_main": "#E0E6ED",
        "text_header": "#05D9E8",
        "btn_primary_bg": "#FF2A6D",
        "btn_primary_shadow": "#05D9E8",
        "btn_primary_text": "#090A0F",
        "btn_sec_shadow": "#B100E8",
        "btn_sec_hover": "#23283B",
        "active_config_bg": "#FFC900",
        "active_config_text": "#090A0F",
        "active_row_bg": "#2A0826", 
        "active_row_text": "#FFC900",
        "zebra_bg": "#0e1017",
        "session_col": "#FF2A6D",
        "time_col": "#05D9E8",
        "next_banner_bg": "#151821",
        "next_banner_border": "#05D9E8",
        "next_banner_shadow": "#FF2A6D",
        "clock_shadow": "#FF2A6D"
    }
else:
    theme = {
        "bg_color": "#FFFFFF",
        "panel_bg": "#FAFAFA",
        "border": "#1E1E1E",
        "shadow_1": "#4ECDC4",
        "shadow_2": "#FFE66D",
        "text_main": "#1E1E1E",
        "text_header": "#1E1E1E",
        "btn_primary_bg": "#FF6B6B",
        "btn_primary_shadow": "#1E1E1E",
        "btn_primary_text": "#FFFFFF",
        "btn_sec_shadow": "#374151",  # Dark Slate Gray Shadow for Theme Toggle & Tabs!
        "btn_sec_hover": "#F3F4F6",
        "active_config_bg": "#FFE66D",
        "active_config_text": "#1E1E1E",
        "active_row_bg": "#E6FFFA", 
        "active_row_text": "#00A389",
        "zebra_bg": "#F3F4F6",
        "session_col": "#845EF7",
        "time_col": "#3B82F6",
        "next_banner_bg": "#E6FFFA",
        "next_banner_border": "#1E1E1E",
        "next_banner_shadow": "#00A389",
        "clock_shadow": "#FF6B6B"
    }

# ==========================================
# DYNAMIC NEO-BRUTALIST / SYNTHWAVE CSS
# ==========================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@600;800;900&display=swap');
    html, body, [class*="css"] {{ font-family: 'Nunito', sans-serif !important; }}
    
    .stApp {{ background-color: {theme['bg_color']} !important; }}
    h1, h2, h3, h4, h5, h6 {{ color: {theme['text_header']} !important; }}
    p, label, li {{ color: {theme['text_main']} !important; }}
    
    /* Inputs */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {{
        border-radius: 8px !important; border: 3px solid {theme['border']} !important;
        background-color: {theme['panel_bg']} !important; font-weight: 800 !important; color: {theme['text_header']} !important;
        box-shadow: 4px 4px 0px {theme['shadow_2']} !important; transition: all 0.1s ease !important;
    }}
    div[data-baseweb="select"] > div {{
        border-radius: 8px !important; border: 3px solid {theme['border']} !important;
        background-color: {theme['panel_bg']} !important; font-weight: 800 !important; color: {theme['text_header']} !important;
        box-shadow: 4px 4px 0px {theme['shadow_2']} !important; transition: all 0.1s ease !important;
        padding-left: 2px !important; padding-right: 2px !important;
    }}
    
    /* Stop Streamlit flexbox from dynamically squishing/stretching buttons */
    div[data-testid="stButton"] {{ width: fit-content !important; }}

    /* Primary buttons (Generate, Now) */
    button[kind="primary"] {{
        background-color: {theme['btn_primary_bg']} !important; color: {theme['btn_primary_text']} !important;
        border-radius: 8px !important; font-weight: 900 !important; font-size: 16px !important;
        border: 3px solid {theme['border']} !important; padding: 6px 16px !important; height: 48px !important; margin: 0 !important;
        box-shadow: 4px 4px 0px {theme['btn_primary_shadow']} !important; transition: all 0.1s ease !important;
        white-space: nowrap !important; display: inline-flex !important; align-items: center !important; justify-content: center !important; width: max-content !important;
    }}
    button[kind="primary"]:active {{ transform: translate(4px, 4px) !important; box-shadow: 0px 0px 0px transparent !important; }}
    button[kind="primary"]:hover {{ filter: brightness(1.1); }}

    /* Secondary buttons (Config Modes, Refresh, Camera) - STRICTLY LOCKED 48x48 SQUARES */
    button[kind="secondary"] {{
        background-color: {theme['panel_bg']} !important; color: {theme['border']} !important;
        border-radius: 8px !important; font-weight: 900 !important; font-size: 22px !important;
        border: 3px solid {theme['border']} !important; 
        width: 48px !important; min-width: 48px !important; max-width: 48px !important;
        height: 48px !important; min-height: 48px !important; max-height: 48px !important; 
        padding: 0 !important; margin: 0 !important; box-sizing: border-box !important;
        box-shadow: 4px 4px 0px {theme['btn_sec_shadow']} !important; transition: all 0.1s ease !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
    }}
    button[kind="secondary"]:active {{ transform: translate(4px, 4px) !important; box-shadow: 0px 0px 0px transparent !important; }}
    button[kind="secondary"]:hover {{ background-color: {theme['btn_sec_hover']} !important; }}

    /* Active Secondary (Disabled Config Button) */
    button[kind="secondary"]:disabled {{
        background-color: {theme['active_config_bg']} !important; color: {theme['active_config_text']} !important;
        transform: translate(4px, 4px) !important; box-shadow: 0px 0px 0px transparent !important;
        opacity: 1 !important; cursor: default !important; border-color: {theme['border']} !important;
    }}

    /* Tertiary button (Theme Toggle ONLY) -> Keeps text wide dynamically */
    button[kind="tertiary"] {{
        background-color: {theme['panel_bg']} !important; color: {theme['border']} !important;
        border-radius: 8px !important; font-weight: 900 !important; font-size: 16px !important;
        border: 3px solid {theme['border']} !important; height: 48px !important; padding: 0 16px !important; margin: 0 !important;
        box-shadow: 4px 4px 0px {theme['btn_sec_shadow']} !important; transition: all 0.1s ease !important;
        width: max-content !important;
    }}
    button[kind="tertiary"]:active {{ transform: translate(4px, 4px) !important; box-shadow: 0px 0px 0px transparent !important; }}
    button[kind="tertiary"]:hover {{ background-color: {theme['btn_sec_hover']} !important; }}

    /* Preset Info Boxes */
    div[data-testid="stAlert"] {{
        border-radius: 8px !important; background-color: {theme['panel_bg']} !important;
        border: 3px solid {theme['border']} !important; color: {theme['text_main']} !important; 
        box-shadow: 5px 5px 0px {theme['shadow_1']} !important; font-weight: 800 !important;
    }}
    
    /* ----------------------------------------------------
       COMPLETELY CUSTOMIZED BRUTALIST UI TABS 
       ---------------------------------------------------- */
       
    /* 1. Nuke ALL Streamlit native tab decorations safely */
    div[data-testid="stTabIndicator"], div[data-testid="stTabs"] [data-baseweb="tab-highlight"], div[data-testid="stTabs"] [data-baseweb="tab-border"] {{
        display: none !important; opacity: 0 !important; visibility: hidden !important; height: 0px !important; width: 0px !important;
    }}
    
    /* 2. NUCLEAR OVERRIDE: Shatter Streamlit's hidden clipping walls on all tab containers */
    div[data-testid="stTabs"], div[data-testid="stTabs"] * {{ 
        overflow: visible !important; 
    }}
    
    /* 3. Give the list container physical room for the shadow */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {{ 
        gap: 16px !important; padding-bottom: 25px !important; padding-top: 5px !important;
    }}
    
    /* 4. The Tab Headers - Targeted universally inside the tab list */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] button {{ 
        background-color: {theme['panel_bg']} !important; border: 3px solid {theme['border']} !important; border-radius: 8px !important;
        padding: 8px 24px !important; box-shadow: 4px 4px 0px {theme['btn_sec_shadow']} !important; transition: all 0.1s ease !important; 
        margin: 0px 8px 15px 0px !important; /* Critical margin ensures shadow renders */
        min-width: fit-content !important; height: auto !important; 
    }}
    div[data-testid="stTabs"] [data-baseweb="tab-list"] button:hover {{ 
        background-color: {theme['btn_sec_hover']} !important; 
    }}
    
    /* 5. The Active Tab - Press animation */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] button[aria-selected="true"] {{ 
        background-color: {theme['btn_primary_bg']} !important; 
        box-shadow: 0px 0px 0px transparent !important; transform: translate(4px, 4px) !important; border-color: {theme['border']} !important;
    }}
    
    /* Force bold text natively on the headers */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] button p, div[data-testid="stTabs"] [data-baseweb="tab-list"] button span {{ 
        font-weight: 900 !important; color: {theme['text_main']} !important; margin: 0 !important;
    }}
    div[data-testid="stTabs"] [data-baseweb="tab-list"] button[aria-selected="true"] p, div[data-testid="stTabs"] [data-baseweb="tab-list"] button[aria-selected="true"] span {{ 
        color: {theme['btn_primary_text']} !important;
    }}
    
    /* ---------------------------------------------------- */
    
    /* 80s Table Styling */
    [data-testid="stTable"] {{ 
        background-color: {theme['bg_color']} !important; padding: 10px; border-radius: 8px; 
        border: 3px solid {theme['border']} !important; box-shadow: 6px 6px 0px {theme['shadow_2']} !important; margin-bottom: 20px;
    }}
    [data-testid="stTable"] table {{ width: 100% !important; border-collapse: collapse !important; }}
    [data-testid="stTable"] th {{ background-color: {theme['panel_bg']} !important; border-bottom: 3px solid {theme['border']} !important; font-weight: 900 !important; white-space: nowrap !important; color: {theme['text_header']} !important; }}
    [data-testid="stTable"] td, [data-testid="stTable"] th {{ padding: 12px 10px !important; font-weight: 700; white-space: nowrap !important;}}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 1. TITLE & TOGGLE
# ==========================================
col_title, col_spacer, col_toggle = st.columns([3, 0.5, 1.5])
with col_title:
    st.title("🧰 TMS Tools")
with col_toggle:
    st.markdown("<br>", unsafe_allow_html=True) 
    btn_text = "☀️ Light Mode" if is_synthwave else "🕶️ Synthwave"
    # Tertiary type allows the theme toggle text to breathe properly without squishing
    st.button(btn_text, on_click=toggle_theme, key="theme_btn", type="tertiary")


# ==========================================
# 2. BULLETPROOF CLOCK BANNER (100% Python Native!)
# ==========================================
# Grabbing exact local time instantly on every app interaction
clock_now = datetime.now(timezone.utc) + timedelta(hours=st.session_state.tz_offset)
current_date_str = clock_now.strftime("%A, %B %d, %Y")
current_time_str = clock_now.strftime("%I:%M %p").lstrip("0")

st.markdown(f"""
<div style="background-color: {theme['panel_bg']}; border-radius: 8px; padding: 16px 20px; display: flex; justify-content: center; align-items: center; gap: 40px; border: 3px solid {theme['border']}; box-shadow: 5px 5px 0px {theme['clock_shadow']}; margin-bottom: 25px; font-family: 'Nunito', sans-serif;">
    <div style="font-size: 18px; font-weight: 700; color: {theme['text_main']};">{current_date_str}</div>
    <div style="font-size: 22px; font-weight: 900; color: {theme['time_col']};">{current_time_str}</div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 3. NEXT SESSION BANNER (Placed directly below clock)
# ==========================================
status_banner = st.empty()


# ==========================================
# 4. TABS
# ==========================================
tab1, tab2 = st.tabs(["⏱️ Session Tracker", "📊 Percentage Calculator"])

def format_12h(dt):
    return dt.strftime("%I:%M %p").lstrip("0")


# ==========================================
# TAB 1: SESSION TRACKER
# ==========================================
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.6, 2], gap="large")
    
    with col_left:
        st.write("##### Configuration Mode")
        mode = st.session_state.mode
        
        # Reduced gap spacing to bring the buttons closer together
        col_m1, col_m2, col_m3, col_mspace = st.columns([1, 1, 1, 6], gap="small")
        # Assigned type="secondary" here so they snap mathematically to exactly 48x48 squares!
        with col_m1:
            st.button("🧲", key="btn_mag", on_click=set_mode, args=("MAGNETS",), disabled=(mode == "MAGNETS"), help="MAGNETS Preset", type="secondary")
        with col_m2:
            st.button("✨", key="btn_man", on_click=set_mode, args=("MANIFEST",), disabled=(mode == "MANIFEST"), help="MANIFEST Preset", type="secondary")
        with col_m3:
            st.button("⚙️", key="btn_cus", on_click=set_mode, args=("Custom",), disabled=(mode == "Custom"), help="Custom Configuration", type="secondary")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.write("##### Initial Start Time")
        col_btn, col_tz = st.columns([1, 1.5], gap="small")
        with col_btn:
            st.button("🕒 Now", on_click=set_time_to_now, type="primary")
        with col_tz:
            st.selectbox(
                "Local TZ Offset", 
                options=[i for i in range(-12, 13)], 
                format_func=lambda x: f"UTC{'+' if x >= 0 else ''}{x}", 
                key="tz_offset",
                label_visibility="collapsed"
            )
        
        t1, t2, t3 = st.columns([1, 1.2, 1.5])
        with t1:
            hour_val = st.selectbox("Hr", options=list(range(1, 13)), key="hour", label_visibility="collapsed")
        with t2:
            min_val = st.selectbox("Min", options=[f"{m:02d}" for m in range(60)], key="minute", label_visibility="collapsed")
        with t3:
            ampm_val = st.selectbox("AM/PM", options=["AM", "PM"], key="ampm", label_visibility="collapsed")
            
        time_str = f"{hour_val}:{min_val} {ampm_val}"
        start_time_obj = datetime.strptime(time_str, "%I:%M %p").time()
        start_dt = datetime.combine(datetime.today(), start_time_obj)
        
    with col_right:
        st.markdown("<div style='height: 38px;'></div>", unsafe_allow_html=True)
        
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
    
    # Bottom alignment securely aligns the primary button and the icon buttons perfectly
    col_gen, col_ref, col_cam, col_spacer = st.columns([3, 1, 1, 5], gap="small", vertical_alignment="bottom")
    
    with col_gen:
        if st.button("Generate Schedule", type="primary"):
            st.session_state.schedule_generated = True
            
    if st.session_state.schedule_generated:
        with col_ref:
            # Type is secondary, locking it perfectly to 48x48 like the config modes
            st.button("🔄", help="Update the active highlight", type="secondary")
            
        with col_cam:
            # Replaced custom HTML with a native st.button for flawless Streamlit grid alignment!
            st.button("📷", key="cam_btn", type="secondary", help="Download Schedule Image")
            
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
                bb_text = f"{format_12h(bring_back)}" if i > 1 else ""
                session_html = f'<span style="color: {theme["session_col"]}; font-weight: 900;">Session {i}</span>'
                time_html = f'<span style="color: {theme["time_col"]}; font-weight: 900;">{bb_text}</span>' if bb_text else ""
                spacing = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" if bb_text else ""
                banner_msg = f"Next: &nbsp;&nbsp; {session_html}{spacing}{time_html}"
            
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
                
        # Send the banner text back up the page to the global placeholder
        status_banner.markdown(f"""
        <div style="background-color: {theme['next_banner_bg']}; border: 3px solid {theme['next_banner_border']}; box-shadow: 5px 5px 0px {theme['next_banner_shadow']}; border-radius: 8px; padding: 12px 16px; margin-top: -5px; margin-bottom: 25px; color: {theme['text_main']}; font-weight: 800; text-align: center; font-size: 18px;">
            {banner_msg}
        </div>
        """, unsafe_allow_html=True)
            
        def highlight_custom_cells(x):
            df_style = pd.DataFrame('', index=x.index, columns=x.columns)
            for row_num, r in enumerate(x.index):
                for c in x.columns:
                    style_str = ""
                    if r == active_idx:
                        style_str += f"background-color: {theme['active_row_bg']}; "
                        if c == "Session":
                            style_str += f"color: {theme['session_col']}; font-weight: 900;" 
                        else:
                            style_str += f"color: {theme['active_row_text']}; font-weight: 900;" 
                    else:
                        if row_num % 2 == 1:
                            style_str += f"background-color: {theme['zebra_bg']}; "
                        else:
                            style_str += f"background-color: {theme['bg_color']}; "
                            
                        if c == "Session":
                            style_str += f"color: {theme['session_col']}; font-weight: 900;" 
                        else:
                            style_str += f"color: {theme['text_main']};"
                            
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

# ==========================================
# SILENT BACKEND DOM SCRIPT RUNNER (CAMERA INTEGRATION)
# ==========================================
# This purely binds to the camera button natively rendered by Streamlit above
st.html(f"""
<script>
    (function() {{
        function attachCamera() {{
            let doc = document;
            try {{ doc = window.parent.document || document; }} catch(e) {{}}
            
            const btns = doc.querySelectorAll('button');
            let camBtn = null;
            btns.forEach(b => {{ if (b.innerText.includes('📷')) camBtn = b; }});
            
            if (camBtn && !camBtn.dataset.attached) {{
                camBtn.addEventListener('click', function(e) {{
                    e.preventDefault();
                    e.stopPropagation();
                    const target = doc.querySelector('[data-testid="stTable"]');
                    if (target) {{
                        const script = doc.createElement('script');
                        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
                        script.onload = () => {{
                            window.parent.html2canvas(target, {{ backgroundColor: '{theme["bg_color"]}', scale: 2 }}).then(canvas => {{
                                const link = doc.createElement('a');
                                link.download = 'TMS_Schedule.png';
                                link.href = canvas.toDataURL();
                                link.click();
                            }});
                        }};
                        doc.head.appendChild(script);
                    }} else {{
                        alert('Table not found. Please generate the schedule first!');
                    }}
                }});
                camBtn.dataset.attached = 'true';
            }} else if (!camBtn) {{
                setTimeout(attachCamera, 1000);
            }}
        }}
        attachCamera();
    }})();
</script>
""")
