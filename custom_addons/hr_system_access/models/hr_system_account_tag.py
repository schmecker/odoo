from odoo import fields, models


class HrSystemAccountTag(models.Model):
    _name = 'hr.system.account.tag'
    _description = 'Rola dostępu'
    _order = 'name'

    name = fields.Char('Nazwa roli', required=True)
    color = fields.Integer('Kolor')
    access_ids = fields.Many2many(
        'hr.system.account.access',
        'hr_system_account_access_tag_rel',
        'tag_id',
        'access_id',
        string='Dostępy',
    )

    _sql_constraints = [
        (
            'name_uniq',
            'unique(name)',
            'Nazwa roli musi być unikalna.',
        ),
    ]
