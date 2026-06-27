{
    'name': 'Wooden Tools Store',
    'version': '1.0',
    'summary': ' custom module',
    'description': """
     
    """,
    'author': 'Salah',
    'category': 'Tools',
    'depends': ['base','sale','mail','account','product'],
    'assets': {


    },
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
     #   'views/owner2_view.xml',
        'views/technical_order.xml',
        'views/inherited_res_partner.xml',
        'data/order_sequence.xml',
    ],
    'images': [],
    'demo': [

    ],

    'application': True,
'installable': True,
}
