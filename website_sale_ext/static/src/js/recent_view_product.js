odoo.define("website_sale.load", function(require) {
    "use strict";
    const ajax = require("web.ajax");
    const core = require("web.core");
    const QWeb = core.qweb;
    ajax.loadXML(
        "/website_sale_ext/static/src/xml/recently_viewed_products.xml",
        QWeb
    );
});
