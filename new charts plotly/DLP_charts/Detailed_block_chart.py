import pandas as pd
from Chart_generators.generic_charts import generic_charts
from Chart_generators.email_charts import detailed_email_charts
from Chart_generators.application_charts import detailed_application_charts
from Chart_generators.https_charts import detailed_http_charts
from Chart_generators.print_charts import detailed_print_charts
from Chart_generators.copy_to_networkShare import detailed_networkshare_charts
from Chart_generators.removableStorage_charts import detailed_usb_charts
from Chart_generators.CloudStorage_charts import detailed_cloudstorage_charts
from Chart_generators.FTP_charts import detailed_ftp_charts

df = pd.read_excel("all_block_data.xlsx")

def detailed_block_data_charts():

    # -----------------------------
    # GENERIC CHARTS
    # -----------------------------

    generic_block_charts=generic_charts(df)
    generic_chart_notes=["Block Channels",
                           """
    <ul>
      <li>Network- This includes data blocked at one of our proxies via which the data is
routed, this includes http/https and email data.</li>
      <li>Endpoint- This includes the data that was blocked at the Endpoint device itself, this
includes application blocks, usb, Bluetooth, Print etc.</li>
    </ul>
    """,
                         "Overall policies triggered"]
    
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
    known_types = ["Email/SMTP", "Application File Access","HTTP/HTTPS", "Printer/Fax" ,"Removable Storage","Copy to Network Share","Cloud Storage","FTP"]
    

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
      <li>Top 50 senders blocked from sending data outside</li>
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
                detailed_email_charts(incident_type, subset,charts_by_type)

                 # Consolidate charts + notes
                charts_by_type_withnotes[incident_type] = [
                    {"html": chart_html, "note": note_text} 
                    for chart_html, note_text in zip(charts_by_type[incident_type], email_notes)
                ]

            # ---------------------------
            # APPLICATION FILE ACCESS
            # ---------------------------
            if incident_type == "Application File Access":

                application_notes = [
    """
    <ul>
      <li>Shows the proportion of file access incidents across different applications</li>
      <li>msedgewebview2.exe - It is a system component that that allows windows applications
like teams, office apps etc. to use embedded web technologies, so applications like teams
and other Microsoft applications are flagged here.</li>
      <li>fsquirt.exe - It is used for Bluetooth File Transfer Operations in windows.</li>
      
    </ul>
    """,
    """
    <ul>
      <li>Top 50 senders involved in file access incidents</li>
      <li>This includes users trying to send sensitive data via applications like teams , Bluetooth ,
and other applications on the endpoint.</li>
      <li>Doesn’t include HTTP/HTTPS and SMTP applications whose data passes via proxy.</li>
      <li>Scroll to view more</li>
    </ul>
    """,
    """
    <ul>
      <li>Shows which applications are being used by Top 50 senders for file access</li>
      <li>Scroll to view more senders</li>
    </ul>
    """,
    """
    <ul>
      <li>Top 50 Total incident match count per sender for file access events</li>
      <li>Incident match count- Example if a user sends uploads a file or data with 100 credit card
numbers the incident count is 100.</li>
      <li>The incident match count and the top senders can differ because a person can send only 1
file or send data once but that single file/ data upload can contain large amounts of
sensitive information leading to a higher incident match count.</li>
      <li>Scroll to view more senders</li>
    </ul>
    """,
    """
    <ul>
      <li>Displays how many unique senders exist in Top 50 business unit for file access activities</li>
    </ul>
    """,
    """
    <ul>
      <li>Shows total incident match counts per business unit</li>
      <li>Sorted by Top 50 incidents first</li>
    </ul>
    """,
    """
    <ul>
      <li>Shows which applications are used across different business units</li>
      <li>Stacked by application type</li>
      <li>TOP 50 departments here are the ones that have maximum instances of application use ,
hence order can differ from the incidents generated and the no. of people in that
department.</li>
      <li>Top 50 scroll to view all</li>
    </ul>
    """,
    """
    <ul>
      <li>Shows distribution of policies triggered in file access incidents</li>
      
    </ul>
    """
]

                detailed_application_charts(incident_type, subset, charts_by_type)

                # Consolidate charts + notes
                charts_by_type_withnotes[incident_type] = [
                    {"html": chart_html, "note": note_text} 
                    for chart_html, note_text in zip(charts_by_type[incident_type], application_notes)
                ]
            # ---------------------------
            # HTTP/HTTPS TYPE
            # ---------------------------
            if incident_type == "HTTP/HTTPS":

                http_notes = [
    """
    <ul>
      <li>Top 50 senders for HTTP/HTTPS incidents</li>
      <li>Use slider to view more</li>
    </ul>
    """,
    """
    <ul>
      <li>Shows Top 5 websites each sender is contacting </li>
    </ul>
    """,
    """
    <ul>
      <li>Sum of incident match counts per sender for HTTP/HTTPS incidents</li>
      <li>Incident match count- Example if a user sends data / uploads a file with 100 credit card
numbers the incident count is 100.</li>
<li>The incident match count and the top senders can differ because a person can send only 1
file but that single file can contain large amounts of sensitive information leading to a
higher incident match count.</li>
    </ul>
    """,
    """
    <ul>
      <li>Top 50 recipient websites</li>
      <li>Use slider to view more</li>
    </ul>
    """,
    """
    <ul>
      <li>Number of unique senders in each Business Unit (HTTP/HTTPS)</li>
      <li>Ordered by Top 50</li>
    </ul>
    """,
    """
    <ul>
      <li>Total incident match counts aggregated per Business Unit (HTTP/HTTPS)</li>
      <li>Ordered by Top 50</li>
    </ul>
    """,
    """
    <ul>
      <li>Business Units vs Websites accessed</li>
      <li>Business Units ordered as per incident counts from previous chart</li>
    </ul>
    """,
    """
    <ul>
      <li>Policies triggered distribution for HTTP/HTTPS incidents</li>
      
    </ul>
    """
]
                detailed_http_charts( incident_type, subset, charts_by_type)

                # Consolidate charts + notes
                charts_by_type_withnotes[incident_type] = [
                    {"html": chart_html, "note": note_text} 
                    for chart_html, note_text in zip(charts_by_type[incident_type], http_notes)
                ]

            # ---------------------------
            # Print TYPE
            # ---------------------------
            if incident_type == "Printer/Fax":

                print_notes = [
    """
    <ul>
      <li>Shows top to print senders with total counts</li>
      <li>Use the slider to view more senders</li>
    </ul>
    """,
    """
    <ul>
      <li>Displays total incident match counts per print sender</li>
      
      <li>Example if a user sends a file with 100 credit card numbers the
incident count is 100.</li>
      <li>The incident match count and the top senders can differ because a person can send only 1
file but that single file can contain large amounts of sensitive information leading to a
higher incident match count.s</li>
<li>Use the slider to view more senders</li>
    </ul>
    """,
    """
    <ul>
      <li>Displays number of unique senders in each business unit for print incidents</li>
      <li>Sorted by Top 50</li>
    </ul>
    """,
    """
    <ul>
      <li>Shows total incident matches per business unit for print incidents</li>
      <li>Sorted by Top 50</li>
    </ul>
    """,
    """
    <ul>
      <li>Policies triggered distribution for print incidents</li>
      
    </ul>
    """
]
                detailed_print_charts( incident_type, subset, charts_by_type)

                # Consolidate charts + notes
                charts_by_type_withnotes[incident_type] = [
                    {"html": chart_html, "note": note_text} 
                    for chart_html, note_text in zip(charts_by_type[incident_type], print_notes)
                ]

            # ---------------------------
            # Copy To Networkshare
            # ---------------------------
            if incident_type == "Copy to Network Share":

                copytonetowrkShare_notes = [
    """
    <ul>
      <li>Top 50 senders associated with Copy to Network Share incidents</li>
      <li>Use the slider below to view more senders</li>
    </ul>
    """,
    """
    <ul>
      <li>Shows total incident match counts per sender</li>
      <li>Example: if a user copies a single file containing 200 sensitive entries, the match count is 200</li>
      <li>The total incident match count and top senders can differ because one file can contain multiple sensitive entries, resulting in higher match counts</li>
      <li>Use the slider to view more senders</li>
    </ul>
    """,
    """
    <ul>
      <li>Displays the number of unique senders in each Business Unit</li>
      <li>Sorted by Top 50 active Business Units</li>
      <li>Scroll to view additional Business Units</li>
    </ul>
    """,
    """
    <ul>
      <li>Shows total incident match counts aggregated per Business Unit</li>
      <li>Sorted by Top 50 highest incident counts</li>
      <li>Scroll to view more Business Units</li>
    </ul>
    """,
    """
    <ul>
      <li>Policies triggered distribution for Copy to Network Share incidents</li>
    </ul>
    """
]

                detailed_networkshare_charts( incident_type, subset, charts_by_type)

                # Consolidate charts + notes
                charts_by_type_withnotes[incident_type] = [
                    {"html": chart_html, "note": note_text} 
                    for chart_html, note_text in zip(charts_by_type[incident_type], copytonetowrkShare_notes)
                ]


            # ---------------------------
            # Removable Storage
            # ---------------------------
            if incident_type == "Removable Storage":

                usb_notes = [
    """
    <ul>
      <li>Shows top 50 USB senders with total counts</li>
      <li>Use the slider to view more senders</li>
    </ul>
    """,
    """
    <ul>
      <li>Displays total incident match counts per USB sender</li>
      <li>Example: if a user transfers one file containing 100 sensitive entries, the match count is 100</li>
      <li>The incident match count and sender count can differ as one file may hold multiple sensitive data matches</li>
      <li>Use the slider to explore more senders</li>
    </ul>
    """,
    """
    <ul>
      <li>Displays number of unique senders in each Business Unit for USB incidents</li>
      <li>Sorted by Top 50</li>
    </ul>
    """,
    """
    <ul>
      <li>Shows total incident matches per Business Unit for USB incidents</li>
      <li>Sorted by Top 50</li>
    </ul>
    """,
    """
    <ul>
      <li>Policies triggered distribution for USB incidents</li>
    </ul>
    """
]

                detailed_usb_charts( incident_type, subset, charts_by_type)

                  # Consolidate charts + notes
                charts_by_type_withnotes[incident_type] = [
                    {"html": chart_html, "note": note_text} 
                    for chart_html, note_text in zip(charts_by_type[incident_type], usb_notes)
                ]


            # ---------------------------
            # CloudStorage
            # ---------------------------
            if incident_type == "Cloud Storage":

                cloudstorage_notes = [
    """
    <ul>
      <li>Shows 50 top Cloud Storage senders with total counts</li>
      <li>Use the slider to view more senders</li>
    </ul>
    """,
    """
    <ul>
      <li>Displays total incident match counts per Cloud Storage sender</li>
      <li>Example: if a user uploads one file containing 300 sensitive entries, the match count is 300</li>
      <li>The total incident match count and sender count can differ because one upload can contain multiple sensitive entries</li>
      <li>Sorted in descending order; use the slider to explore more senders</li>
    </ul>
    """,
    """
    <ul>
      <li>Displays number of unique senders in each Business Unit for Cloud Storage incidents</li>
      <li>Sorted by Top 50</li>
    </ul>
    """,
    """
    <ul>
      <li>Shows total incident matches per Business Unit for Cloud Storage incidents</li>
      <li>Sorted by Top 50 highest incident counts</li>
    </ul>
    """,
    """
    <ul>
      <li>Policies triggered distribution for Cloud Storage incidents</li>
    </ul>
    """
]

                detailed_cloudstorage_charts(incident_type, subset, charts_by_type)

                # Consolidate charts + notes
                charts_by_type_withnotes[incident_type] = [
                    {"html": chart_html, "note": note_text} 
                    for chart_html, note_text in zip(charts_by_type[incident_type], cloudstorage_notes)
                ]

            # ---------------------------
            # FTP
            # ---------------------------
            if incident_type == "FTP":

                ftp_notes = [
    """
    <ul>
      <li>Shows top 50 FTP senders with total counts</li>
      <li>Use the slider to view more senders</li>
    </ul>
    """,
    """
    <ul>
      <li>Displays total incident match counts per FTP sender</li>
      <li>Example: if a user uploads a file with 150 sensitive entries, the incident match count is 150</li>
      <li>The incident match count and sender count can differ because a single transfer can contain multiple sensitive matches</li>
      <li>Sorted in descending order; use the slider to explore more senders</li>
    </ul>
    """,
    """
    <ul>
      <li>Displays number of unique senders in each Business Unit for FTP incidents</li>
      <li>Sorted by Top 50</li>
    </ul>
    """,
    """
    <ul>
      <li>Shows total incident matches per Business Unit for FTP incidents</li>
      <li>Sorted by Top 50</li>
    </ul>
    """,
    """
    <ul>
      <li>Policies triggered distribution for FTP incidents</li>
    </ul>
    """
]

                detailed_ftp_charts(incident_type, subset, charts_by_type)

                # Consolidate charts + notes
                charts_by_type_withnotes[incident_type] = [
                    {"html": chart_html, "note": note_text} 
                    for chart_html, note_text in zip(charts_by_type[incident_type], ftp_notes)
                ]


             
        else:
            continue
 

    
    return generic_block_charts_withnotes,charts_by_type_withnotes
