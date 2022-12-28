odoo.define("sd_multi_barcode_pos.models", function (require){
    "use strict";

    const models = require('point_of_sale.models');
    const _super_Order = models.Order.prototype;
    let _super_posmodel = models.PosModel.prototype;

    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var self = this;
            // load new field in this method
            models.load_fields('product.product',['barcode_ids_list']);
            _super_posmodel.initialize.apply(this, arguments);
        },
    });
});