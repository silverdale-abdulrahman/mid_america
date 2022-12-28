odoo.define('sd_multi_barcode.ClientAction', function (require) {
'use strict';
var concurrency = require('web.concurrency');
var core = require('web.core');
var AbstractAction = require('web.AbstractAction');
var BarcodeParser = require('barcodes.BarcodeParser');

var ViewsWidget = require('stock_barcode.ViewsWidget');
var HeaderWidget = require('stock_barcode.HeaderWidget');
var LinesWidget = require('stock_barcode.LinesWidget');
var SettingsWidget = require('stock_barcode.SettingsWidget');
var utils = require('web.utils');
var ClientActionExt = require('stock_barcode.ClientAction');

var _t = core._t;

ClientActionExt.include({
    _getProductByBarcode: async function (barcode) {
        let product = this.productsByBarcode[barcode];
        if (product) {
            return product;
        } else {
            product = await this._rpc({
                model: 'product.product',
                method: 'search_read',
                args: [[['barcode_ids.name', '=', barcode]], ['barcode', 'display_name', 'uom_id', 'tracking']],

            });
            if (product.length) {
                console.log("Product : ", product)
                this.productsByBarcode[barcode] = product[0];
                return product[0];
            }
            return false;
        }
    },
})
});
