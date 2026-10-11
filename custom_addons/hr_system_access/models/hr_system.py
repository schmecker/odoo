from odoo import fields, models


class HrSystem(models.Model):
    _name = 'hr.system'
    _description = 'Systemy'
    _order = 'sequence'

    name = fields.Char('Nazwa', required=True)
    valid_from = fields.Date('Ważne od')
    valid_until = fields.Date('Ważne do')
    is_active = fields.Boolean('Czy aktywne?', default=True)
    url = fields.Char('URL')
    sequence = fields.Integer('Sekwencja', default=10)

    _sql_constraints = [
        (
            'check_date',
            'CHECK(valid_until IS NULL OR valid_from IS NULL OR valid_from <= valid_until)',
            'Data końcowa nie może być wcześniejsza niż data początkowa.',
        ),
    ]
