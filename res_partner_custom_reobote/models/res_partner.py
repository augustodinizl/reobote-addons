from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


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
        partner._create_product_category()
        return partner

    def write(self, vals):
        """
        Sobrescreve o método write para criar uma nova subcategoria de produto
        se o nome_curto_cliente for alterado.
        """
        result = super(ResPartner, self).write(vals)
        for partner in self:
            if 'nome_curto_cliente' in vals:
                partner._create_product_category()
        return result

    def _create_product_category(self):
        """
        Cria uma nova categoria de produto associada ao parceiro, se necessário.
        """
        for partner in self:
            if partner.is_company and partner.nome_curto_cliente:
                product_category = self.env['product.category'].search([
                    ('name', '=', 'Produto Acabado')
                ], limit=1)

                if not product_category:
                    raise ValidationError(_("Categoria 'Produto Acabado' não encontrada. Crie-a primeiro."))

                # Cria a nova subcategoria sem verificar se já existe:
                new_category = self.env['product.category'].create({
                    'name': partner.nome_curto_cliente,
                    'parent_id': product_category.id,
                    'code_prefix': partner.nome_curto_cliente,
                })

                partner.write({'categoria_produto_id': new_category.id})