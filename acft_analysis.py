import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Column mapping for readability
col_map = {
    "soldier_acft_id": "Soldier ID",
    "test_date": "Test Date",
    "uic": "Unit (UIC)",
    "mos": "MOS",
    "sex": "Sex",
    "rank": "Rank",
    "rank_category": "Rank Category",
    "pay_grade": "Pay Grade",
    "age_at_test": "Age",
    "test_type": "Test Type",
    "profile": "Profile",
    "raw_plank": "Plank (sec)",
    "raw_strength_deadlift": "Deadlift (lbs)",
    "raw_standing_power_throw": "Standing Power Throw (m)",
    "raw_hand_release_push_up": "Hand Release Push-ups",
    "raw_sprint_drag_carry": "Sprint-Drag-Carry (sec)",
    "raw_2mi_run": "2-Mile Run (sec)",
    "raw_alt_aerobic": "Alt Aerobic (sec)",
    "plank_score": "Plank Score",
    "strength_deadlift_score": "Deadlift Score",
    "alt_aerobic_event": "Alt Aerobic Event",
    "standing_power_throw_score": "Power Throw Score",
    "hand_release_push_up_score": "Push-up Score",
    "sprint_drag_carry_score": "Sprint-Drag-Carry Score",
    "2mi_run_score": "2-Mile Run Score",
    "alt_aerobic_score": "Alt Aerobic Score",
    "total_score": "Total Score",
    "test_status": "Test Status",
    "deadlift_not_attempted": "Deadlift Not Attempted",
    "plank_not_attempted": "Plank Not Attempted",
    "power_throw_not_attempted": "Power Throw Not Attempted",
    "pushup_not_attempted": "Push-up Not Attempted",
    "sprint_not_attempted": "Sprint Not Attempted",
}

# Load dataset function
def load_data():
    try:
        df = pd.read_csv("acft_demo.csv")
    except FileNotFoundError:
        st.error("Default dataset acft_demo.csv not found. Please upload a dataset.")
        return None

    # Rename columns for readability
    df.rename(columns=col_map, inplace=True)
    return df

# Streamlit app
def main():
    st.sidebar.title("ACFT Data Explorer")
    page = st.sidebar.radio(
        "Navigation",
        [
            "Home",
            "Overview",
            "Demographic Breakdown",
            "Event Performance",
            "Participation Analysis",
            "Score Trends",
        ],
    )

    df = load_data()

    if page == "Home":
        st.title("Army Combat Fitness Test (ACFT) Data Explorer")
        st.write("""
        This interactive dashboard allows commanders, trainers, and analysts to
        explore ACFT performance data. You can view summaries, demographic breakdowns,
        event-level performance, participation analysis, and trends.

        By default, the app loads **acft_demo.csv**, but you can also upload another dataset.
        """)
        uploaded = st.file_uploader("Upload a CSV dataset", type=["csv"])
        if uploaded:
            df = pd.read_csv(uploaded)
            df.rename(columns=col_map, inplace=True)
            st.success("Dataset uploaded and applied.")
        if df is not None:
            st.dataframe(df.head())

    elif df is not None:
        if page == "Overview":
            st.title("Dataset Overview")
            st.write(df.describe(include="all"))

        elif page == "Demographic Breakdown":
            st.title("Demographic Breakdown")
            st.write("### Distribution by Sex")
            st.bar_chart(df["Sex"].value_counts())
            st.write("### Distribution by MOS")
            st.bar_chart(df["MOS"].value_counts().head(20))

        elif page == "Event Performance":
            st.title("Event Performance")
            event_cols = [
                "Deadlift (lbs)", "Standing Power Throw (m)", "Hand Release Push-ups",
                "Sprint-Drag-Carry (sec)", "2-Mile Run (sec)", "Plank (sec)", "Alt Aerobic (sec)"
            ]
            event = st.selectbox("Select Event", event_cols)
            fig, ax = plt.subplots()
            sns.histplot(df[event], kde=True, ax=ax)
            st.pyplot(fig)

        elif page == "Participation Analysis":
            st.title("Participation Analysis")
            not_attempted = [
                "Deadlift Not Attempted", "Plank Not Attempted", "Power Throw Not Attempted",
                "Push-up Not Attempted", "Sprint Not Attempted"
            ]
            st.bar_chart(df[not_attempted].sum())

        elif page == "Score Trends":
            st.title("Score Trends")

            if "Test Date" in df.columns:
                df["Test Date"] = pd.to_datetime(df["Test Date"])
                df = df.sort_values("Test Date")

        # Date range selector
                min_date = df["Test Date"].min()
                max_date = df["Test Date"].max()
                start_date, end_date = st.date_input(
                    "Select timeframe",
                    [min_date, max_date],
                    min_value=min_date,
                    max_value=max_date
        )

        # Apply filter
                mask = (df["Test Date"] >= pd.to_datetime(start_date)) & (df["Test Date"] <= pd.to_datetime(end_date))
                filtered_df = df.loc[mask]

                if filtered_df.empty:
                    st.warning("No data available in the selected timeframe.")
                else:
                    trend = filtered_df.groupby("Test Date")["Total Score"].mean()
                    st.line_chart(trend)
            else:
                st.warning("Test Date column not available.")


if __name__ == "__main__":
    main()
