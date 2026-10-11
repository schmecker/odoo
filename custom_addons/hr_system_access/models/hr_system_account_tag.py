from odoo import fields, models


class HrSystemAccountTag(models.Model):
    _name = 'hr.system.account.tag'
    _description = 'HrSystemAccount'

    name = fields.Char()
