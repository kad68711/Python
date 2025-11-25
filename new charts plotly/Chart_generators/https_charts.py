import urllib.parse
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

def detailed_http_charts(incident_type, subset, charts_by_type):
    http_df = subset.copy()

    # helper to extract root (scheme + netloc), e.g. "https://chatgpt.com"
    def get_root_url(url):
        if not url or pd.isna(url):
            return None
        url = str(url).strip()
        # if value looks like multiple recipients, we won't handle here; caller will split
        # ensure scheme is present for parsing
        if not (url.startswith("http://") or url.startswith("https://")):
            url_to_parse = "http://" + url
        else:
            url_to_parse = url
        try:
            p = urllib.parse.urlparse(url_to_parse)
            if p.netloc:
                # include scheme to be explicit (https/http)
                return f"{p.scheme}://{p.netloc}".lower()
            else:
                return None
        except Exception:
            return None

    # ----- Chart 1: Top Senders -----
    if "Sender" in http_df.columns:
        top_senders = http_df["Sender"].value_counts().reset_index()
        top_senders.columns = ["Sender", "Count"]

        top_senders = top_senders.head(50)  # ✅ Limit to Top 50 senders

        fig_top_http_senders = px.bar(
            top_senders,
            x="Sender",
            y="Count",
            title="Senders for (HTTP/HTTPS)",
            text="Count",
            color="Sender"
        )
        fig_top_http_senders.update_traces(textposition='outside')

        addlayout(fig_top_http_senders)

        charts_by_type[incident_type].append(create_chart_div(fig_top_http_senders))
       

        # preserve sender order
        sender_order = top_senders["Sender"].tolist()
    else:
        sender_order = []

    # ----- Chart 2: Senders mapped to Root Website (stacked, preserve Chart1 order) -----
    if "Sender" in http_df.columns and "Recipient" in http_df.columns:
        # Build (Sender, RootURL) exploded list
        exploded = []
        for _, row in http_df.iterrows():
            sender = row.get("Sender")
            rec_field = row.get("Recipient")
            if pd.isna(rec_field):
                continue
            # recipients may be comma-separated
            for r in str(rec_field).split(","):
                r = r.strip()
                root = get_root_url(r)
                if root:
                    exploded.append((sender, root))

        if exploded:
            sd_df = pd.DataFrame(exploded, columns=["Sender", "RootURL"])
            sd_counts = sd_df.groupby(["Sender", "RootURL"]).size().reset_index(name="Count")

            sd_counts = (
            sd_counts.groupby("Sender")
            .apply(lambda g: g.nlargest(5, "Count"))
            .reset_index(drop=True)
        )

            # Force sender order same as chart 1
            if sender_order:
                sd_counts["Sender"] = pd.Categorical(sd_counts["Sender"], categories=sender_order, ordered=True)
                sd_counts = sd_counts.sort_values("Sender")

            fig_sender_websites = px.bar(
                sd_counts,
                x="Sender",
                y="Count",
                color="Sender",
                title="Senders mapped to top 5 websites",
                text="RootURL",
                category_orders={"Sender": sender_order}
            )
            fig_sender_websites.update_traces(textposition='outside')

            

            addlayout(fig_sender_websites)

            charts_by_type[incident_type].append(create_chart_div(fig_sender_websites))
            

    # ----- Chart 3: Senders → Incident (sum) -----
    if "Incident Match Count" in http_df.columns and "Sender" in http_df.columns:
        sender_incident_counts = (
            http_df.groupby("Sender")["Incident Match Count"]
            .sum()
            .reset_index()
            .sort_values("Incident Match Count", ascending=False)
            .head(50)  # ✅ Top 50 senders by incident count
        )

        # Use same slider/appearance
        fig_sender_incidents_http = px.bar(
            sender_incident_counts,
            x="Sender",
            y="Incident Match Count",
            text="Incident Match Count",
            color="Sender",
            title="Senders mapped to Incident Match Count"
        )
        fig_sender_incidents_http.update_traces(textposition='outside')

        # If desired, preserve sender_order too (optional). Here we rely on incident order.
        addlayout(fig_sender_incidents_http)

        charts_by_type[incident_type].append(create_chart_div(fig_sender_incidents_http))
      

    # ----- Chart 4: Top Recipients (strip to root first) -----
    if "Recipient" in http_df.columns:
        all_roots = []
        for rec_field in http_df["Recipient"].dropna():
            for r in str(rec_field).split(","):
                root = get_root_url(r.strip())
                if root:
                    all_roots.append(root)

        if all_roots:
            root_counts = pd.Series(all_roots).value_counts().reset_index()
            root_counts.columns = ["RootURL", "Count"]

            root_counts = root_counts.head(50)  # ✅ Top 50 recipient root domains

            fig_top_root_recipients = px.bar(
                root_counts,
                x="RootURL",
                y="Count",
                title="Top Recipient Websites",
                text="Count",
                color="RootURL"
            )
            fig_top_root_recipients.update_traces(textposition='outside')

            addlayout(fig_top_root_recipients)

            charts_by_type[incident_type].append(create_chart_div(fig_top_root_recipients))
            

            # preserve domain order for later BU→domain chart
            domain_order = root_counts["RootURL"].tolist()
        else:
            domain_order = []

    # ----- Chart 5: Unique Senders per Business Unit -----
    if "Business Unit" in http_df.columns and "Sender" in http_df.columns:
        unique_senders_by_bu = (
            http_df.groupby("Business Unit")["Sender"]
            .nunique()
            .reset_index(name="UniqueSenders")
            .sort_values("UniqueSenders", ascending=False)
            .head(50)  # ✅ Top 50 BUs by unique senders
        )

        fig_unique_senders_bu = px.bar(
            unique_senders_by_bu,
            x="Business Unit",
            y="UniqueSenders",
            title="Unique Senders per Business Unit ",
            text="UniqueSenders",
            color="Business Unit"
        )
        fig_unique_senders_bu.update_traces(textposition='outside')

        addlayout(fig_unique_senders_bu)

        charts_by_type[incident_type].append(create_chart_div(fig_unique_senders_bu))
        

    # ----- Chart 6: Business Unit → Incident Sum -----
    if "Business Unit" in http_df.columns and "Incident Match Count" in http_df.columns:
        bu_incident_counts = (
            http_df.groupby("Business Unit")["Incident Match Count"]
            .sum()
            .reset_index(name="TotalIncidentMatches")
            .sort_values("TotalIncidentMatches", ascending=False)
            .head(50)  # ✅ Top 50 BUs by total incidents
        )

        fig_bu_incidents = px.bar(
            bu_incident_counts,
            x="Business Unit",
            y="TotalIncidentMatches",
            title="Incident Match Counts per Business Unit",
            text="TotalIncidentMatches",
            color="Business Unit"
        )
        fig_bu_incidents.update_traces(textposition='outside')

        addlayout(fig_bu_incidents)

        charts_by_type[incident_type].append(create_chart_div(fig_bu_incidents))
       

    # ----- Chart 7: Business Unit → Recipient Root (stacked) -----
    # ----- Chart 7: Business Unit → Recipient Root (stacked, using defined BU order) -----
    if "Business Unit" in http_df.columns and "Recipient" in http_df.columns:
        exploded_bu = []
        for _, row in http_df.iterrows():
            bu = row["Business Unit"]
            rec_field = row["Recipient"]
            if pd.isna(rec_field):
                continue
            for r in str(rec_field).split(","):
                root = get_root_url(r.strip())
                if root:
                    exploded_bu.append((bu, root))

        if exploded_bu:
            bu_root_df = pd.DataFrame(exploded_bu, columns=["Business Unit", "RootURL"])
            bu_root_counts = (
                bu_root_df.groupby(["Business Unit", "RootURL"]).size().reset_index(name="Count")
            )

             # --- 🔹 Keep only the Top 5 RootURLs per Business Units ---
            bu_root_counts = (
            bu_root_counts.groupby("Business Unit")
            .apply(lambda g: g.nlargest(5, "Count"))
            .reset_index(drop=True)
        )

            # --- Define Business Unit order from previous incident count chart ---
            bu_order = bu_incident_counts["Business Unit"].tolist()  # from Chart 6
            bu_root_counts["Business Unit"] = pd.Categorical(
                bu_root_counts["Business Unit"], categories=bu_order, ordered=True
            )
            bu_root_counts = bu_root_counts.sort_values("Business Unit")

            fig_bu_root = px.bar(
                bu_root_counts,
                x="Business Unit",
                y="Count",
                color="Business Unit",
                title="Business Units mapped to Recipient Websites",
                text="RootURL"
            )
            fig_bu_root.update_traces(textposition='outside')

            addlayout(fig_bu_root,'stack')

            charts_by_type[incident_type].append(create_chart_div(fig_bu_root))
            

        

    # ----- Chart 8: Policy Pie -----
    if "Policy" in http_df.columns:
        policy_counts = http_df["Policy"].value_counts().reset_index()
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
            title="Policies Triggered for Http/Https",
            margin=dict(l=20, r=20, t=40, b=20),
            width=1100,
            height=600,
        )
        charts_by_type[incident_type].append(create_chart_div(fig_policy))
