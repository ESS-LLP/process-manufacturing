# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "process_manufacturing"
app_title = "Process Manufacturing"
app_publisher = "earthians"
app_description = "Process Manufacturing"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@earthianslive.com"
app_license = "MIT"

fixtures = [{"dt":"Custom Field", "filters": [["fieldname", "in", ("process_order", "department")]]}]

doc_events = {
 	"Stock Entry": {
        "on_submit": "process_manufacturing.process_manufacturing.doctype.process_order.process_order.manage_se_changes",
        "on_cancel": "process_manufacturing.process_manufacturing.doctype.process_order.process_order.manage_se_changes"
    }
}
# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/process_manufacturing/css/process_manufacturing.css"
# app_include_js = "/assets/process_manufacturing/js/process_manufacturing.js"

# include js, css files in header of web template
# web_include_css = "/assets/process_manufacturing/css/process_manufacturing.css"
# web_include_js = "/assets/process_manufacturing/js/process_manufacturing.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "process_manufacturing.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "process_manufacturing.install.before_install"
# after_install = "process_manufacturing.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "process_manufacturing.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"process_manufacturing.tasks.all"
# 	],
# 	"daily": [
# 		"process_manufacturing.tasks.daily"
# 	],
# 	"hourly": [
# 		"process_manufacturing.tasks.hourly"
# 	],
# 	"weekly": [
# 		"process_manufacturing.tasks.weekly"
# 	]
# 	"monthly": [
# 		"process_manufacturing.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "process_manufacturing.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "process_manufacturing.event.get_events"
# }
