# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "edpms"
app_title = "Erpnext Forex Hedging Edpms Settlement"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Forex Hedging Edpms Settlement for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/edpms/css/edpms.bundle.css"
app_include_js = "/assets/edpms/js/edpms.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "edpms.engine.on_document_submit",
        "on_cancel": "edpms.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "edpms.engine.daily_scheduled_sync"
    ]
}
