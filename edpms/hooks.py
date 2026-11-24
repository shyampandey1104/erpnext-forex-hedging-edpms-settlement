# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "edpms"
app_title = "Erpnext Forex Hedging Edpms Settlement"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Forex Hedging Edpms Settlement - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/edpms/css/edpms.bundle.css"
app_include_js = "/assets/edpms/js/edpms.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Erpnext Forex Hedging Edpms Settlement Entry": {
        "validate": "edpms.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "edpms.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "edpms.tasks.hourly_sync"
    ],
    "daily": [
        "edpms.tasks.daily_reconciliation"
    ],
    "weekly": [
        "edpms.tasks.weekly_digest"
    ]
}
