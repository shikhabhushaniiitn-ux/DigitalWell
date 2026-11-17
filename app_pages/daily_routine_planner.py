"""Session-only, editable study-day schedule planner."""

from datetime import date, datetime, time, timedelta

import streamlit as st

st.title("Daily Routine Planner", icon=":material/calendar_month:")
st.caption("Draft a flexible day that makes room for study, breaks, meals, and wind-down time.")
st.info("Your entries stay in this Streamlit session and are not sent to an external service or saved as a profile. This is an editable suggestion, not an ideal routine or assessment.", icon=":material/lock:")

DEFAULTS = {
    "planner_wake": time(7, 0),
    "planner_study_start": time(9, 0),
    "planner_study_hours": 3.0,
    "planner_break_minutes": 10,
    "planner_meal": time(13, 0),
    "planner_bedtime": time(22, 30),
}


def reset_planner() -> None:
    for key, value in DEFAULTS.items():
        st.session_state[key] = value
    st.session_state["planner_schedule"] = None


st.session_state.setdefault("planner_schedule", None)
for state_key, default_value in DEFAULTS.items():
    st.session_state.setdefault(state_key, default_value)
with st.form("routine_inputs"):
    st.markdown("### Your preferred times")
    first = st.columns(3)
    with first[0]:
        wake = st.time_input("Wake-up time", key="planner_wake")
    with first[1]:
        study_start = st.time_input("Preferred study start", key="planner_study_start")
    with first[2]:
        study_hours = st.slider("Total focused study time (hours)", 1.0, 8.0, step=0.5, key="planner_study_hours")
    second = st.columns(3)
    with second[0]:
        break_minutes = st.slider("Break between study blocks (minutes)", 5, 30, step=5, key="planner_break_minutes")
    with second[1]:
        meal = st.time_input("Meal break time", key="planner_meal")
    with second[2]:
        bedtime = st.time_input("Preferred bedtime", key="planner_bedtime")
    submitted = st.form_submit_button("Generate my draft schedule", icon=":material/auto_awesome:", width="stretch")
reset_col, hint_col = st.columns([1, 3], vertical_alignment="center")
with reset_col:
    st.button("Reset planner", on_click=reset_planner, width="stretch")
with hint_col:
    st.caption("Use the times that fit your day. You can change them and generate a new draft at any time.")


def build_schedule(wake_time: time, study_time: time, study_hours_value: float, break_value: int, meal_time: time, bed_time: time):
    day = date.today()
    wake_dt = datetime.combine(day, wake_time)
    study_dt = datetime.combine(day, study_time)
    meal_dt = datetime.combine(day, meal_time)
    bed_dt = datetime.combine(day, bed_time)
    if bed_dt <= wake_dt:
        bed_dt += timedelta(days=1)
    if study_dt < wake_dt:
        return None, "Study start is earlier than wake-up. Adjust one of those times."
    if meal_dt < wake_dt:
        return None, "Meal time is earlier than wake-up. Set the meal within your planned day."
    if meal_dt >= bed_dt:
        return None, "Meal time falls at or after bedtime. Adjust the meal or bedtime."

    wake_end = wake_dt + timedelta(minutes=30)
    meal_end = meal_dt + timedelta(minutes=45)
    wind_down_start = bed_dt - timedelta(minutes=45)
    if study_dt < wake_end:
        return None, "Study starts during the first 30 minutes after wake-up. Move study later or wake earlier."
    if meal_dt < wake_end:
        return None, "The meal overlaps the first 30 minutes after wake-up. Choose a later meal time."
    if meal_end > wind_down_start:
        return None, "The 45-minute meal break overlaps the wind-down period. Move the meal earlier or bedtime later."
    if study_dt >= wind_down_start:
        return None, "Study starts during the wind-down period or later. Move study earlier or bedtime later."

    events = [(wake_dt, wake_end, "Wake-up and morning transition", "Ease into the day; this is an optional planning block.")]
    events.append((meal_dt, meal_end, "Meal break", "A planned pause away from study tasks."))
    remaining = int(study_hours_value * 60)
    cursor = study_dt
    while remaining > 0:
        block_minutes = min(50, remaining)
        if cursor < meal_end and cursor + timedelta(minutes=block_minutes) > meal_dt:
            cursor = meal_end
        elif meal_dt <= cursor < meal_end:
            cursor = meal_end
        end = cursor + timedelta(minutes=block_minutes)
        if end > wind_down_start:
            return None, "The requested study time does not fit before the meal and wind-down blocks. Reduce study hours or adjust the times."
        events.append((cursor, end, "Focused study", "One study block; choose the task that matters now."))
        cursor = end
        remaining -= block_minutes
        if remaining > 0:
            if cursor < meal_end and cursor + timedelta(minutes=break_value) > meal_dt:
                cursor = meal_end
            elif meal_dt <= cursor < meal_end:
                cursor = meal_end
            else:
                break_end = cursor + timedelta(minutes=break_value)
                if cursor < meal_dt < break_end:
                    cursor = meal_end
                else:
                    events.append((cursor, break_end, "Short study break", "Step away from the current task if that feels useful."))
                    cursor = break_end
    events.append((wind_down_start, bed_dt, "Wind-down time", "Optional time to shift away from study and review evening device settings."))
    events.append((bed_dt, bed_dt + timedelta(minutes=15), "Preferred bedtime", "Your chosen bedtime marker."))
    events.sort(key=lambda item: item[0])
    for earlier, later in zip(events, events[1:]):
        if earlier[1] > later[0]:
            return None, "Some planned activities overlap. Try different times or a shorter study duration."
    return events, None


if submitted:
    schedule, error = build_schedule(wake, study_start, study_hours, break_minutes, meal, bedtime)
    st.session_state["planner_schedule"] = {"events": schedule, "error": error}

result = st.session_state.get("planner_schedule")
if result:
    if result["error"]:
        st.error(result["error"], icon=":material/event_busy:")
    else:
        st.markdown("### Your editable draft")
        base_day = result["events"][0][0].date()
        rows = []
        for start, end, title, note in result["events"]:
            start_label = f"{'Next day · ' if start.date() > base_day else ''}{start:%I:%M %p}"
            end_label = f"{'Next day · ' if end.date() > base_day else ''}{end:%I:%M %p}"
            rows.append({"Time": f"{start_label} – {end_label}", "Activity": title, "Idea": note})
        st.dataframe(rows, hide_index=True, width="stretch", height=min(540, 42 * len(rows) + 44), column_config={"Time": st.column_config.TextColumn("Time", width="medium"), "Activity": st.column_config.TextColumn("Activity", width="medium"), "Idea": st.column_config.TextColumn("Optional suggestion", width="large")}, key="daily_routine_schedule", alt="Suggested schedule with times, activities, and optional ideas")
        st.caption("This is a draft: edit the inputs to regenerate it, and change or ignore any block that does not suit you.")
