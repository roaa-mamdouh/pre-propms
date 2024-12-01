frappe.require([
    '/assets/csf_tz/js/csfUtlis.js',
    '/assets/csf_tz/js/shortcuts.js'
]);

frappe.ui.form.on("Purchase Order", {
    refresh: (frm) => {
        const limit_uom_as_item_uom = getValue("CSF TZ Settings", "CSF TZ Settings", "limit_uom_as_item_uom");
        if (limit_uom_as_item_uom == 1) {
            frm.set_query("uom", "items", function (frm, cdt, cdn) {
                let row = locals[cdt][cdn];
                return {
                    query:
                        "erpnext.accounts.doctype.pricing_rule.pricing_rule.get_item_uoms",
                    filters: {
                        value: row.item_code,
                        apply_on: "Item Code",
                    },
                };
            });
        }
    },
    supplier: function(frm) {
        setTimeout(function() {
            if (!frm.doc.tax_category){
                frappe.call({
                    method: "csf_tz.custom_api.get_tax_category",
                    args: {
                        doc_type: frm.doc.doctype,
                        company: frm.doc.company,
                    },
                    callback: function(r) {
                        if(!r.exc) {
                            frm.set_value("tax_category", r.message);
                            frm.trigger("tax_category");
                        }
                    }
                });           
        }
          }, 1000);   
    },
    setup: function(frm) {
        frm.set_query("taxes_and_charges", function() {
			return {
				"filters": {
                    "company": frm.doc.company,
				}
			};
        });
    },
});