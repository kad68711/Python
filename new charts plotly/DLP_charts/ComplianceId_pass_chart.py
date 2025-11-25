import pandas as pd
from Chart_generators.generic_charts import generic_charts
from Chart_generators.email_charts import detailed_email_charts


df = pd.read_excel("compliance_id_data.xlsx")

def complianceid_pass_data_charts():

    # -----------------------------
    # GENERIC CHARTS
    # -----------------------------

    generic_block_charts=generic_charts(df)
    generic_chart_notes=["Pass CHANNELS",
                         """
    <ul>
      <li>Network- This includes data at one of our proxies via which the data is
routed, this includes http/https and email data.</li>
      
    </ul>
    """,
                         "overall policies triggered"]
    
    generic_block_charts_withnotes = {
    "overall_block_type_pie": {
        "html": generic_block_charts["overall_block_type_pie"],
        "note": generic_chart_notes[0]
    },
    "overall_block_location_pie": {
        "html": generic_block_charts["overall_block_location_pie"],
        "note": generic_chart_notes[1]
    },
    "overall_Policies_triggered": {
        "html": generic_block_charts["overall_Policies_triggered"],
        "note": generic_chart_notes[2]
    }
}

    # -----------------------------
    # TYPE-SPECIFIC CHARTS
    # -----------------------------
    known_types = ["Email/SMTP"]
    

    charts_by_type_withnotes = {}
    charts_by_type={}
    
   

    for incident_type in known_types:
        if incident_type in df["Type"].dropna().unique():
            subset = df[df["Type"] == incident_type]
            charts_by_type[incident_type] = []
            

            # ---------------------------
            # EMAIL TYPE
            # ---------------------------
            if incident_type == "Email/SMTP":

                email_notes = [
    """
    <ul>
      <li>Top 50 senders successfully sending data outside by the use of compliance id.</li>
      <li>Use the slider below to view more senders</li>
    </ul>
    """,
    """
    <ul>
      <li>Top 50 senders mapped to top 5 recipient domains</li>
      <li>Use the slider to view more senders</li>
    </ul>
    """,
    """
    <ul>
      <li>Total incident match counts per Top 50 senders </li>
      <li>Incident match count- Example if a user sends an email or uploads a file with 100 credit
card numbers the incident count is 100.</li>
      <li>The incident match count and the top senders can differ because a person can send only 1
email but that single email can contain large amounts of sensitive information leading to a
higher incident match count.</li>
      <li>Use the slider to view more senders</li>
    </ul>
    """,
    """
    <ul>
      <li>Number of unique recipients per sender</li>
      <li>EXAMPLE USECASE-
If a person has a higher incident match count and the unique recipients count is just 1 for example.
This mean all that data is sent outside to a single recipient.</li>
      <li>Use slider to view more senders</li>
    </ul>
    """,

    """
    <ul>
      <li>Top 50 senders who have unique outside recipient as 1.</li>
      <li>Ordered by incindet match count.</li>
      <li>It is almost a 70% possibility that when unique recipient count is 1 that recipient is the users personal email id.</li>
    </ul>
    """,
    """
    <ul>
      <li>Top recipients by total email count</li>
      <li>Use the slider to view more recipients</li>
    </ul>
    """,
    """
    <ul>
      <li>Domains with the most unique recipients</li>
      <li>Use the slider to view more recipients</li>
    </ul>
    """,
    """
    <ul>
      <li>Shows the most frequently used recipient domains</li>
      <li>The count shown here reflects the number of times an external domain was used, not the
number of unique recipients within that domain.</li>
      <li>It is important to note that a domain with even a single recipient can be used multiple
times, resulting in a higher usage count. Therefore, the number of recipients associated
with a domain may differ from the total usage count displayed.</li>
      <li>Use the slider to explore all domains</li>
    </ul>
    """,
    """
    <ul>
      <li>Shows Top 5 Business Units are communicating with each domain</li>
      <li>Stacked by Business Unit</li>
      <li>Scroll to view more domains</li>
    </ul>
    """,
    """
    <ul>
      <li>Displays the number of unique senders in each Business Unit</li>
      <li>Sorted by Top 50 Business Unit activity</li>
      <li>Scroll to view additional Business Units</li>
    </ul>
    """,
    """
    <ul>
      <li>Shows total incident match counts aggregated per Business Unit</li>
      <li>Sorted by Top 50 incident counts</li>
      <li>Scroll to view more Business Units</li>
    </ul>
    """,
    """
    <ul>
      <li>Shows the distribution of policies triggered in Email incidents</li>
      
    </ul>
    """
]
                # detailed_email_charts should now return a list of HTML chart strings
                # also skip the last chart for exmpted users and compliance id
                detailed_email_charts(incident_type, subset,charts_by_type,return_last_chart=False)

                 # Consolidate charts + notes
                charts_by_type_withnotes[incident_type] = [
                    {"html": chart_html, "note": note_text} 
                    for chart_html, note_text in zip(charts_by_type[incident_type], email_notes)
                ]

            
             
        else:
            continue
 

    
    return generic_block_charts_withnotes,charts_by_type_withnotes
