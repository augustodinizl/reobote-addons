from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Definição dos campos Many2one - APENAS OS NOVOS CAMPOS, relacionados ao modelo reobote.custom
    prazo_entrega = fields.Many2one('reobote.custom', string="Prazo de Entrega", domain=[('campo', '=', 'prazo_entrega')])
    frete = fields.Many2one('reobote.custom', string="Frete", domain=[('campo', '=', 'frete')])
    pis_incluso = fields.Many2one('reobote.custom', string="PIS Incluso", domain=[('campo', '=', 'pis_incluso')])
    cofins_incluso = fields.Many2one('reobote.custom', string="COFINS Incluso", domain=[('campo', '=', 'cofins_incluso')])
    icms_incluso = fields.Many2one('reobote.custom', string="ICMS Incluso", domain=[('campo', '=', 'icms_incluso')])
    ipi_a_incluir = fields.Many2one('reobote.custom', string="IPI a Incluir", domain=[('campo', '=', 'ipi_a_incluir')])

    @api.onchange('prazo_entrega', 'frete', 'pis_incluso', 'cofins_incluso', 'icms_incluso', 'ipi_a_incluir')
    def _onchange_reobote_custom_fields(self):
        """
        Atualiza o campo `campo` no modelo `reobote.custom` com o nome do campo Many2one utilizado.
        """
        for field_name in ['prazo_entrega', 'frete', 'pis_incluso', 'cofins_incluso', 'icms_incluso', 'ipi_a_incluir']:
            field_value = getattr(self, field_name)
            if field_value:
                field_value.campo = field_name

    @api.model
    def create(self, vals):
        """
        Atualiza o campo `campo` ao criar um registro em `sale.order`.
        """
        res = super(SaleOrder, self).create(vals)
        for field_name in ['prazo_entrega', 'frete', 'pis_incluso', 'cofins_incluso', 'icms_incluso', 'ipi_a_incluir']:
            if vals.get(field_name):
                custom = self.env['reobote.custom'].browse(vals[field_name])
                if custom:
                    custom.campo = field_name
        return res

    def write(self, vals):
        """
        Atualiza o campo `campo` ao modificar um registro em `sale.order`.
        """
        res = super(SaleOrder, self).write(vals)
        for record in self:
            for field_name in ['prazo_entrega', 'frete', 'pis_incluso', 'cofins_incluso', 'icms_incluso', 'ipi_a_incluir']:
                if field_name in vals:
                    custom = self.env['reobote.custom'].browse(vals[field_name])
                    if custom:
                        custom.campo = field_name
        return res