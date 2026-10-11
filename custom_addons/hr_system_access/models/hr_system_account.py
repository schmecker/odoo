from odoo import fields, models


class HrSystemAccount(models.Model):
    _name = 'hr.system.account'
    _description = 'Konta w systemach'

    name = fields.Char(string="Nazwa")
    valid_from = fields.Date(string="Ważne do")
    valid_until = fields.Date(string="Ważne od")

    login = fields.Char(string='Login', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Telefon')

    is_active = fields.Boolean(default=True, string="Aktywne?")
    # system_id = fields.Many2one(comodel_name='hr.system', string="System ID", required=True, ondelete='cascade')
    # permissions = fields.Many2many('hr.system.account.tag',)

    _sql_constraints = [
        (
            "check_date",
            "CHECK(valid_until IS NULL OR valid_from IS NULL OR valid_from <= valid_until)",
            "Data końcowa nie może być wcześniejsza niż data początkowa",
        ),
    ]
