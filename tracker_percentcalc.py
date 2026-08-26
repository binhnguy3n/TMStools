import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configure the page
st.set_page_config(page_title="Utility Tools", layout="centered", page_icon="⚙️")

st.title("⚙️ Utility Tools")

# Create tabs for the two different tools
tab1, tab2 = st.tabs(["📊 Percentage Calculator", "⏱️ Session Tracker"])

# ==========================================
# TAB 1: PERCENTAGE CALCULATOR
# ==========================================
with tab1:
    st.write("Calculate a sequence of values based on a known percentage and step size.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("### 1. Known Values")
        known_pct = st.number_input("Known Percentage (%)", min_value=0.1, value=120.0, step=1.0)
        known_val = st.number_input("Known Value", value=78.0, step=1.0)
    
    with col_b:
        st.write("### 2. Table Settings")
        start_pct = st.number_input("Start Percentage (%)", value=30.0, step=1.0)
        end_pct = st.number_input("End Percentage (%)", value=120.0, step=1.0)
        step_pct = st.number_input("Step Percentage (%)", min_value=0.1, value=5.0, step=1.0)
    
    # Calculations
    if known_pct > 0:
        base_value = known_val / (known_pct / 100)
        step_value = base_value * (step_pct / 100)
        
        st.info(f"**Base Value (100%):** {base_value:g} &nbsp; | &nbsp; **{step_pct:g}% increment:** {step_value:g}")
        
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
    st.write("Generate a schedule of sessions with bring-back, start, and finish times.")
    
    # Preset selection
    mode = st.radio(
        "Choose Configuration Mode", 
        ["Custom", "MAGNETS Preset", "MANIFEST Preset"],
        horizontal=True
    )
    
    # Setup variables based on mode
    if mode == "MAGNETS Preset":
        sessions = 10
        stim_dur = 10
        interval = 50
        start_dt = datetime.now()
        st.success("✅ **MAGNETS Loaded:** 10 Sessions | 10m Stim | 50m Start-to-Start | Start time: NOW")
        
    elif mode == "MANIFEST Preset":
        sessions = 5
        stim_dur = 10
        interval = 40
        start_dt = datetime.now()
        st.success("✅ **MANIFEST Loaded:** 5 Sessions | 10m Stim | 40m Start-to-Start | Start time: NOW")
        
    else: # Custom Mode
        col1, col2 = st.columns(2)
        with col1:
            sessions = st.number_input("Total Number of Sessions", min_value=1, value=5, step=1)
            start_time_val = st.time_input("First Session Start Time", value=datetime.now().time())
        with col2:
            stim_dur = st.number_input("Stimulation Duration (mins)", min_value=1, value=10, step=1)
            interval = st.number_input("Rest Duration (Start-to-Start in mins)", min_value=1, value=40, step=1)
            
        # Combine today's date with the user's chosen time to allow for time math
        start_dt = datetime.combine(datetime.today(), start_time_val)
    
    # Generate schedule
    if st.button("Generate Schedule", type="primary") or mode != "Custom":
        tracker_data = []
        current_time = start_dt
        
        for i in range(1, sessions + 1):
            bring_back = current_time - timedelta(minutes=5)
            # Calculates finish time dynamically based on the stimulation duration
            finish = current_time + timedelta(minutes=stim_dur) 
            
            tracker_data.append({
                "Session": f"Session {i}",
                "Bring Back (-5m)": bring_back.strftime("%I:%M %p"),
                "Start Time": current_time.strftime("%I:%M %p"),
                "Finish Time": finish.strftime("%I:%M %p")
            })
            
            # Increment time by the start-to-start interval for the next loop
            current_time += timedelta(minutes=interval)
            
        # Display the schedule table
        tracker_df = pd.DataFrame(tracker_data)
        st.dataframe(tracker_df, use_container_width=True, hide_index=True)
