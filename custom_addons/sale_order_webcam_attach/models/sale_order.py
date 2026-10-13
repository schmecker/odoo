import base64

from odoo import _, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_open_webcam_capture(self):
        self.ensure_one()
        if not self.id:
            raise UserError(_('Najpierw zapisz zlecenie sprzedaży.'))
        return {
            'type': 'ir.actions.client',
            'tag': 'sale_order_webcam_capture',
            'params': {
                'res_model': self._name,
                'res_id': self.id,
            },
        }

    def action_attach_webcam_photo(self, image_base64, filename=None):
        self.ensure_one()
        if not image_base64:
            raise UserError(_('Brak zdjęcia do załączenia.'))
        try:
            content = base64.b64decode(image_base64)
        except Exception as exc:
            raise UserError(_('Nie udało się odczytać zdjęcia.')) from exc
        if not content:
            raise UserError(_('Zdjęcie jest puste.'))
        if len(content) > 10 * 1024 * 1024:
            raise UserError(_('Zdjęcie jest zbyt duże (maks. 10 MB).'))
        filename = filename or _('zdjecie_kamera.jpg')
        self.message_post(
            body=_('Zdjęcie z kamery USB'),
            attachments=[(filename, content)],
            message_type='comment',
            subtype_xmlid='mail.mt_note',
        )
        return True
