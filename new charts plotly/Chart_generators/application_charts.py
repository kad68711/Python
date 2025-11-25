import plotly.express as px
import pandas as pd
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

def detailed_application_charts(incident_type, subset, charts_by_type):
    app_df = subset.copy()

    # --- Chart 1: Application Distribution (Pie Chart) ---
    if "Endpoint Application Name" in app_df.columns:
        fig_app_pie = px.pie(
            app_df,
            names="Endpoint Application Name",
            title="Application Usage Distribution",
            
        )

        fig_app_pie.update_layout(
                                
                                width=1100,
                                height=600,
                                margin=dict(l=50, r=50, t=40, b=10),
                            )

        # Show both percentage and count
        fig_app_pie.update_traces(
            textinfo='percent+value',
            textfont_size=14
        )

        charts_by_type[incident_type].append(create_chart_div(fig_app_pie))
       

    # --- Chart 2: Top Senders (Scrollable Bar) ---
    if "Sender" in app_df.columns:
        top_app_senders = app_df["Sender"].value_counts().reset_index()
        top_app_senders.columns = ["Sender", "Count"]

        # ✅ Keep only top 50 senders
        top_app_senders = top_app_senders.head(50)

        fig_top_app_senders = px.bar(
            top_app_senders,
            x="Sender",
            y="Count",
            title="Senders triggering for Application file access ",
            text="Count",
            color="Sender"
        )
        fig_top_app_senders.update_traces(textposition='outside')

        addlayout(fig_top_app_senders)

        charts_by_type[incident_type].append(create_chart_div(fig_top_app_senders))
       

    # --- Chart 3: Senders Mapped to Applications (Stacked) ---
    if "Sender" in app_df.columns and "Endpoint Application Name" in app_df.columns:
        sender_app_counts = (
            app_df.groupby(["Sender", "Endpoint Application Name"])
            .size()
            .reset_index(name="Count")
        )

        sender_order = top_app_senders["Sender"].tolist()
        sender_app_counts["Sender"] = pd.Categorical(
            sender_app_counts["Sender"], categories=sender_order, ordered=True
        )
        sender_app_counts = sender_app_counts.sort_values("Sender")

        fig_sender_apps = px.bar(
            sender_app_counts,
            x="Sender",
            y="Count",
            color="Endpoint Application Name",
            title="Senders Mapped to Applications used",
            text="Endpoint Application Name",
            category_orders={"Sender": sender_order}
        )
        fig_sender_apps.update_traces(textposition='outside')

        # ✅ Auto-scale y-axis to max data value necessary othewise the bars become too small
        max_y = sender_app_counts["Count"].max()
        fig_sender_apps.update_yaxes(range=[0, max_y * 1.1])

        addlayout(fig_sender_apps,'stack')

        charts_by_type[incident_type].append(create_chart_div(fig_sender_apps))
        

    # --- Chart 4: Senders vs Incident Match Count ---
    if "Incident Match Count" in app_df.columns:
        sender_incident_counts = (
            app_df.groupby("Sender")["Incident Match Count"]
            .sum()
            .reset_index()
            .sort_values("Incident Match Count", ascending=False)
            .head(50)  # ✅ Limit to top 50
        )

        fig_sender_incidents = px.bar(
            sender_incident_counts,
            x="Sender",
            y="Incident Match Count",
            text="Incident Match Count",
            color="Sender",
            title="Senders mapped to Incident Match Count "
        )
        fig_sender_incidents.update_traces(textposition='outside')

        addlayout(fig_sender_incidents)

        charts_by_type[incident_type].append(create_chart_div(fig_sender_incidents))
      

    # --- Chart 5: Unique Senders per Business Unit ---
    if "Business Unit" in app_df.columns and "Sender" in app_df.columns:
        unique_senders_per_dept = (
            app_df.groupby("Business Unit")["Sender"]
            .nunique()
            .reset_index(name="UniqueSenders")
            .sort_values("UniqueSenders", ascending=False)
            .head(50)  # ✅ optional
        )

        fig_unique_senders = px.bar(
            unique_senders_per_dept,
            x="Business Unit",
            y="UniqueSenders",
            title="Unique Senders per Business Unit",
            text="UniqueSenders",
            color="Business Unit"
        )
        fig_unique_senders.update_traces(textposition='outside')

        addlayout(fig_unique_senders)

        charts_by_type[incident_type].append(create_chart_div(fig_unique_senders))
        

    # --- Chart 6: Department Incident Counts ---
    if "Business Unit" in app_df.columns and "Incident Match Count" in app_df.columns:
        dept_incident_counts = (
            app_df.groupby("Business Unit")["Incident Match Count"]
            .sum()
            .reset_index()
            .sort_values("Incident Match Count", ascending=False)
            .head(50)  # ✅ optional
        )

        fig_dept_incidents = px.bar(
            dept_incident_counts,
            x="Business Unit",
            y="Incident Match Count",
            title="Business Unit mapped to Incident Match Count",
            text="Incident Match Count",
            color="Business Unit"
        )
        fig_dept_incidents.update_traces(textposition='outside')

        addlayout(fig_dept_incidents)

        charts_by_type[incident_type].append(create_chart_div(fig_dept_incidents))
        

    # --- Chart 7: Business Units Mapped to Applications (Stacked Bar) ---
    if "Business Unit" in app_df.columns and "Endpoint Application Name" in app_df.columns:
        dept_app_counts = (
            app_df.groupby(["Business Unit", "Endpoint Application Name"])
            .size()
            .reset_index(name="Count")
            .sort_values("Count", ascending=False)
            .head(50)  # ✅ optional
        )

        dept_app_counts = dept_app_counts.sort_values("Count", ascending=False)

        fig_dept_apps = px.bar(
            dept_app_counts,
            x="Business Unit",
            y="Count",
            color="Endpoint Application Name",
            title="Business Units Mapped to Application used",
            text="Endpoint Application Name"
        )
        fig_dept_apps.update_traces(textposition='outside')

        addlayout(fig_dept_apps,'stack')

        charts_by_type[incident_type].append(create_chart_div(fig_dept_apps))
        

    # --- Chart 8: Policies Triggered (Pie Chart) ---
    if "Policy" in app_df.columns:
        policy_counts = app_df["Policy"].value_counts().reset_index()
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
            title="Policies Triggered Distribution for Application File Access",
            margin=dict(l=20, r=20, t=40, b=20),
            width=1100,
            height=600,
        )

        charts_by_type[incident_type].append(create_chart_div(fig_policy))
       
