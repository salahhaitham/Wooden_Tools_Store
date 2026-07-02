{
    'name': 'Wooden Tools Store',
    'version': '1.0',
    'summary': ' custom module',
    'description': """
     
    """,
    'author': 'Salah',
    'category': 'Tools',
    'depends': ['base','sale','mail','account','product','sale_management'],
    'assets': {


    },
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'wizards/cancel_order_wizard.xml',
        'views/technical_order.xml',
        'views/inherited_res_partner.xml',
        'data/order_sequence.xml',
        'reports/technical_order_report.xml',
        'views/sale_order.xml',

    ],
    'images': [],
    'demo': [

    ],

    'application': True,
'installable': True,
}
