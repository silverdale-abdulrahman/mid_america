odoo.define('sd_restrict_multicompany_checkboxes.switch_company_menu_extended', function(require) {
"use strict";

/**
 * User will be only allowed to be in one company environment at a time
 */

var config = require('web.config');
var core = require('web.core');
var session = require('web.session');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');
var SwitchCompanyMenuExtended = require('web.SwitchCompanyMenu')
var _t = core._t;

    SwitchCompanyMenuExtended.include({

        /**
         * @override
         */
         willStart: function () {
            var self = this;

             session.user_has_group('sd_restrict_multicompany_checkboxes.group_can_access_company_checkboxes').then(function (has_group) {
                if (has_group === false) {
                    self.$el.find(".toggle_company").addClass('d-none')
                }
            });

            return this._super.apply(this, arguments);
        },

    });

});