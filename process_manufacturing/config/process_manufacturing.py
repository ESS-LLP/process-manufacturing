from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Production"),
			"items": [
                {
					"type": "doctype",
					"name": "Oztro Process Order",
					"description": _("Process Manufacturing Order."),
				},
				{
					"type": "doctype",
					"name": "Stock Entry",
					"description": _("Record item movement."),
				},
				{
					"type": "doctype",
					"name": "Material Request",
					"description": _("Requests for items."),
				},
			]
		},
        {
			"label": _("Process Manufacturing"),
			"items": [
				{
					"type": "doctype",
					"name": "Oztro Process",
					"description": _("Process Definition."),
				},
				{
					"type": "doctype",
					"name": "Oztro Process Type",
					"description": _("Oztro Process Type."),
				},
                {
					"type": "doctype",
					"name": "Oztro Manufacturing Department",
					"description": _("Oztro Manufacturing Department"),
				},
                {
					"type": "doctype",
					"name": "Item",
					"description": _("All Products or Services."),
				},
                {
					"type": "doctype",
					"name": "Batch",
					"description": _("Batch (lot) of an Item."),
				},
			]
		},
	]
