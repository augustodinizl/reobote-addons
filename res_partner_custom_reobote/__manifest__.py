{
    'name': "Categoria de Produto no Parceiro",
    'version': '1.0',
    'summary': "Adiciona campo de categoria de produto no parceiro",
    'description': """
        Este módulo adiciona um campo Many2one no modelo res.partner para 
        relacioná-lo com uma categoria de produto e automatiza a criação 
        de uma subcategoria quando um novo parceiro do tipo empresa é criado.
    """,
    'author': "LTCS",
    'category': 'Sales',
    'depends': ['base', 'product', 'sale'],
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}