from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    nome_curto_cliente = fields.Char(string="Nome da Categoria")
    categoria_produto_id = fields.Many2one('product.category', string="Categoria de Produto")

    @api.model
    def create(self, vals):
        """
        Sobrescreve o método create para criar uma subcategoria de produto
        diretamente no campo categoria_produto_id do parceiro.
        """
        partner = super(ResPartner, self).create(vals)

        if partner.is_company and partner.nome_curto_cliente:
            product_category = self.env['product.category'].search([
                ('name', '=', 'Produto Acabado')
            ], limit=1)

            if not product_category:
                raise ValueError(_("Categoria 'Produto Acabado' não encontrada. Crie-a primeiro."))

            # Cria a subcategoria diretamente no campo categoria_produto_id:
            partner.write({
                'categoria_produto_id': self.env['product.category'].create({
                    'name': partner.nome_curto_cliente,
                    'parent_id': product_category.id,
                    'code_prefix': partner.nome_curto_cliente,
                }).id
            })

        return partner