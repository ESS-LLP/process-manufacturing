// Copyright (c) 2018, earthians and contributors
// For license information, please see license.txt

frappe.ui.form.on('Process Definition', {
	refresh: function(frm) {

	},
	setup: function (frm) {
		frm.set_query("workstation", function () {
			return {
				filters: {"department": frm.doc.department}
			}
		});
	}
});
