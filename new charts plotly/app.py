from flask import Flask, render_template, send_file
from DLP_charts.Detailed_block_chart import detailed_block_data_charts
from DLP_charts.PII_block_chart import detailed_PII_block_data_charts
from DLP_charts.ComplianceId_pass_chart import complianceid_pass_data_charts
from DLP_charts.ExemptedUsers_pass_chart import ExemptedUsers_pass_data_charts
from DLP_charts.Health_MotorRenewal_pass_chart import health_motor_renewal_pass_data_charts
from DLP_charts.DLP_trends_chart import DLP_trends_charts
from DLP_charts.Users_justifications import justifications_chart
import io

import base64
# because the icon cant isnt present when dashboard is generated
def get_favicon_base64():
    with open("static/logo.png", "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

app = Flask(__name__)


@app.route("/")
def index():

    # trends chart
    DLP_trends = DLP_trends_charts()

    # justification chart
    justification_chart = justifications_chart()    

    # all block data
    generic_block_charts, charts_by_blocktype = detailed_block_data_charts()

    # PII block data
    generic_PIIblock_charts, charts_by_PIIblocktype = detailed_PII_block_data_charts()

    # Complianceid pass data
    complianceid_generic_chart, complianceid_pass_data_chart = complianceid_pass_data_charts()

    # ExemptedUsers pass data
    exemptedusers_generic_chart, exemptedusers_pass_data_chart,exception_summary = ExemptedUsers_pass_data_charts()

    # Health & Motor Renewal pass data
    healthrenewal_generic_chart, healthrenewal_pass_data_chart = health_motor_renewal_pass_data_charts()

    return render_template(
        "index.html",

        showdownloadbutton=True,
        favicon_base64=get_favicon_base64(),


        # trends charts
        DLP_trends=DLP_trends,

         # justification chart
        justification_chart = justification_chart, 

        # block data
        generic_block_charts=generic_block_charts,
        charts_by_blocktype=charts_by_blocktype,

        # PII block data
        generic_PIIblock_charts=generic_PIIblock_charts,
        charts_by_PIIblocktype=charts_by_PIIblocktype,

        # Complianceid pass data
        complianceid_generic_chart=complianceid_generic_chart,
        complianceid_pass_data_chart=complianceid_pass_data_chart,

        # ExemptedUsers pass data
        exemptedusers_generic_chart=exemptedusers_generic_chart,
        exemptedusers_pass_data_chart=exemptedusers_pass_data_chart,
        exception_summary=exception_summary,

        # Health & Motor Renewal pass data
        healthrenewal_generic_chart=healthrenewal_generic_chart,
        healthrenewal_pass_data_chart=healthrenewal_pass_data_chart,


    )


@app.route("/download")
def download_dashboard():

    # trends chart
    DLP_trends = DLP_trends_charts()

     # justification chart
    justification_chart = justifications_chart()    

    # all block data
    generic_block_charts, charts_by_blocktype = detailed_block_data_charts()

    # PII block data
    generic_PIIblock_charts, charts_by_PIIblocktype = detailed_PII_block_data_charts()

    # Complianceid pass data
    complianceid_generic_chart, complianceid_pass_data_chart = complianceid_pass_data_charts()

    # ExemptedUsers pass data
    exemptedusers_generic_chart, exemptedusers_pass_data_chart,exception_summary = ExemptedUsers_pass_data_charts()

    # Health & Motor Renewal pass data
    healthrenewal_generic_chart, healthrenewal_pass_data_chart = health_motor_renewal_pass_data_charts()

    html_content = render_template(
        "index.html",
        showdownloadbutton=False,
        favicon_base64=get_favicon_base64(),


        # trends charts
        DLP_trends=DLP_trends,

         # justification chart
        justification_chart = justification_chart, 


        # block data
        generic_block_charts=generic_block_charts,
        charts_by_blocktype=charts_by_blocktype,

        # PII block data
        generic_PIIblock_charts=generic_PIIblock_charts,
        charts_by_PIIblocktype=charts_by_PIIblocktype,

        # Complianceid pass data
        complianceid_generic_chart=complianceid_generic_chart,
        complianceid_pass_data_chart=complianceid_pass_data_chart,

        # ExemptedUsers pass data
        exemptedusers_generic_chart=exemptedusers_generic_chart,
        exemptedusers_pass_data_chart=exemptedusers_pass_data_chart,
        exception_summary=exception_summary,

        # Health & Motor Renewal pass data
        healthrenewal_generic_chart=healthrenewal_generic_chart,
        healthrenewal_pass_data_chart=healthrenewal_pass_data_chart,



    )
    html_bytes = html_content.encode("utf-8")

    return send_file(
        io.BytesIO(html_bytes),
        mimetype="text/html",
        as_attachment=True,
        download_name="dashboard.html"
    )


if __name__ == "__main__":
    app.run(debug=True)
