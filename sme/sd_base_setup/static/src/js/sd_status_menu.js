odoo.define('sd_base_setup.sd_status_menu', function (require) {
"use strict";

var core = require('web.core');
var session = require('web.session');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');
var QWeb = core.qweb;

/**
 * Menu item appended in the systray part of the navbar, redirects to the next
 * activities of all app
 */
var SdStatusActionMenu = Widget.extend({
    template:'sd_base_setup.SdStatusActionMenu',
    events: {
        'click .composerClicked': 'sdOpenFullComposer',
    },

    start: function () {
        return this._super();
    },

    init: function (parent, options) {
        this._super(parent);
        this.sd_modules = 0;
        this.modules_installed = 0;
        this.modules_not_installed = 0;
        this.loaded = false;
    },

    willStart: function () {
        const modulesPromise = this._rpc({
            model: 'ir.module.module',
            method: 'get_silverdale_apps',
        })
        return Promise.all(
            [modulesPromise]
        ).then(this._loadedCallback.bind(this));
    },

    _loadedCallback: function ([modules]) {
        // Process modules count
        this.sd_modules = modules.sd_modules;
        this.modules_installed = modules.modules_installed;
        this.modules_not_installed = modules.modules_not_installed;
        this.loaded = true;
    },

    sdOpenFullComposer: async function(ev) {
        ev.preventDefault();
        ev.stopPropagation();
        var defaultData = await this._rpc({
                model: 'mail.compose.message',
                method: 'get_help_default_data',
                args: [],
            });
            debugger
            var recipient_ids = []
            if (defaultData.recipient_id !== false){
                recipient_ids.push(defaultData.recipient_id)
            }
        const context = {
            default_partner_ids: recipient_ids,
            default_is_for_help: true,
            default_template_id: defaultData.template_id,
            default_url_link: window.location.href,
        };

        const action = {
            name: ("Get Help"),
            type: 'ir.actions.act_window',
            res_model: 'mail.compose.message',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new',
            context: context,
        };

        debugger;
        this.trigger().do_action(action)
    },

});

SystrayMenu.Items.push(SdStatusActionMenu);

return SdStatusActionMenu;

});

