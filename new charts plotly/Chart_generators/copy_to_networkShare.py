import plotly.express as px
import plotly.graph_objects as go

def create_chart_div(fig):
    """
    Converts a Plotly figure to HTML without annotations.
    """
    return fig.to_html(full_html=False, include_plotlyjs='inline',config={"displaylogo": False})

# below design only for bar chart not for pie charts
def addlayout(fig,barmode='relative'):
    fig.update_layout(
    width=1100,
    height=600,
    margin=dict(l=50, r=50, t=40, b=10),
    autosize=False,                 # ✅ Prevent Plotly from resizing canvas
    dragmode='pan',                 # Enable pan interaction (keeps layout fixed)
    xaxis=dict(
        tickangle=45,
        range=[-0.5, 9.5],
        fixedrange=False,           # Allow horizontal pan
        constrain='domain',         # Prevent aspect ratio distortion
        rangeslider=dict(
            visible=True,
            thickness=0.05,          # Slider height as fraction of plot area
            bgcolor="rgba(200,200,200,0.15)",
            bordercolor="rgba(0,0,0,0)"
        )
    ),
    yaxis=dict(
        fixedrange=True,             # ✅ Prevent vertical auto-zooming
        automargin=True
    ),

    barmode=barmode,
    
)


def detailed_networkshare_charts(incident_type, subset, charts_by_type):
    df = subset.copy()

    # --- Chart 1: Top Senders (Scrollable View) ---
    top_senders = df["Sender"].value_counts().reset_index()
    top_senders.columns = ["Sender", "Count"]
    top_senders = top_senders.head(50)  # ✅ Top 50

    fig_top_senders = px.bar(
        top_senders,
        x="Sender",
        y="Count",
        title="Senders to a shared folder on Network",
        text="Count",
        color="Sender"
    )
    fig_top_senders.update_traces(textposition="outside")

    addlayout(fig_top_senders)

    charts_by_type[incident_type].append(create_chart_div(fig_top_senders))

    # --- Chart 2: Senders vs Incident Match Count (Scrollable View) ---
    if "Incident Match Count" in df.columns:
        sender_incident_counts = (
            df.groupby("Sender")["Incident Match Count"]
            .sum()
            .reset_index()
            .sort_values("Incident Match Count", ascending=False)
            .head(50)  # ✅ Top 50
        )

        fig_sender_incidents = px.bar(
            sender_incident_counts,
            x="Sender",
            y="Incident Match Count",
            text="Incident Match Count",
            color="Sender",
            title="Senders mapped to Incident Match Count"
        )
        fig_sender_incidents.update_traces(textposition='outside')
        addlayout(fig_sender_incidents)

        charts_by_type[incident_type].append(create_chart_div(fig_sender_incidents))

    # --- Chart 3: Unique Senders per Business Unit ---
    if "Business Unit" in df.columns:
        unique_senders_df = (
            df.groupby("Business Unit")["Sender"]
            .nunique()
            .reset_index()
            .rename(columns={"Sender": "Unique Senders"})
            .sort_values(by="Unique Senders", ascending=False)
            .head(50)  # ✅ Top 50
        )

        fig_unique_senders = px.bar(
            unique_senders_df,
            x="Business Unit",
            y="Unique Senders",
            title="Unique Senders per Business Unit",
            text="Unique Senders",
            color="Business Unit",
        )
        fig_unique_senders.update_traces(textposition="outside")
        addlayout(fig_unique_senders)

        charts_by_type[incident_type].append(create_chart_div(fig_unique_senders))

    # --- Chart 4: Business Unit vs Incident Match Counts (Scrollable View) ---
    if "Business Unit" in df.columns and "Incident Match Count" in df.columns:
        incident_counts_df = (
            df.groupby("Business Unit")["Incident Match Count"]
            .sum()
            .reset_index()
            .rename(columns={"Incident Match Count": "Total Incident Matches"})
            .sort_values(by="Total Incident Matches", ascending=False)
            .head(50)  # ✅ Top 50
        )

        fig_incident_counts = px.bar(
            incident_counts_df,
            x="Business Unit",
            y="Total Incident Matches",
            title="Incident Match Counts per Business Unit",
            text="Total Incident Matches",
            color="Business Unit",
        )
        fig_incident_counts.update_traces(textposition="outside")
        
        addlayout(fig_incident_counts)

        charts_by_type[incident_type].append(create_chart_div(fig_incident_counts))

    # ----- Chart 8: Policy Pie -----
    if "Policy" in df.columns:
        policy_counts = df["Policy"].value_counts().reset_index()
        policy_counts.columns = ["Policy", "Count"]

        # Ensure plain Python types
        labels = policy_counts["Policy"].astype(str).tolist()
        values = policy_counts["Count"].astype(int).tolist()

        # Use graph_objects Treemap instead of Plotly Express
        fig_policy = go.Figure(go.Treemap(
            labels=labels,
            parents=[""] * len(labels),  # no hierarchy, flat structure
            values=values,
            textinfo="label+value+percent entry",
            marker=dict(colors=values, colorscale="OrRd"),  # changed color
        ))

        fig_policy.update_layout(
            title="Policies Triggered for Copy to NetworkShare",
            margin=dict(l=20, r=20, t=40, b=20),
            width=1100,
            height=600,
        )
        charts_by_type[incident_type].append(create_chart_div(fig_policy))
