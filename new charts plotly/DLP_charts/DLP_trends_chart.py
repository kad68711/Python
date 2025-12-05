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
        """
    <ul>
      <li>Combined trend showing overall, network, and endpoint incidents over time.</li>
      <li>Network trend includes traffic that passed through network proxies like http/https and email.</li>
      <li>Endpoint trend includes usb, copy to network share, upload to application, print and so on.</li>
    </ul>
    """,
        "Monthly Trends for DLP includes both network and enpoint incidents", 
                        "Network trend includes traffic that passed through network proxies like http/https and email",
                        "Endpoint trend includes usb, copy to network share, upload to application, print and so on.",
                         "Protocol trends showing SMTP, HTTP/HTTPS, PRINT/FAX, and Removable Storage traffic",
                        "Monthly DLP severity distribution showing counts of high, medium, and low incidents."]
    
    trends_block_charts_withnotes = {

     "Combined_Channel_Trend": {
        "html": trends_charts["Combined_Trend"],
        "note": trends_chart_notes[0]
    },

    # "Monthly_trend": {
    #     "html": trends_charts["Monthly_trend"],
    #     "note": trends_chart_notes[1]
    # },
    # "Monthly_Networktrend": {
    #     "html": trends_charts["Monthly_Networktrend"],
    #     "note": trends_chart_notes[2]
    # },
    # "Monthly_Endpointtrend": {
    #     "html": trends_charts["Monthly_Endpointtrend"],
    #     "note": trends_chart_notes[3]
    # },
    "Protocol_Trend": {
    "html": trends_charts["Protocol_Trend"],
    "note": trends_chart_notes[4]
},

        "Monthly_Severity_Table": {
        "html": trends_charts["Monthly_Severity_Table"],
        "note": trends_chart_notes[5]
    },
}

    return trends_block_charts_withnotes
    


