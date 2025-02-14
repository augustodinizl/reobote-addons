{
    'name': 'Manufacture Order Customization - Reobote',
    'version': '16.0.1.7.2',
    'category': 'Manufacturing',
    'summary': 'Customizations for Manufacture Orders - Reobote',
    'description': """
        This module implements specific customizations for manufacture orders
        for Reobote's needs.
    """,
    'author': 'LTCS.com.br - Augusto',
    'website': 'https://www.ltcs.com.br',
    'license': 'LGPL-3',
    'depends': ['mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/work_order_form.xml', 
        'views/report_mrporder.xml',
        'views/routing_reobote.xml',
        'views/mrp_production_form.xml',
        'reports/report_certificado_qualidade_templates.xml',
        'reports/certificado_qualidade.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
