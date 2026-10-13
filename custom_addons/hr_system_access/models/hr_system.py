from odoo import fields, models


class HrSystem(models.Model):
    _name = 'hr.system'
    _description = 'System'
    _order = 'sequence, name'

    name = fields.Char('Nazwa', required=True)
    valid_from = fields.Date('Ważne od')
    valid_until = fields.Date('Ważne do')
    is_active = fields.Boolean('Aktywny', default=True)
    url = fields.Char('URL')
    sequence = fields.Integer('Sekwencja', default=10)
    account_ids = fields.One2many(
        'hr.system.account',
        'system_id',
        string='Konta',
    )
    account_count = fields.Integer(
        compute='_compute_account_count',
        string='Liczba kont',
    )

    _sql_constraints = [
        (
            'check_date',
            'CHECK(valid_until IS NULL OR valid_from IS NULL OR valid_from <= valid_until)',
            'Data końcowa nie może być wcześniejsza niż data początkowa.',
        ),
    ]

    def _compute_account_count(self):
        for system in self:
            system.account_count = len(system.account_ids)
