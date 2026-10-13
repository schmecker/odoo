from odoo import api, fields, models


class HrSystemAccountAccess(models.Model):
    _name = 'hr.system.account.access'
    _description = 'Dostęp pracownika do konta'
    _order = 'account_id, employee_id'

    name = fields.Char('Nazwa', compute='_compute_name', store=True)
    account_id = fields.Many2one(
        'hr.system.account',
        string='Konto',
        required=True,
        ondelete='cascade',
        index=True,
    )
    system_id = fields.Many2one(
        related='account_id.system_id',
        store=True,
        index=True,
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Pracownik',
        required=True,
        ondelete='restrict',
        index=True,
    )
    tag_ids = fields.Many2many(
        'hr.system.account.tag',
        'hr_system_account_access_tag_rel',
        'access_id',
        'tag_id',
        string='Role',
    )
    valid_from = fields.Date('Ważne od')
    valid_until = fields.Date('Ważne do')
    is_active = fields.Boolean('Aktywny', default=True)

    _sql_constraints = [
        (
            'check_date',
            'CHECK(valid_until IS NULL OR valid_from IS NULL OR valid_from <= valid_until)',
            'Data końcowa nie może być wcześniejsza niż data początkowa.',
        ),
        (
            'account_employee_uniq',
            'unique(account_id, employee_id)',
            'Ten pracownik ma już dostęp do tego konta.',
        ),
    ]

    @api.depends('account_id', 'account_id.login', 'employee_id', 'employee_id.name')
    def _compute_name(self):
        for access in self:
            account = access.account_id.login or access.account_id.display_name or ''
            employee = access.employee_id.display_name or ''
            access.name = f'{employee} — {account}'.strip(' —') if employee or account else False
