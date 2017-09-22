// Copyright (c) 2017, earthians and contributors
// For license information, please see license.txt

frappe.ui.form.on('Oztro Process Order', {
	process_type: function(frm){
		frm.set_query("process_name", function () {
			return {
				filters: {"process_type": frm.doc.process_type}
			}
		});
	}
});
