import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURATION ---
TASKS = ["Wake Up Early", "Gym", "Breakfast", "Attend Full College", "Lunch", "2h Study", "2h Self-Improvement"]
DATA_FILE = "habit_data.csv"

st.set_page_config(page_title="6-Month Transformation Tracker", page_icon="📈")

# --- DATA ENGINE ---
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, index_col=0)
    return pd.DataFrame(columns=TASKS)

def save_data(df):
    df.to_csv(DATA_FILE)

data = load_data()
today = datetime.now().strftime("%Y-%m-%d")

# --- UI ---
st.title("🚀 6-Month Rebuild Tracker")
st.subheader(f"Date: {today}")

# Create columns for today's checkboxes
st.info("Complete your tasks to build your streak. No excuses.")
current_progress = {}
cols = st.columns(2)

for i, task in enumerate(TASKS):
    # Split tasks into two columns for better UI
    with cols[i % 2]:
        # Check if we already have data for today
        default_val = False
        if today in data.index:
            default_val = bool(data.loc[today, task])
        
        current_progress[task] = st.checkbox(task, value=default_val)

if st.button("Save Progress"):
    data.loc[today] = current_progress
    save_data(data)
    st.success("Progress saved!")

# --- PROGRESSION ANALYTICS ---
st.divider()
st.header("📊 Progression")

if not data.empty:
    # Calculate Streak
    data = data.sort_index(ascending=False)
    streak = 0
    for i in range(len(data)):
        if data.iloc[i].all(): # If all tasks were ticked
            streak += 1
        else:
            break
    
    col1, col2 = st.columns(2)
    col1.metric("Current Streak", f"{streak} Days")
    col2.metric("Total Days Logged", len(data))

    # Visual Representation
    st.write("### Recent History")
    st.dataframe(data.head(10).style.highlight_max(axis=0, color='lightgreen'))
else:
    st.write("Start today to see your progression analytics!")

st.sidebar.markdown("""
### 💡 Mental Reminders:
1. **Phone stays off** for the first 10 mins.
2. **Ground yourself** when overthinking starts.
3. **5-4-3-2-1** - Move before the brain stops you.
""")
