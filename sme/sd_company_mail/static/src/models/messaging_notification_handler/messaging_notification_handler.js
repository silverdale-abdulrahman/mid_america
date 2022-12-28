odoo.define('sd_company_mail/static/src/models/messaging_notification_handler/messaging_notification_handler.js', function (require) {
'use strict';

    const {registerInstancePatchModel,} = require('mail/static/src/model/model_core.js');
    const { decrement, increment } = require('mail/static/src/model/model_field_command.js');


    registerInstancePatchModel('mail.messaging_notification_handler', 'sd_company_mail/static/src/models/messaging_notification_handler/messaging_notification_handler.js', {
        /**
            * @override
        */
        async _handleNotificationNeedaction(data) {
            const response = await this.env.services.rpc({
                model: 'mail.message',
                method: 'get_company',
                args: [[data.id]]
            });

            if (response === false || response === Number(document.cookie.split('cids=')[1])) {
                const message = this.env.models['mail.message'].insert(this.env.models['mail.message'].convertData(data));
                this.env.messaging.inbox.update({ counter: increment() });
                const originThread = message.originThread;
                if (originThread && message.isNeedaction) {
                    originThread.update({ message_needaction_counter: increment() });
                }
                // manually force recompute of counter
                this.messaging.messagingMenu.update();
            }
        }
    });
});
