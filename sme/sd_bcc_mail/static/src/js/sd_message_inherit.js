odoo.define('sd_bcc_mail/static/src/js/message_inherit.js', function (require) {
    'use strict';
    const {
        registerClassPatchModel,
        registerFieldPatchModel,
    } = require('mail/static/src/model/model_core.js');
    const { attr } = require('mail/static/src/model/model_field.js');
    registerFieldPatchModel('mail.message', 'sd_bcc_mail/static/src/js/message_inherit.js', {
        email_bcc: attr({
            default: false,
        }),
    });
    registerClassPatchModel('mail.message', 'sd_bcc_mail/static/src/js/message_inherit.js', {
        //----------------------------------------------------------------------
        // Public
        //----------------------------------------------------------------------

        /**
         * @override
         */
        convertData(data) {
            const data2 = this._super(data);
            if (Object.keys(data).includes('email_bcc') && data.email_bcc) {
                if (!data2.email_bcc) {
                    data2.email_bcc = data.email_bcc;
                }
            }
//            debugger;
            return data2;
        },
    });
});
