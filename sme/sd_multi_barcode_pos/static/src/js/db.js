odoo.define('sd_multi_barcode_pos.db', function (require) {
"use strict";

    let DBExtend = require("point_of_sale.DB");
    let utils = require('web.utils');

    DBExtend.include({

        // Override the _product_search_string method and include the multi-barcodes in search
        _product_search_string: function(product){
            var str = product.display_name;
            if (product.barcode_ids_list) {
                let other_barcodes = JSON.parse(product.barcode_ids_list.replace(/'/g, '"'))
                for (var i=0; i <= other_barcodes.length; i++){
                    str += '|' + other_barcodes[i];
                }
            }
            if (product.barcode) {
                str += '|' + product.barcode;
            }
            if (product.default_code) {
                str += '|' + product.default_code;
            }
            if (product.description) {
                str += '|' + product.description;
            }
            if (product.description_sale) {
                str += '|' + product.description_sale;
            }
            str  = product.id + ':' + str.replace(/:/g,'') + '\n';
            return str;
        },
    });
});