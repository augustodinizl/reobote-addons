from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Definição dos campos Many2one
    codigo_cliente = fields.Many2one('reobote.custom', string="Código do Cliente", domain=[('campo', '=', 'codigo_cliente')])
    diametro_externo = fields.Many2one('reobote.custom', string="Diâmetro Externo", domain=[('campo', '=', 'diametro_externo')])
    diametro_interno = fields.Many2one('reobote.custom', string="Diâmetro Interno", domain=[('campo', '=', 'diametro_interno')])
    espessura = fields.Many2one('reobote.custom', string="Espessura", domain=[('campo', '=', 'espessura')])
    comprimento = fields.Many2one('reobote.custom', string="Comprimento", domain=[('campo', '=', 'comprimento')])
    variacao = fields.Many2one('reobote.custom', string="Variação", domain=[('campo', '=', 'variacao')])
    dint_tolerancia_maior = fields.Many2one('reobote.custom', string="+", domain=[('campo', '=', 'dint_tolerancia_maior')])
    dint_tolerancia_menor = fields.Many2one('reobote.custom', string="-", domain=[('campo', '=', 'dint_tolerancia_menor')])
    dext_tolerancia_maior = fields.Many2one('reobote.custom', string="+", domain=[('campo', '=', 'dext_tolerancia_maior')])
    dext_tolerancia_menor = fields.Many2one('reobote.custom', string="-", domain=[('campo', '=', 'dext_tolerancia_menor')])
    comp_tolerancia_maior = fields.Many2one('reobote.custom', string="+", domain=[('campo', '=', 'comp_tolerancia_maior')])
    comp_tolerancia_menor = fields.Many2one('reobote.custom', string="-", domain=[('campo', '=', 'comp_tolerancia_menor')])
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
        Este método onchange não é mais necessário e foi removido.
        A lógica de atualizar o campo 'campo' em reobote.custom será feita diretamente
        nos métodos create e write, tornando o código mais eficiente.
        """
        pass

    @api.model
    def create(self, vals):
        """
        Atualiza o campo `campo` ao criar um registro em `product.template`.
        """
        res = super(ProductTemplate, self).create(vals)
        for field_name in [
            'codigo_cliente', 'diametro_externo', 'diametro_interno', 'espessura',
            'comprimento', 'perfil_externo', 'perfil_interno', 'norma',
            'materia_prima', 'aco', 'fornecimento', 'superficie', 'faces', 'embalagem'
        ]:
            if vals.get(field_name):
                custom = self.env['reobote.custom'].browse(vals[field_name])
                if custom and not custom.campo: # Verifica se o campo já não foi setado
                    custom.campo = field_name
        return res
    def write(self, vals):
            """
            Atualiza o campo `campo` ao modificar um registro em `product.template`.
            """
            res = super(ProductTemplate, self).write(vals)
            for record in self:
                for field_name in [
                    'codigo_cliente', 'diametro_externo', 'diametro_interno', 'espessura',
                    'comprimento', 'perfil_externo', 'perfil_interno', 'norma',
                    'materia_prima', 'aco', 'fornecimento', 'superficie', 'faces', 'embalagem'
                ]:
                    if field_name in vals and vals[field_name]:
                        custom = self.env['reobote.custom'].browse(vals[field_name])
                        if custom and custom.campo != field_name: # Verifica se o campo já não tem o valor correto
                            custom.campo = field_name
                    elif field_name in vals and not vals[field_name]: # Caso o campo seja limpo
                        old_custom = record[field_name]
                        if old_custom and old_custom.campo == field_name:
                            old_custom.campo = False
            return res