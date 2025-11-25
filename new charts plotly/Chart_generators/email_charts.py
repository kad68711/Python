import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def create_chart_div(fig):
    """
    Converts a Plotly figure to HTML without annotations.
    """
    return fig.to_html(full_html=False, include_plotlyjs='inline',config={"displaylogo": False})


# --- Helper function to filter out @bajajal* and @bajajge*(internal) recipients ---
def filter_internal_recipients(recipient_series):
    filtered = []
    for r in recipient_series:
        if pd.isna(r):
            continue
        for email in str(r).split(','):
            email = email.strip().lower()
            if email and ('@bajajal' not in email and '@bajajge' not in email):
                filtered.append(email)
    return filtered

# below design only for bar chart not for pie charts


def addlayout(fig, barmode='relative'):
    fig.update_layout(
        width=1100,
        height=600,
        margin=dict(l=50, r=50, t=40, b=10),
        autosize=False,                 # ✅ Prevent Plotly from resizing canvas
        # Enable pan interaction (keeps layout fixed)
        dragmode='pan',
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


def detailed_email_charts(incident_type, subset, charts_by_type,return_last_chart=True):

    email_df = subset.copy()

    if "Sender" in email_df.columns:
        # --- Chart 1: Top Senders with Slider ---
        top_senders = email_df["Sender"].value_counts(
        ).reset_index()
        top_senders.columns = ["Sender", "Count"]

        top_senders = top_senders.head(50)  # ✅ Only top 50 senders

        fig_top_senders = px.bar(
            top_senders,
            x="Sender",
            y="Count",
            title="Email Senders",
            text="Count",
            color="Sender"
        )
        fig_top_senders.update_traces(textposition='outside')

        # ✨ Only 10 visible at a time with range slider (scroll-like)

        addlayout(fig_top_senders)

        charts_by_type[incident_type].append(
            create_chart_div(fig_top_senders))

        # --- Chart 2: Senders mapped to Domains (Stacked & Scrollable) ---
        if "Recipient" in email_df.columns:
            def extract_domains(recipient):
                domains = []
                for r in str(recipient).split(','):
                    r = r.strip()
                    if '@' in r:
                        domains.append(r.split('@')[-1].lower())
                return domains

            # Build sender → domain mapping
            # Build sender → domain mapping with filtered recipients
            exploded = []
            for _, row in email_df.iterrows():
                sender = row["Sender"]
                recipients_filtered = filter_internal_recipients(
                    [row["Recipient"]])
                domains = []
                for rec in recipients_filtered:
                    domains.extend(extract_domains(rec))
                for d in domains:
                    exploded.append((sender, d))

            sender_domain_df = pd.DataFrame(
                exploded, columns=["Sender", "Domain"])

            sender_domain_counts = (
                sender_domain_df.groupby(["Sender", "Domain"])
                .size()
                .reset_index(name="Count")
            )

            # --- Use sender order from Chart 1 (top_senders) ---
            # Ensure you already have `top_senders` DataFrame from Chart 1
            sender_order = top_senders["Sender"].tolist()

            # Keep only those senders that appear in Chart 1
            sender_domain_counts = sender_domain_counts[
                sender_domain_counts["Sender"].isin(sender_order)
            ]

            # Apply Chart 1 ordering
            sender_domain_counts["Sender"] = pd.Categorical(
                sender_domain_counts["Sender"],
                categories=sender_order,
                ordered=True
            )
            sender_domain_counts = sender_domain_counts.sort_values("Sender")

           # Compute top 5 domains *per sender*
            sender_domain_counts = (
                sender_domain_counts.groupby("Sender")
                .apply(lambda g: g.nlargest(5, "Count"))
                .reset_index(drop=True)
            )

            fig_sender_domains = px.bar(
                sender_domain_counts,
                x="Sender",
                y="Count",
                color="Sender",
                title="Senders Mapped to top 5 Outside Recipient Domains",
                text="Domain",
                category_orders={"Sender": sender_order}
            )

            fig_sender_domains.update_traces(
                textposition='outside')

            addlayout(fig_sender_domains, 'stack')

            charts_by_type[incident_type].append(
                create_chart_div(fig_sender_domains))

            # --- Chart 3: Senders vs Incident Match Count ---
        if "Incident Match Count" in email_df.columns:
            sender_incident_counts = (
                email_df.groupby("Sender")["Incident Match Count"]
                .sum()
                .reset_index()
                .sort_values("Incident Match Count", ascending=False)
            )

            sender_incident_counts = sender_incident_counts.head(
                50)  # ✅ Only top 50

            # Preserve sender order for next chart
            sender_order_for_unique_recipients = sender_incident_counts["Sender"].tolist(
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

            charts_by_type[incident_type].append(
                create_chart_div(fig_sender_incidents))

        # --- Chart 4: Senders vs Unique Recipients (Stacked & Ordered by Chart 3) ---
        if "Recipient" in email_df.columns:
            # no need to use below function as usecase is fulfillled other way
            # def extract_unique_recipients(recipient_series):
            #     recipients_list = []
            #     for r in recipient_series:
            #         if pd.isna(r):
            #             continue
            #         for email in str(r).split(','):
            #             email = email.strip().lower()
            #             if email:
            #                 recipients_list.append(email)
            #     return recipients_list

            # Build sender → unique recipients mapping
            exploded = []
            for _, row in email_df.iterrows():
                sender = row["Sender"]
                recipients_filtered = filter_internal_recipients(
                    [row["Recipient"]])
                for rec in recipients_filtered:
                    exploded.append((sender, rec))

            sender_recipient_df = pd.DataFrame(
                exploded, columns=["Sender", "Recipient"])
            unique_recipient_counts = (
                sender_recipient_df.groupby("Sender")["Recipient"]
                .nunique()
                .reset_index(name="UniqueRecipientCount")
            )

            # --- Keep top 50 senders based on UniqueRecipientCount ---
            # --- Use sender order from Chart 3 (sender_incident_counts) ---
            sender_order = sender_incident_counts["Sender"].tolist()

            # Keep only those senders that appear in Chart 3
            unique_recipient_counts = unique_recipient_counts[
                unique_recipient_counts["Sender"].isin(sender_order)
            ]

            # Apply Chart 3 ordering
            unique_recipient_counts["Sender"] = pd.Categorical(
                unique_recipient_counts["Sender"],
                categories=sender_order,
                ordered=True
            )
            unique_recipient_counts = unique_recipient_counts.sort_values(
                "Sender")

            fig_sender_unique_recips = px.bar(
                unique_recipient_counts,
                x="Sender",
                y="UniqueRecipientCount",
                title="Senders mapped to Unique Recipient Count",
                text="UniqueRecipientCount",
                color="Sender"
            )
            fig_sender_unique_recips.update_traces(textposition='outside')

            addlayout(fig_sender_unique_recips)

            charts_by_type[incident_type].append(
                create_chart_div(fig_sender_unique_recips))
            
            # --- Chart 4.1: Senders with Exactly One Unique Recipient (sorted by Incident Match Count) ---
            if "Sender" in email_df.columns and "Recipient" in email_df.columns and "Incident Match Count" in email_df.columns:
                # Build sender → recipient mapping (filtered)
                exploded = []
                for _, row in email_df.iterrows():
                    sender = row["Sender"]
                    recipients_filtered = filter_internal_recipients([row["Recipient"]])
                    incident_count = row["Incident Match Count"]
                    for rec in recipients_filtered:
                        exploded.append((sender, rec, incident_count))

                sender_recipient_df = pd.DataFrame(exploded, columns=["Sender", "Recipient", "Incident Match Count"])

                # Compute unique recipients per sender
                unique_recipient_counts = (
                    sender_recipient_df.groupby("Sender")["Recipient"]
                    .nunique()
                    .reset_index(name="UniqueRecipientCount")
                )

                # Filter senders with exactly one unique recipient
                single_recipient_senders = unique_recipient_counts[unique_recipient_counts["UniqueRecipientCount"] == 1]

                # Merge back to get the actual recipient and incident counts
                sender_single_recipient = sender_recipient_df.merge(single_recipient_senders[["Sender"]], on="Sender")

                # Get the one recipient per sender
                sender_recipient_names = (
                    sender_single_recipient.groupby("Sender")["Recipient"]
                    .first()
                    .reset_index()
                )

                # Sum up total incident counts for those senders
                sender_incident_sum = (
                    sender_single_recipient.groupby("Sender")["Incident Match Count"]
                    .sum()
                    .reset_index()
                )

                # Combine recipient names and total incidents
                merged_single_recipient_data = pd.merge(sender_incident_sum, sender_recipient_names, on="Sender")
                merged_single_recipient_data = pd.merge(merged_single_recipient_data, single_recipient_senders, on="Sender")


                # Sort descending by total incident count
                merged_single_recipient_data = merged_single_recipient_data.sort_values(
                    "Incident Match Count", ascending=False
                )

                # Limit to top 50 (optional)
                merged_single_recipient_data = merged_single_recipient_data.head(50)

                # Create the chart
                fig_single_recipient = px.bar(
                    merged_single_recipient_data,
                    x="Sender",
                    y="UniqueRecipientCount",
                    text="UniqueRecipientCount",
                    color="Sender",
                    title="Senders with Exactly One Unique Outside Recipient (Sorted by Incident Match Count)",
                    hover_data={
                        "Incident Match Count": True,
                        "Recipient": True,
                        "UniqueRecipientCount":False
                    }
                )

                fig_single_recipient.update_traces(textposition="outside")

                addlayout(fig_single_recipient)
                charts_by_type[incident_type].append(create_chart_div(fig_single_recipient))


            # --- Chart 5: Top Recipients (Scrollable View) ---
            if "Recipient" in email_df.columns:
                def extract_all_recipients(recipient_series):
                    recipients = []
                    for r in recipient_series:
                        if pd.isna(r):
                            continue
                        for email in str(r).split(','):
                            email = email.strip().lower()
                            if email:
                                recipients.append(email)
                    return recipients

                # Flatten all recipients
                initial_recipients = extract_all_recipients(
                    email_df["Recipient"])
                all_recipients = filter_internal_recipients(initial_recipients)

                recipient_counts = (
                    pd.Series(all_recipients)
                    .value_counts()
                    .reset_index()
                )
                recipient_counts.columns = ["Recipient", "Count"]
                recipient_counts = recipient_counts.head(50)  # ✅

                fig_top_recipients = px.bar(
                    recipient_counts,
                    x="Recipient",
                    y="Count",
                    title="Top Recipients",
                    text="Count",
                    color="Recipient"
                )
                fig_top_recipients.update_traces(textposition='outside')

                addlayout(fig_top_recipients)

                charts_by_type[incident_type].append(
                    create_chart_div(fig_top_recipients))

            # --- Chart 6: Domains by Unique Recipients (Scrollable View) ---
            if "Recipient" in email_df.columns:
                def extract_recipient_domain(email):
                    if '@' in email:
                        return email.split('@')[-1].lower()
                    return None

                # Reuse exploded recipient list
                recipient_domain_data = []
                for r in all_recipients:
                    domain = extract_recipient_domain(r)
                    if domain:
                        recipient_domain_data.append((r, domain))

                recipient_domain_df = pd.DataFrame(
                    recipient_domain_data, columns=["Recipient", "Domain"])

                domain_unique_counts = (
                    recipient_domain_df.groupby("Domain")["Recipient"]
                    .nunique()
                    .reset_index(name="UniqueRecipients")
                    .sort_values("UniqueRecipients", ascending=False)
                )
                domain_unique_counts = domain_unique_counts.head(50)  # ✅

                fig_domain_unique = px.bar(
                    domain_unique_counts,
                    x="Domain",
                    y="UniqueRecipients",
                    title="Domains by Unique Recipient Count",
                    text="UniqueRecipients",
                    color="Domain"
                )
                fig_domain_unique.update_traces(textposition='outside')

                addlayout(fig_domain_unique)

                charts_by_type[incident_type].append(
                    create_chart_div(fig_domain_unique))

                # --- Chart 7: Most Used Recipient Domains ---
                if "Recipient" in email_df.columns:
                    def extract_domains(recipient):
                        domains = []
                        for r in str(recipient).split(','):
                            r = r.strip()
                            if '@' in r:
                                domains.append(r.split('@')[-1].lower())
                        return domains

                    # Collect all domains from all recipients
                    all_domains = []
                    for rec in filter_internal_recipients(email_df["Recipient"]):
                        all_domains.extend(extract_recipient_domain(rec) for rec in [
                                           rec] if extract_recipient_domain(rec))

                    domain_counts = pd.Series(
                        all_domains).value_counts().reset_index()
                    domain_counts.columns = ["Domain", "Count"]

                    domain_counts = domain_counts.head(50)  # ✅

                    fig_most_used_domains = px.bar(
                        domain_counts,
                        x="Domain",
                        y="Count",
                        text="Count",
                        color="Domain",
                        title="Most Used Outside Recipient Domains"
                    )
                    fig_most_used_domains.update_traces(textposition='outside')

                    addlayout(fig_most_used_domains)

                    charts_by_type[incident_type].append(
                        create_chart_div(fig_most_used_domains))

                    # Preserve domain order for chart 8
                    domain_order = domain_counts["Domain"].tolist()

                # --- Chart 8: Business Units vs Recipient Domains (Stacked) ---
                if "Business Unit" in email_df.columns and "Recipient" in email_df.columns:
                    exploded = []
                    for _, row in email_df.iterrows():
                        dept = row["Business Unit"]
                        recipients_filtered = filter_internal_recipients([row["Recipient"]])
                        domains = []
                        for rec in recipients_filtered:
                            domains.extend(
                                extract_recipient_domain(rec) for rec in [rec] if extract_recipient_domain(rec)
                            )
                        for d in domains:
                            exploded.append((dept, d))

                    dept_domain_df = pd.DataFrame(exploded, columns=["Business Unit", "Domain"])

                    dept_domain_counts = (
                        dept_domain_df.groupby(["Domain", "Business Unit"])
                        .size()
                        .reset_index(name="Count")
                    )

                    # ✅ Keep only domains from Chart 7
                    dept_domain_counts = dept_domain_counts[dept_domain_counts["Domain"].isin(domain_order)]

                    # ✅ Assign same order as Chart 7
                    dept_domain_counts["Domain"] = pd.Categorical(
                        dept_domain_counts["Domain"], categories=domain_order, ordered=True
                    )
                    dept_domain_counts = dept_domain_counts.sort_values("Domain")

                    # ✅ Keep only top 5 Business Units per Domain
                    dept_domain_counts = (
                        dept_domain_counts.groupby("Domain", group_keys=False)
                        .apply(lambda g: g.nlargest(5, "Count"))
                        .reset_index(drop=True)
                    )

                    fig_dept_domains = px.bar(
                        dept_domain_counts,
                        x="Domain",
                        y="Count",
                        color="Domain",
                        title="Most used Outside domains mapped to top 5 Business Units using them",
                        text="Business Unit",
                        category_orders={"Domain": domain_order}
                    )
                    fig_dept_domains.update_traces(textposition='outside')

                    addlayout(fig_dept_domains, 'stack')
                    charts_by_type[incident_type].append(create_chart_div(fig_dept_domains))


                # Chart 9: Unique Senders per Business Unit (sorted descending)
                unique_senders_df = (
                    subset.groupby("Business Unit")["Sender"]
                    .nunique()
                    .reset_index()
                    .rename(columns={"Sender": "Unique Senders"})
                    .sort_values(by="Unique Senders", ascending=False)
                )

                unique_senders_df = unique_senders_df.head(50)

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

                charts_by_type[incident_type].append(
                    create_chart_div(fig_unique_senders))

                # Chart 10: Incident Match Counts per Business Unit (sorted descending)
                incident_counts_df = (
                    subset.groupby("Business Unit")["Incident Match Count"]
                    .sum()
                    .reset_index()
                    .rename(columns={"Incident Match Count": "Total Incident Matches"})
                    .sort_values(by="Total Incident Matches", ascending=False)
                )

                incident_counts_df = incident_counts_df.head(50)

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

                charts_by_type[incident_type].append(
                    create_chart_div(fig_incident_counts))
                    
                # skip the last charts for exempted users and complianceid 
                if return_last_chart:

                    # --- Chart 11: Policies Triggered Treemap ---
                    if "Policy" in email_df.columns:
                        
                        policy_counts = email_df["Policy"].value_counts().reset_index()
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
                            title="Policies Triggered for Email",
                            margin=dict(l=20, r=20, t=40, b=20),
                            width=1100,
                            height=600,
                        )

                        charts_by_type[incident_type].append(create_chart_div(fig_policy))


