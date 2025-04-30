odoo.define('legal_compliance.ComplianceDashboard', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;

    var ComplianceDashboard = AbstractAction.extend({
        template: 'ComplianceDashboard',
        events: {
            'click .o_compliance_refresh': '_onRefresh',
        },

        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.dashboard_data = {};
        },

        willStart: function () {
            var self = this;
            return this._rpc({
                route: '/compliance/dashboard_data',
            }).then(function (result) {
                self.dashboard_data = result;
            });
        },

        _render: function () {
            var self = this;
            this.$el.html(QWeb.render('ComplianceDashboard', {
                widget: self,
            }));
        },

        _onRefresh: function () {
            this.reload();
        },
    });

    core.action_registry.add('compliance_dashboard', ComplianceDashboard);

    return ComplianceDashboard;
});

// Compliance status in systray
odoo.define('legal_compliance.ComplianceSystray', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var SystrayMenu = require('web.SystrayMenu');
    var rpc = require('web.rpc');

    var ComplianceSystray = Widget.extend({
        template: 'legal_compliance.ComplianceSystray',
        events: {
            'click': '_onClick',
        },

        willStart: function () {
            var self = this;
            return rpc.query({
                route: '/compliance/check_due',
            }).then(function (result) {
                self.due_count = result.due_count;
            });
        },

        _onClick: function () {
            this.do_action({
                type: 'ir.actions.act_window',
                name: 'Due Compliance Checks',
                res_model: 'compliance.rule',
                views: [[false, 'list'], [false, 'form']],
                domain: [['next_check_date', '<=', new Date().toISOString().split('T')[0]]],
                context: {'search_default_active': 1},
            });
        },
    });

    SystrayMenu.Items.push(ComplianceSystray);

    return ComplianceSystray;
});