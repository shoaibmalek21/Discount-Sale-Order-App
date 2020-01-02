# -*- coding: utf-8 -*-
{
    'name' : 'Discount on Sales Order',
    'summary': """Manage Discount on Sale Order""",
    'author': "shoaib",
    'version' : '11.0',
    'category': 'Sales',
    'website': 'https://www.shoaibmalek.com',
    'depends' : ['base','sale'],
    'data': [
        'data/discount_product_data.xml',
        'views/discount_on_sale_order.xml',
        'wizard/sale_order_discount_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,

}
