import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def create_chart_div(fig):
    """
    Converts a Plotly figure to HTML without annotations.
    """
    return fig.to_html(full_html=False, include_plotlyjs='inline',config={"displaylogo": False})

def DLP_trends_charts():
    trends_charts=DLP_trends()
    trends_chart_notes=[
        "Combined trend showing overall, network, and endpoint incidents over time",
        "Monthly Trends for DLP includes both network and enpoint incidents", 
                        "Network trend includes traffic that passed through network proxies like http/https and email",
                        "Endpoint trend includes usb, copy to network share, upload to application, print and so on.",
                        "Monthly DLP severity distribution showing counts of high, medium, and low incidents."]
    
    trends_block_charts_withnotes = {

     "Combined_Trend": {
        "html": trends_charts["Combined_Trend"],
        "note": trends_chart_notes[0]
    },

    "Monthly_trend": {
        "html": trends_charts["Monthly_trend"],
        "note": trends_chart_notes[1]
    },
    "Monthly_Networktrend": {
        "html": trends_charts["Monthly_Networktrend"],
        "note": trends_chart_notes[2]
    },
    "Monthly_Endpointtrend": {
        "html": trends_charts["Monthly_Endpointtrend"],
        "note": trends_chart_notes[3]
    },
        "Monthly_Severity_Table": {
        "html": trends_charts["Monthly_Severity_Table"],
        "note": trends_chart_notes[4]
    },
}

    return trends_block_charts_withnotes
    


