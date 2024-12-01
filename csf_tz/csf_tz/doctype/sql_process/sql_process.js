// Copyright (c) 2022, Aakvatech and contributors
// For license information, please see license.txt

frappe.ui.form.on('SQL Process', {
	refresh: function (frm) {
		frm.set_value('process', []);
	},
	refresh_q: function (frm) {
		frappe.call({
			method: "get_process",
			doc: frm.doc,
			callback: function (r) {
				update_table(frm, r.message);

			}
		});
	}
});

frappe.ui.form.on('SQL Process Detail', {
	kill: function (frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		frappe.call({
			method: "kill_process",
			doc: frm.doc,
			args: {
				pid: row.id
			},
			callback: function (r) {
				frm.trigger('refresh_q');

			}
		});
	}
});

const update_table = (frm, data) => {
	frm.doc.process = [];
	data.forEach(element => {
		let row = frm.add_child('process', {
			id: element.id,
			time: element.time,
			query: element.info,

		});
		frm.refresh_field('process');

	});
};