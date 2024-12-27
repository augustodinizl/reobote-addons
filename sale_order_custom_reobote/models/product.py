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
    concatenado = fields.Text(string="Concatenado")

    def _update_reobote_custom_campo(self, record, fields_to_update):
        """Atualiza o campo 'campo' na tabela reobote.custom."""
        for field_name in fields_to_update:
            if record[field_name]:
                custom = self.env['reobote.custom'].browse(record[field_name].id)
                if custom and custom.campo != field_name:
                    custom.campo = field_name
            else:
                old_custom = record.read([field_name])[0][field_name]
                if old_custom:
                    custom = self.env['reobote.custom'].browse(old_custom[0])
                    if custom and custom.campo == field_name:
                        custom.campo = False

    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        self._update_reobote_custom_campo(res, [
            'codigo_cliente', 'diametro_externo', 'diametro_interno', 'espessura',
            'comprimento', 'perfil_externo', 'perfil_interno', 'norma',
            'materia_prima', 'aco', 'fornecimento', 'superficie', 'faces', 'embalagem'
        ])
        return res

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        for record in self:
            self._update_reobote_custom_campo(record, [
                'codigo_cliente', 'diametro_externo', 'diametro_interno', 'espessura',
                'comprimento', 'perfil_externo', 'perfil_interno', 'norma',
                'materia_prima', 'aco', 'fornecimento', 'superficie', 'faces', 'embalagem'
            ])
        return res

    @api.onchange('concatenado')
    def _onchange_concatenado(self):
        if not self.concatenado:
            for campo in [
                'codigo_cliente', 'diametro_externo', 'diametro_interno', 'espessura',
                'comprimento', 'variacao', 'dint_tolerancia_maior', 'dint_tolerancia_menor',
                'dext_tolerancia_maior', 'dext_tolerancia_menor', 'comp_tolerancia_maior',
                'comp_tolerancia_menor', 'perfil_externo', 'perfil_interno', 'norma',
                'materia_prima', 'aco', 'fornecimento', 'superficie', 'faces', 'embalagem'
            ]:
                self[campo] = False
            return

        valores = [v.strip() for v in self.concatenado.split('|')]
        campos = [
            'codigo_cliente', 'diametro_externo', 'diametro_interno', 'espessura',
            'comprimento', 'variacao', 'dint_tolerancia_maior', 'dint_tolerancia_menor',
            'dext_tolerancia_maior', 'dext_tolerancia_menor', 'comp_tolerancia_maior',
            'comp_tolerancia_menor', 'perfil_externo', 'perfil_interno', 'norma',
            'materia_prima', 'aco', 'fornecimento', 'superficie', 'faces', 'embalagem'
        ]

        # Usar busca única para todos os valores
        reobote_customs = self.env['reobote.custom'].search([('name', 'in', valores)])
        reobote_customs_dict = {rc.name: rc for rc in reobote_customs}

        new_records_commands = []
        
        valores += [''] * (len(campos) - len(valores)) # Completa a lista de valores com strings vazias

        for i, campo in enumerate(campos):
            valor = valores[i] if i < len(valores) else ''
            if valor:
                reobote_custom = reobote_customs_dict.get(valor)
                if reobote_custom:
                    self[campo] = reobote_custom.id
                else:
                    # Comando para criar novo registro (adiado)
                    new_records_commands.append((0, 0, {'name': valor, 'campo': campo}))
                    self[campo]