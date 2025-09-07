# ACFT Data Analysis Dashboard

## Purpose
This project provides an interactive dashboard to analyze Army Combat Fitness Test (ACFT) data. The goal is to help commanders, analysts, and trainers:
- Understand overall performance trends.
- Compare performance across demographics (sex, rank, MOS).
- Evaluate event-specific results.
- Identify participation gaps (events not attempted).
- Track changes in scores over time.

By using this tool, leaders can make data-driven decisions about training, readiness, and resource allocation.

## Features
- **Dataset Overview**: View sample data and missing values.
- **Descriptive Statistics**: Summary stats for all numeric fields (raw scores and event scores).
- **Demographic Breakdown**: Compare total scores by sex, rank category, and MOS.
- **Event Performance**: Explore average scores and distributions across events, broken down by sex.
- **Participation Analysis**: Identify which events soldiers did not attempt.
- **Score Trends**: Visualize changes in average total scores over time.

## Requirements
- Python 3.8+
- Dependencies listed in `requirements.txt`:
  ```txt
  pandas
  matplotlib
  seaborn
  streamlit
  ```

## Installation
1. Clone this repository or download the project files.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place your ACFT dataset (CSV format) in the project folder.

## Usage
Run the Streamlit app:
```bash
streamlit run acft_analysis.py
```

- Upload your CSV dataset when prompted.
- Navigate through the sections of the dashboard to explore data insights.

## Example Dataset Headers
The dataset should include columns such as:
```
soldier_acft_id,test_date,uic,mos,sex,rank,rank_category,pay_grade,age_at_test,
test_type,profile,raw_plank,raw_strength_deadlift,raw_standing_power_throw,
raw_hand_release_push_up,raw_sprint_drag_carry,raw_2mi_run,raw_alt_aerobic,
plank_score,strength_deadlift_score,alt_aerobic_event,standing_power_throw_score,
hand_release_push_up_score,sprint_drag_carry_score,2mi_run_score,alt_aerobic_score,
total_score,test_status,deadlift_not_attempted,plank_not_attempted,
power_throw_not_attempted,pushup_not_attempted,sprint_not_attempted
```

## Output
- Interactive tables and plots within the Streamlit UI.
- Insights into soldier performance and training readiness.

---

### Author
Created to support ACFT readiness analysis and data-driven decision-making.
