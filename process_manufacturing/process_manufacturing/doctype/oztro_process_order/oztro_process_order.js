// Copyright (c) 2017, earthians and contributors
// For license information, please see license.txt

frappe.ui.form.on('Oztro Process Order', {
	process_type: function(frm){
		frm.set_query("process_name", function () {
			return {
				filters: {"process_type": frm.doc.process_type}
			}
		});
	},
	process_name: function(frm) {
		if(frm.doc.process_name){
			frappe.call({
				doc: frm.doc,
				method: "get_process_details",
				callback: function(r) {
					refresh_field("costing_method");
					refresh_field("finished_products");
					refresh_field("scrap");
					refresh_field("materials");
				}
			});
		}
	}
});