def DLP_trends():

    trends_charts={}

        # --- Combined Overall, Network, and Endpoint Trend ---
    df_overall = pd.read_excel("dlp_trends.xlsx")
    df_network = pd.read_excel("dlp_networktrends.xlsx")
    df_endpoint = pd.read_excel("dlp_endpointtrends.xlsx")

    # Clean column names
    for d in [df_overall, df_network, df_endpoint]:
        d.columns = [col.strip() for col in d.columns]

    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    # Add a Source column to each
    df_overall["Source"] = "Overall"
    df_network["Source"] = "Network"
    df_endpoint["Source"] = "Endpoint"

    # Combine all
    combined_df = pd.concat([df_overall, df_network, df_endpoint], ignore_index=True)

    # Ensure month order
    combined_df["Month"] = pd.Categorical(combined_df["Month"], categories=month_order, ordered=True)
    combined_df = combined_df.sort_values("Month")

    # --- Create combined line chart ---
    fig_combined = px.line(
        combined_df,
        x="Month",
        y="No. of Incidents",
        color="Source",
        title="Overall DLP Trends (Network + Endpoint + Overall) - 2025",
        markers=True,
    )

    fig_combined.for_each_trace(
    lambda trace: trace.update(
        text=combined_df.loc[combined_df["Source"] == trace.name, "No. of Incidents"],
        textposition="top center",
        mode="lines+markers+text"
    )
)
    
    fig_combined.update_layout(
        xaxis=dict(tickangle=45),
        width=1100,
        height=600,
        margin=dict(l=50, r=50, t=40, b=80),
    )

    trends_charts["Combined_Trend"] = create_chart_div(fig_combined)


    # MOnthyl trend
   
    df = pd.read_excel("dlp_trends.xlsx")

    # Ensure proper column names (adjust if needed)
    df.columns = [col.strip() for col in df.columns]
    if "Month" not in df.columns or "No. of Incidents" not in df.columns:
        raise ValueError("Excel must contain 'Month' and 'No. of Incidents' columns")

    # Sort months chronologically if possible
    # This assumes months are full names like 'January', 'February', etc.
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)
    df = df.sort_values("Month")

    # --- Create the Timeline Chart ---
    fig_timeline = px.line(
        df,
        x="Month",
        y="No. of Incidents",
        title="Overall DLP Incident Trends Over Time 2025",
        markers=True,
    )

    # Annotate each point with the number of incidents
    fig_timeline.update_traces(
        mode="lines+markers+text",
        text=df["No. of Incidents"],
        textposition="top center",
        line=dict(width=3),
    )

    # --- Layout styling similar to your existing charts ---
    fig_timeline.update_layout(
        xaxis=dict(
            tickangle=45,
            
        ),
        width=1100,
        height=600,
        margin=dict(l=50, r=50, t=40, b=80),
    )

    trends_charts["Monthly_trend"]=create_chart_div(fig_timeline)

    # Monthyl endpoint incident trend

    df = pd.read_excel("dlp_endpointtrends.xlsx")

    # Ensure proper column names (adjust if needed)
    df.columns = [col.strip() for col in df.columns]
    if "Month" not in df.columns or "No. of Incidents" not in df.columns:
        raise ValueError("Excel must contain 'Month' and 'No. of Incidents' columns")

    # Sort months chronologically if possible
    # This assumes months are full names like 'January', 'February', etc.
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)
    df = df.sort_values("Month")

    # --- Create the Timeline Chart ---
    fig_timeline = px.line(
        df,
        x="Month",
        y="No. of Incidents",
        title="DLP Endpoint Incident Trends Over Time 2025",
        markers=True,
    )

    # Annotate each point with the number of incidents
    fig_timeline.update_traces(
        mode="lines+markers+text",
        text=df["No. of Incidents"],
        textposition="top center",
        line=dict(width=3),
    )

    # --- Layout styling similar to your existing charts ---
    fig_timeline.update_layout(
        xaxis=dict(
            tickangle=45,
            
        ),
        width=1100,
        height=600,
        margin=dict(l=50, r=50, t=40, b=80),
    )

    trends_charts["Monthly_Endpointtrend"]=create_chart_div(fig_timeline)


    # Monthyl network incident trend

    df = pd.read_excel("dlp_networktrends.xlsx")

    # Ensure proper column names (adjust if needed)
    df.columns = [col.strip() for col in df.columns]
    if "Month" not in df.columns or "No. of Incidents" not in df.columns:
        raise ValueError("Excel must contain 'Month' and 'No. of Incidents' columns")

    # Sort months chronologically if possible
    # This assumes months are full names like 'January', 'February', etc.
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)
    df = df.sort_values("Month")

    # --- Create the Timeline Chart ---
    fig_timeline = px.line(
        df,
        x="Month",
        y="No. of Incidents",
        title="DLP Network Incident Trends Over Time 2025",
        markers=True,
    )

    # Annotate each point with the number of incidents
    fig_timeline.update_traces(
        mode="lines+markers+text",
        text=df["No. of Incidents"],
        textposition="top center",
        line=dict(width=3),
    )

    # --- Layout styling similar to your existing charts ---
    fig_timeline.update_layout(
        xaxis=dict(
            tickangle=45,
            
        ),
        width=1100,
        height=600,
        margin=dict(l=50, r=50, t=40, b=80),
    )

    trends_charts["Monthly_Networktrend"]=create_chart_div(fig_timeline)


    

    # =======================
    # Add Severity Table
    # =======================

    df = pd.read_excel("dlp_severity_table.xlsx")  # <-- file with Month, High, Medium, Low

    # Ensure month order
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)
    df = df.sort_values("Month")

    # Prepare table data
    header = ["Month", "High", "Medium", "Low"]
    values = [df["Month"], df["High"], df["Medium"], df["Low"]]

    # Define color coding for cells (column-based)
    cell_colors = []
    for col in header:
        if col == "High":
            cell_colors.append(["#FFCCCC"] * len(df))  # light red
        elif col == "Medium":
            cell_colors.append(["#FFD3B3"] * len(df))  # light orange
        elif col == "Low":
            cell_colors.append(["#FCFFCC"] * len(df))  # light yellow
        else:
            cell_colors.append(["white"] * len(df))  # Month column

    # Create Plotly table
    fig_table = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=header,
                    fill_color="#E5ECF6",
                    align="left",
                    font=dict(size=13, color="black"),
                ),
                cells=dict(
                    values=values,
                    fill_color=cell_colors,
                    align="left",
                    font=dict(size=12, color="black"),
                ),
            )
        ]
    )

    fig_table.update_layout(
        title="Monthly DLP Severity Summary",
        width=1100,
        height=600,
        margin=dict(l=50, r=50, t=60, b=30),
    )

    # Convert to HTML
    trends_charts["Monthly_Severity_Table"] = create_chart_div(fig_table)


    return trends_charts
