from __future__ import unicode_literals
from frappe import _


def get_data():
	return [
		{
			"label": _("Process Manufacturing"),
			"items": [
				{
					"type": "doctype",
					"name": "Item",
					"description": _("All Products or Services."),
					"onboard": 1
				},
				{
					"type": "doctype",
					"name": "Batch",
					"description": _("Batch (lot) of an Item."),
					"onboard": 1,
					"dependencies": ["Item"]
				},
				{
					"type": "doctype",
					"name": "Manufacturing Department",
					"description": _("Manufacturing Department"),
					"onboard": 1
				},
				{
					"type": "doctype",
					"name": "Workstation",
					"description": _("Workstation"),
					"onboard": 1,
					"dependencies": ["Manufacturing Department"]
				},
				{
					"type": "doctype",
					"name": "Process Type",
					"description": _("Process Type."),
					"onboard": 1
				},
				{
					"type": "doctype",
					"name": "Process Definition",
					"description": _("Process Definition."),
					"onboard": 1,
					"dependencies": ["Workstation", "Manufacturing Department", "Process Type", "Item"]
				},
			]
		},
		{
			"label": _("Production"),
			"items": [
				{
					"type": "doctype",
					"name": "Process Order",
					"description": _("Process Manufacturing Order."),
					"onboard": 1,
					"dependencies": ["Warehouse", "Workstation", "Manufacturing Department", "Process Type",
									 "Process Definition"]
				},
				{
					"type": "doctype",
					"name": "Stock Entry",
					"description": _("Record item movement."),
					"onboard": 1,
					"dependencies": ["Item"]
				},
				{
					"type": "doctype",
					"name": "Material Request",
					"description": _("Requests for items."),
					"onboard": 1,
					"dependencies": ["Item"]
				},
			]
		},
	]
