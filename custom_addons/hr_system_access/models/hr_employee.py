from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    system_access_ids = fields.One2many(
        'hr.system.account.access',
        'employee_id',
        string='Dostępy do systemów',
    )
