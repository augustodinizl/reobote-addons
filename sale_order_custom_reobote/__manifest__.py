{
    'name': 'Sale Order Customization - Reobote',
    'version': '16.0.1.7.0',
    'category': 'Sales',
    'summary': 'Customizations for Sale Orders - Reobote',
    'description': """
        This module implements specific customizations for sale orders
        for Reobote's needs.
    """,
    'author': 'LTCS.com.br - Augusto',
    'website': 'https://www.ltcs.com.br',
    'license': 'LGPL-3',
    'depends': ['contacts', 'sale', 'l10n_br_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_view.xml', 
        'views/report_saleorder_document.xml', 
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
