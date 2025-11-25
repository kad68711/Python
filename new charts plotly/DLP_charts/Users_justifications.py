import pandas as pd
import plotly.graph_objects as go

def create_chart_div(fig):
    """
    Converts a Plotly figure to HTML without annotations.
    """
    return fig.to_html(full_html=False, include_plotlyjs='inline',config={"displaylogo": False})



# =======================
# User Justification Table
# =======================
def justifications_chart():
    justification_chart={}

    # Read data
    df = pd.read_excel("dummy_data.xlsx")  # change to your actual file name

    # Clean column names
    df.columns = [col.strip() for col in df.columns]

    # Select only needed columns
    cols_to_display = [
        "Sr no.",
        "ID",
        "Sender",
        "Policy",
        "Incident Match Count",
        "User Justification"
    ]
    df = df[cols_to_display]

    

    # Define header and values
    header = list(df.columns)
    values = [df[col] for col in df.columns]

    # Create Plotly table
    fig_user_table = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=header,
                    fill_color="#CDE4F7",
                    align="left",
                    font=dict(size=13, color="black", family="Arial Bold"),
                ),
                cells=dict(
                    values=values,
                    fill_color=[["#FFFFFF", "#F9F9F9"] * (len(df) // 2 + 1)],  # alternate row colors
                    align="left",
                    font=dict(size=12, color="black", family="Arial"),
                ),
            )
        ]
    )

    

    fig_user_table.update_layout(
        title="User Justification Summary",
        
        height= 900,
        margin=dict(l=50, r=50, t=60, b=30),
    )

    # Convert to HTML (consistent with other charts)
    justification_chart["User_Justification_Table"] = create_chart_div(fig_user_table)

    justification_chart_withnotes = {

        "User_Justification_Table": {
            "html": justification_chart["User_Justification_Table"],
            "note": "User justificaitions for incidents"
        }}

    return justification_chart_withnotes