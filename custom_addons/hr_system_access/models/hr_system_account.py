from odoo import fields, models


class HrSystemAccount(models.Model):
    _name = 'hr.system.account'
    _description = 'Konto w systemie'
    _order = 'system_id, login'

    name = fields.Char('Nazwa')
    login = fields.Char('Login', required=True)
    email = fields.Char('Email')
    phone = fields.Char('Telefon')
    valid_from = fields.Date('Ważne od')
    valid_until = fields.Date('Ważne do')
    is_active = fields.Boolean('Aktywne', default=True)
    system_id = fields.Many2one(
        'hr.system',
        string='System',
        required=True,
        ondelete='cascade',
        index=True,
    )
    access_ids = fields.One2many(
        'hr.system.account.access',
        'account_id',
        string='Dostępy',
    )
    access_count = fields.Integer(
        compute='_compute_access_count',
        string='Liczba dostępów',
    )

    _sql_constraints = [
        (
            'check_date',
            'CHECK(valid_until IS NULL OR valid_from IS NULL OR valid_from <= valid_until)',
            'Data końcowa nie może być wcześniejsza niż data początkowa.',
        ),
        (
            'login_system_uniq',
            'unique(system_id, login)',
            'Login musi być unikalny w ramach systemu.',
        ),
    ]

    def _compute_access_count(self):
        for account in self:
            account.access_count = len(account.access_ids)
