odoo.define("website_stock_info.load", function(require) {
    "use strict";
    const ajax = require("web.ajax");
    const core = require("web.core");
    const QWeb = core.qweb;
    ajax.loadXML(
        "/website_stock_info/static/src/xml/website_stock_info.xml",
        QWeb
    );
});
