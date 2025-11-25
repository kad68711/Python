import plotly.express as px
import plotly.graph_objects as go





def create_chart_div(fig):
    """
    Converts a Plotly figure to HTML without annotations.
    """
    return fig.to_html(full_html=False, include_plotlyjs='inline',config={"displaylogo": False})

def generic_charts(df):
    generic_charts = {}
   

    # -----------------------------
    # GENERIC CHARTS
    # -----------------------------
    if "Channel" in df.columns:
        channel_counts = df["Channel"].value_counts().reset_index()
        channel_counts.columns = ["Channel", "Count"]

        fig_channel = px.pie(
            channel_counts,
            names="Channel",
            values="Count",  # actual counts
            title="Location Distribution",
            
        )

       

        # Show both  percentages on the pie
        fig_channel.update_traces(textinfo='percent')

       

        generic_charts["overall_block_location_pie"] = create_chart_div(fig_channel)
        


    if "Type" in df.columns:
        type_counts = df["Type"].value_counts().reset_index()
        type_counts.columns = ["Type", "Count"]

        fig_type = px.pie(
            type_counts,
            names="Type",
            values="Count",  # actual counts
            title="Channel Distribution",
        )

      

        fig_type.update_traces(textinfo='percent')

        generic_charts["overall_block_type_pie"] = create_chart_div(fig_type)

    if "Policy" in df.columns:
        
        type_counts = df["Policy"].value_counts().reset_index()
        type_counts.columns = ["Policy", "Count"]

        # Ensure plain Python types
        labels = type_counts["Policy"].astype(str).tolist()
        values = type_counts["Count"].astype(int).tolist()

        # Use graph_objects Treemap instead of Plotly Express
        fig_type = go.Figure(go.Treemap(
            labels=labels,
            parents=[""] * len(labels),  # no hierarchy, flat structure
            values=values,
            textinfo="label+value+percent entry",
            marker=dict(colors=values, colorscale="OrRd"),
        ))

        fig_type.update_layout(
            title="Overall Policy Distribution",
            margin=dict(l=20, r=20, t=40, b=20),
            width=1100,
            height=600,
        )

        generic_charts["overall_Policies_triggered"] = create_chart_div(fig_type)

        

    return generic_charts