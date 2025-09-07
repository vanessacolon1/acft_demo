import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os

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

# Load dataset
df = pd.read_csv("acft_demo.csv")
df.rename(columns=col_map, inplace=True)
df["Test Date"] = pd.to_datetime(df["Test Date"])

urlBase = None
if os.environ.get('AIDE_CONTAINER_URL_BASE'):
    urlBase = os.environ.get('AIDE_CONTAINER_URL_BASE')
    app = Dash(__name__, url_base_pathname=urlBase)
else:
    # Update this for your local dev environment
    app = Dash(__name__, requests_pathname_prefix="/project-1-workspace-1/dash-dev/")

server = app.server

# Layout
app.layout = html.Div([
    html.H1("Army Combat Fitness Test (ACFT) Data Explorer"),
    
    dcc.Tabs([
        dcc.Tab(label='Overview', children=[
            html.H2("Dataset Overview"),
            dash_table.DataTable(
                id='overview-table',
                columns=[{"name": i, "id": i} for i in df.describe(include="all").reset_index().columns],
                data=df.describe(include="all").reset_index().to_dict('records')
            )
        ]),
        
        dcc.Tab(label='Demographic Breakdown', children=[
            html.H2("Distribution by Sex"),
            dcc.Graph(
                figure=px.bar(df['Sex'].value_counts().reset_index(), x='index', y='Sex', labels={'index':'Sex','Sex':'Count'})
            ),
            html.H2("Distribution by MOS"),
            dcc.Graph(
                figure=px.bar(df['MOS'].value_counts().head(20).reset_index(), x='index', y='MOS', labels={'index':'MOS','MOS':'Count'})
            )
        ]),

        dcc.Tab(label='Event Performance', children=[
            html.H2("Event Performance"),
            dcc.Dropdown(
                id='event-dropdown',
                options=[{'label': c, 'value': c} for c in [
                    "Deadlift (lbs)", "Standing Power Throw (m)", "Hand Release Push-ups",
                    "Sprint-Drag-Carry (sec)", "2-Mile Run (sec)", "Plank (sec)", "Alt Aerobic (sec)"
                ]],
                value="Deadlift (lbs)"
            ),
            dcc.Graph(id='event-hist')
        ]),

        dcc.Tab(label='Participation Analysis', children=[
            html.H2("Participation Analysis"),
            dcc.Graph(
                figure=px.bar(df[[
                    "Deadlift Not Attempted", "Plank Not Attempted", "Power Throw Not Attempted",
                    "Push-up Not Attempted", "Sprint Not Attempted"
                ]].sum().reset_index(), x='index', y=0, labels={'index':'Event', 0:'Count'})
            )
        ]),

        dcc.Tab(label='Score Trends', children=[
            html.H2("Score Trends"),
            dcc.DatePickerRange(
                id='date-picker',
                start_date=df["Test Date"].min(),
                end_date=df["Test Date"].max(),
                min_date_allowed=df["Test Date"].min(),
                max_date_allowed=df["Test Date"].max()
            ),
            dcc.Graph(id='score-trend')
        ])
    ])
])

# Callbacks
@app.callback(
    Output('event-hist', 'figure'),
    Input('event-dropdown', 'value')
)
def update_event_hist(event):
    fig = px.histogram(df, x=event, nbins=30, marginal="box")
    return fig

@app.callback(
    Output('score-trend', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_score_trend(start_date, end_date):
    filtered_df = df[(df["Test Date"] >= start_date) & (df["Test Date"] <= end_date)]
    trend = filtered_df.groupby("Test Date")["Total Score"].mean().reset_index()
    fig = px.line(trend, x="Test Date", y="Total Score", markers=True)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