def DLP_trends():

    trends_charts={}

    # --- Combined Overall, Network, and Endpoint Trend ---

    df = pd.read_excel("dlp_trends.xlsx")

    # Clean column names
    df.columns = [c.strip() for c in df.columns]

    # Ensure month order
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)
    df = df.sort_values("Month")

    # Reshape into long format
    # We convert:
    # Endpoint Incidents | Network Incidents | Overall Incidents
    # into a column called Source and a column called No. of Incidents
    df_long = df.melt(
        id_vars="Month",
        value_vars=["Endpoint Incidents", "Network Incidents", "Overall Incidents"],
        var_name="Source",
        value_name="No. of Incidents"
    )

    # Make the labels nicer
    df_long["Source"] = df_long["Source"].str.replace(" Incidents", "")

    # --- Create combined line chart ---
    fig_combined = px.line(
        df_long,
        x="Month",
        y="No. of Incidents",
        color="Source",
        title=" DLP Channel Trends (Network + Endpoint + Overall) - 2025",
        markers=True,
    )

    # Add labels above each marker
    fig_combined.for_each_trace(
        lambda trace: trace.update(
            text=df_long.loc[df_long["Source"] == trace.name, "No. of Incidents"],
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


    # =======================
    # PROTOCOL TRENDS CHART
    # =======================

    # Read the protocol trends file
    df_protocol = pd.read_excel("protocol_trends.xlsx")

    # Clean column names
    df_protocol.columns = [c.strip() for c in df_protocol.columns]

    # Ensure month order
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    df_protocol["Month"] = pd.Categorical(df_protocol["Month"], categories=month_order, ordered=True)
    df_protocol = df_protocol.sort_values("Month")

    # Melt into long format
    df_protocol_long = df_protocol.melt(
        id_vars="Month",
        value_vars=["SMTP", "HTTP/HTTPS", "PRINT/FAX", "REMOVABLE STORAGE"],
        var_name="Protocol",
        value_name="No. of Incidents"
    )

    # Create line chart
    fig_protocol = px.line(
        df_protocol_long,
        x="Month",
        y="No. of Incidents",
        color="Protocol",
        title="Protocol Trends - 2025",
        markers=True,
    )

    # Annotate values
    fig_protocol.for_each_trace(
        lambda trace: trace.update(
            text=df_protocol_long.loc[df_protocol_long["Protocol"] == trace.name, "No. of Incidents"],
            textposition="top center",
            mode="lines+markers+text"
        )
    )

    fig_protocol.update_layout(
        xaxis=dict(tickangle=45),
        width=1100,
        height=600,
        margin=dict(l=50, r=50, t=40, b=80),
    )

    # Add to return dict
    trends_charts["Protocol_Trend"] = create_chart_div(fig_protocol)





    ##########################################

    #separate charts for monthly trends commented incase needed afterwards
        
    #####################################



    # # MOnthyl trend
   
    # df = pd.read_excel("dlp_trends.xlsx")

    # # Ensure proper column names (adjust if needed)
    # df.columns = [col.strip() for col in df.columns]
    # if "Month" not in df.columns or "No. of Incidents" not in df.columns:
    #     raise ValueError("Excel must contain 'Month' and 'No. of Incidents' columns")

    # # Sort months chronologically if possible
    # # This assumes months are full names like 'January', 'February', etc.
    # month_order = [
    #     "January", "February", "March", "April", "May", "June",
    #     "July", "August", "September", "October", "November", "December"
    # ]
    # df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)
    # df = df.sort_values("Month")

    # # --- Create the Timeline Chart ---
    # fig_timeline = px.line(
    #     df,
    #     x="Month",
    #     y="No. of Incidents",
    #     title="Overall DLP Incident Trends Over Time 2025",
    #     markers=True,
    # )

    # # Annotate each point with the number of incidents
    # fig_timeline.update_traces(
    #     mode="lines+markers+text",
    #     text=df["No. of Incidents"],
    #     textposition="top center",
    #     line=dict(width=3),
    # )

    # # --- Layout styling similar to your existing charts ---
    # fig_timeline.update_layout(
    #     xaxis=dict(
    #         tickangle=45,
            
    #     ),
    #     width=1100,
    #     height=600,
    #     margin=dict(l=50, r=50, t=40, b=80),
    # )

    # trends_charts["Monthly_trend"]=create_chart_div(fig_timeline)

    # # Monthyl endpoint incident trend

    # df = pd.read_excel("dlp_endpointtrends.xlsx")

    # # Ensure proper column names (adjust if needed)
    # df.columns = [col.strip() for col in df.columns]
    # if "Month" not in df.columns or "No. of Incidents" not in df.columns:
    #     raise ValueError("Excel must contain 'Month' and 'No. of Incidents' columns")

    # # Sort months chronologically if possible
    # # This assumes months are full names like 'January', 'February', etc.
    # month_order = [
    #     "January", "February", "March", "April", "May", "June",
    #     "July", "August", "September", "October", "November", "December"
    # ]
    # df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)
    # df = df.sort_values("Month")

    # # --- Create the Timeline Chart ---
    # fig_timeline = px.line(
    #     df,
    #     x="Month",
    #     y="No. of Incidents",
    #     title="DLP Endpoint Incident Trends Over Time 2025",
    #     markers=True,
    # )

    # # Annotate each point with the number of incidents
    # fig_timeline.update_traces(
    #     mode="lines+markers+text",
    #     text=df["No. of Incidents"],
    #     textposition="top center",
    #     line=dict(width=3),
    # )

    # # --- Layout styling similar to your existing charts ---
    # fig_timeline.update_layout(
    #     xaxis=dict(
    #         tickangle=45,
            
    #     ),
    #     width=1100,
    #     height=600,
    #     margin=dict(l=50, r=50, t=40, b=80),
    # )

    # trends_charts["Monthly_Endpointtrend"]=create_chart_div(fig_timeline)


    # # Monthyl network incident trend

    # df = pd.read_excel("dlp_networktrends.xlsx")

    # # Ensure proper column names (adjust if needed)
    # df.columns = [col.strip() for col in df.columns]
    # if "Month" not in df.columns or "No. of Incidents" not in df.columns:
    #     raise ValueError("Excel must contain 'Month' and 'No. of Incidents' columns")

    # # Sort months chronologically if possible
    # # This assumes months are full names like 'January', 'February', etc.
    # month_order = [
    #     "January", "February", "March", "April", "May", "June",
    #     "July", "August", "September", "October", "November", "December"
    # ]
    # df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)
    # df = df.sort_values("Month")

    # # --- Create the Timeline Chart ---
    # fig_timeline = px.line(
    #     df,
    #     x="Month",
    #     y="No. of Incidents",
    #     title="DLP Network Incident Trends Over Time 2025",
    #     markers=True,
    # )

    # # Annotate each point with the number of incidents
    # fig_timeline.update_traces(
    #     mode="lines+markers+text",
    #     text=df["No. of Incidents"],
    #     textposition="top center",
    #     line=dict(width=3),
    # )

    # # --- Layout styling similar to your existing charts ---
    # fig_timeline.update_layout(
    #     xaxis=dict(
    #         tickangle=45,
            
    #     ),
    #     width=1100,
    #     height=600,
    #     margin=dict(l=50, r=50, t=40, b=80),
    # )

    # trends_charts["Monthly_Networktrend"]=create_chart_div(fig_timeline)


    

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
