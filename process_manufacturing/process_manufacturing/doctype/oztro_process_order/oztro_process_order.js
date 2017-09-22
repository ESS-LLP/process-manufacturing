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
				stop_process_order(frm)
			});
			finish_btn.addClass('btn-primary')
		}
	},
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

var start_process_order = function(frm){
	me.frm.set_value("status", "Start");
	//start_prompt()
	cur_frm.save()
}

var stop_process_order = function(frm){
	me.frm.set_value("status", "Finish");
	cur_frm.save()
}

/*
var start_prompt = function(frm) {
	frappe.prompt({fieldtype:"Float", label: __("Qty for {0}", ["Processing"]), fieldname:"qty",
		description: __("Max: {0}", [10]), 'default': 10 },
		function(data) {
			if(data.quantity > 10) {
				frappe.msgprint(__("Quantity must not be more than {0}", [10]));
				return;
			}
			frappe.call({
				method:"erpnext.manufacturing.doctype.production_order.production_order.make_stock_entry",
				args: {
					"production_order_id": frm.doc.name,
					"purpose": "Processing",
					"qty": data.quantity
				},
				callback: function(r) {
					
					var doclist = frappe.model.sync(r.message);
					frappe.set_route("Form", doclist[0].doctype, doclist[0].name);

				}
			});
		}, __("Select Quantity"), __("Make"));
}*/
