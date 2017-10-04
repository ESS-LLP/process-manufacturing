// Copyright (c) 2017, earthians and contributors
// For license information, please see license.txt

frappe.ui.form.on('Oztro Process Order', {
	refresh: function(frm){
		if(!frm.doc.__islocal && frm.doc.status == 'Open'){
			var start_btn = frm.add_custom_button(__('Start'), function(){
				start_process_order(frm)
			});
			start_btn.addClass('btn-primary');
		}
		if(!frm.doc.__islocal && frm.doc.status == 'Start'){
			var finish_btn = frm.add_custom_button(__('Finish'), function(){
				finish_process_order(frm)
			});
			finish_btn.addClass('btn-primary')
		}
	},
	process_type: function(frm){
		frm.set_query("process_name", function () {
			return {
				filters: {"department": frm.doc.department, "process_type": frm.doc.process_type}
			}
		});
	},
	department: function(frm){
		if(frm.doc.department){
			frappe.call({
				"method": "frappe.client.get",
				args: {
					doctype: "Oztro Manufacturing Department",
					name: frm.doc.department
				},
				callback: function (data) {
					frappe.model.set_value(frm.doctype,frm.docname, "wip_warehouse", data.message.wip_warehouse);
					frappe.model.set_value(frm.doctype,frm.docname, "fg_warehouse", data.message.fg_warehouse);
					frappe.model.set_value(frm.doctype,frm.docname, "scrap_warehouse", data.message.scrap_warehouse);
					frappe.model.set_value(frm.doctype,frm.docname, "src_warehouse", data.message.src_warehouse);
				}
			});
			frm.set_query("process_name", function () {
				return {
					filters: {"department": frm.doc.department, "process_type": frm.doc.process_type}
				}
			});
		}
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

var start_process_order = function(frm){
	if(frm.doc.materials){
		for(item in frm.doc.materials){
			if(frm.doc.materials[item].quantity <= 0){
				frappe.msgprint('Quantity of material should be greater than zero.', "Validation Error");
				frappe.throw()
			}
		}
		frappe.call({
			doc: frm.doc,
			method: "start_finish_processing",
			args:{
				"status": "Start"
			},
			callback: function(r) {
				frm.reload_doc()
				var doclist = frappe.model.sync(r.message);
				frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
			}
		});
	}
}

var finish_process_order = function(frm){
	if(frm.doc.finished_products){
		frappe.confirm(
				'Are you sure to Finish?',
				function(){
					frappe.call({
						doc: frm.doc,
						method: "start_finish_processing",
						args:{
							"status": "Finish"
						},
						callback: function(r) {
							frm.reload_doc()
							var doclist = frappe.model.sync(r.message);
							frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
						}
					});
				},
				function(){
					window.close();
				}
		)
	}
}

/*var start_prompt = function(frm) {
	let fields = []
	$.each(frm.doc.finished_products || [], function(i, row) {
		console.log(i);
		console.log(row);
		fields.push({
			fieldtype: "Float",
			label: __("Quantity of {0} for {1}", [row.item_name,"Processing"]),
			fieldname: "qty_"+row.name
		});
	})
	/*frm.doc.materials.forEach(function(frm) {
		console.log("ASSSSSSSSSSSSS");
	})*/
	/*frappe.prompt(
		fields,
		function(data) {
			console.log(data);
			frappe.call({
				doc: frm.doc,
				method: "start_processing",
				args: {
					'qty': data.qty
				},
				callback: function(r) {
					//refresh_field("materials");
					frm.reload_doc()
				}
			});
		}, __("Select Quantity"), __("Make"));
}*/
