{
    'name': 'Zdjęcie z kamery na zleceniu sprzedaży',
    'summary': 'Przycisk na zleceniu sprzedaży: zdjęcie z kamery USB jako załącznik przy czacie',
    'description': """
Na formularzu zlecenia sprzedaży dodaje przycisk „Zrób zdjęcie”.
Po kliknięciu otwiera podgląd kamery USB w przeglądarce
i załącza ujęcie przy czacie zlecenia.
    """,
    'author': 'My Company',
    'category': 'Sales',
    'version': '1.0',
    'depends': ['sale'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sale_order_webcam_attach/static/src/webcam_capture_dialog/*',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}
