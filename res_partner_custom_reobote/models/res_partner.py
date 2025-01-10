from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    nome_curto_cliente = fields.Char(string="Nome da Categoria")
    categoria_produto_id = fields.Many2one('product.category', string="Categoria de Produto")

    @api.model_create_multi
    def create(self, vals_list):
        """
        Sobrescreve o método create para criar uma subcategoria de produto
        diretamente no campo categoria_produto_id do parceiro.
        """
        partners = super(ResPartner, self).create(vals_list)
        
        self.flush_model(partners) # Força o commit no banco

        for partner, vals in zip(partners, vals_list):
            if partner.is_company and partner.customer_rank > 0 and vals.get('nome_curto_cliente'):
                product_category = self.env['product.category'].search([
                    ('name', '=', 'Produto Finalizado')
                ], limit=1)

                if not product_category:
                    raise ValueError(_("Categoria 'Produto Finalizado' não encontrada. Crie-a primeiro."))

                # Cria a subcategoria:
                new_category = self.env['product.category'].create({
                        'name': vals.get('nome_curto_cliente'),
                        'parent_id': product_category.id,
                        'code_prefix': vals.get('nome_curto_cliente'),
                    })
                
                partner.write({'categoria_produto_id': new_category.id})

        return partners