from odoo import fields, models, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Definição dos campos Many2one
    codigo_cliente = fields.Many2one('reobote.custom', string="Código do Cliente", domain=[('campo', '=', 'codigo_cliente')])
    diametro_externo = fields.Many2one('reobote.custom', string="Diametro Externo", domain=[('campo', '=', 'diametro_externo')])
    diametro_interno = fields.Many2one('reobote.custom', string="Diametro Interno", domain=[('campo', '=', 'diametro_interno')])
    espessura = fields.Many2one('reobote.custom', string="Espessura", domain=[('campo', '=', 'espessura')])
    comprimento = fields.Many2one('reobote.custom', string="Comprimento", domain=[('campo', '=', 'comprimento')])
    perfil_externo = fields.Many2one('reobote.custom', string="Perfil Externo", domain=[('campo', '=', 'perfil_externo')])
    perfil_interno = fields.Many2one('reobote.custom', string="Perfil Interno", domain=[('campo', '=', 'perfil_interno')])
    norma = fields.Many2one('reobote.custom', string="Norma", domain=[('campo', '=', 'norma')])
    materia_prima = fields.Many2one('reobote.custom', string="Matéria Prima", domain=[('campo', '=', 'materia_prima')])
    aco = fields.Many2one('reobote.custom', string="Aço", domain=[('campo', '=', 'aco')])
    fornecimento = fields.Many2one('reobote.custom', string="Fornecimento", domain=[('campo', '=', 'fornecimento')])
    superficie = fields.Many2one('reobote.custom', string="Superfície", domain=[('campo', '=', 'superficie')])
    faces = fields.Many2one('reobote.custom', string="Faces", domain=[('campo', '=', 'faces')])
    embalagem = fields.Many2one('reobote.custom', string="Embalagem", domain=[('campo', '=', 'embalagem')])

    @api.onchange(
        'codigo_cliente', 'diametro_externo', 'diametro_interno', 'espessura',
        'comprimento', 'perfil_externo', 'perfil_interno', 'norma',
        'materia_prima', 'aco', 'fornecimento', 'superficie', 'faces', 'embalagem'
    )
    def _onchange_reobote_custom_fields(self):
        """
        Atualiza o campo `campo` no modelo `reobote.custom` com o nome do campo Many2one utilizado.
        """
        # Itera sobre todos os campos Many2one para verificar qual foi alterado
        for field_name in [
            'codigo_cliente', 'diametro_externo', 'diametro_interno', 'espessura',
            'comprimento', 'perfil_externo', 'perfil_interno', 'norma',
            'materia_prima', 'aco', 'fornecimento', 'superficie', 'faces', 'embalagem'
        ]:
            field_value = getattr(self, field_name)  # Obtém o valor atual do campo
            if field_value:
                # Atualiza o campo `campo` do registro relacionado
                field_value.campo = field_name

    @api.model
    def create(self, vals):
        """
        Atualiza o campo `campo` ao criar um registro em `sale.order.line`.
        """
        res = super(SaleOrderLine, self).create(vals)
        for field_name in [
            'codigo_cliente', 'diametro_externo', 'diametro_interno', 'espessura',
            'comprimento', 'perfil_externo', 'perfil_interno', 'norma',
            'materia_prima', 'aco', 'fornecimento', 'superficie', 'faces', 'embalagem'
        ]:
            if vals.get(field_name):
                custom = self.env['reobote.custom'].browse(vals[field_name])
                if custom:
                    custom.campo = field_name
        return res

    def write(self, vals):
        """
        Atualiza o campo `campo` ao modificar um registro em `sale.order.line`.
        """
        res = super(SaleOrderLine, self).write(vals)
        for record in self:
            for field_name in [
                'codigo_cliente', 'diametro_externo', 'diametro_interno', 'espessura',
                'comprimento', 'perfil_externo', 'perfil_interno', 'norma',
                'materia_prima', 'aco', 'fornecimento', 'superficie', 'faces', 'embalagem'
            ]:
                if field_name in vals:
                    custom = self.env['reobote.custom'].browse(vals[field_name])
                    if custom:
                        custom.campo = field_name
        return res
