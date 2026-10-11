from odoo import fields, models


class HrSystemAccountAccess(models.Model):
    _name = 'hr.system.account.access'
    _description = 'HrSystemAccount'

    name = fields.Char()
