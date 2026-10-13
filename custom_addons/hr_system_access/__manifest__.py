{
    'name': "Dostępy do systemów",
    'summary': "Dostępy pracowników do kont w systemach",
    'description': """
Rejestr systemów, kont i nadań/odebrań uprawnień.
Jeden system ma wiele kont, konto ma wiele dostępów,
dostęp należy do jednego pracownika i ma role (tagi).
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Human Resources',
    'version': '0.2',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_system_views.xml',
        'views/hr_employee_views.xml',
    ],
    'application': True,
}
