from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Definição dos campos Many2one
    codigo_cliente = fields.Many2one('reobote.custom', string="Código do Cliente", domain=[('campo', '=', 'codigo_cliente')])
    diametro_externo = fields.Many2one('reobote.custom', string="Diâmetro Externo", domain=[('campo', '=', 'diametro_externo')])
    diametro_externo_2 = fields.Many2one('reobote.custom', string="Diâmetro Externo 2", domain=[('campo', '=', 'diametro_externo_2')])
    diametro_interno = fields.Many2one('reobote.custom', string="Diâmetro Interno", domain=[('campo', '=', 'diametro_interno')])
    diametro_interno_2 = fields.Many2one('reobote.custom', string="Diâmetro Interno 2", domain=[('campo', '=', 'diametro_interno_2')])
    espessura = fields.Many2one('reobote.custom', string="Espessura", domain=[('campo', '=', 'espessura')])
    comprimento = fields.Many2one('reobote.custom', string="Comprimento", domain=[('campo', '=', 'comprimento')])
    variacao = fields.Many2one('reobote.custom', string="Variação", domain=[('campo', '=', 'variacao')])
    dint_tolerancia_maior = fields.Many2one('reobote.custom', string="+ (DI)", domain=[('campo', '=', 'dint_tolerancia_maior')])
    dint_tolerancia_menor = fields.Many2one('reobote.custom', string="- (DI)", domain=[('campo', '=', 'dint_tolerancia_menor')])
    dint2_toler_maior = fields.Many2one('reobote.custom', string="+ (DI2)", domain=[('campo', '=', 'dint2_toler_maior')])
    dint2_toler_menor = fields.Many2one('reobote.custom', string="- (DI2)", domain=[('campo', '=', 'dint2_toler_menor')])
    dext_tolerancia_maior = fields.Many2one('reobote.custom', string="+ (DE)", domain=[('campo', '=', 'dext_tolerancia_maior')])
    dext_tolerancia_menor = fields.Many2one('reobote.custom', string="- (DE)", domain=[('campo', '=', 'dext_tolerancia_menor')])
    dext2_toler_maior = fields.Many2one('reobote.custom', string="+ (DE2)", domain=[('campo', '=', 'dext2_toler_maior')])
    dext2_toler_menor = fields.Many2one('reobote.custom', string="- (DE2)", domain=[('campo', '=', 'dext2_toler_menor')])
    comp_tolerancia_maior = fields.Many2one('reobote.custom', string="+ (Comp)", domain=[('campo', '=', 'comp_tolerancia_maior')])
    comp_tolerancia_menor = fields.Many2one('reobote.custom', string="- (Comp)", domain=[('campo', '=', 'comp_tolerancia_menor')])
    esp_tolerancia_maior = fields.Many2one('reobote.custom', string="+ (E)", domain=[('campo', '=', 'esp_tolerancia_maior')])
    esp_tolerancia_menor = fields.Many2one('reobote.custom', string="- (E)", domain=[('campo', '=', 'esp_tolerancia_menor')])
    perfil_externo = fields.Many2one('reobote.custom', string="Perfil Externo", domain=[('campo', '=', 'perfil_externo')])
    perfil_interno = fields.Many2one('reobote.custom', string="Perfil Interno", domain=[('campo', '=', 'perfil_interno')])
    norma = fields.Many2one('reobote.custom', string="Norma", domain=[('campo', '=', 'norma')])
    materia_prima = fields.Many2one('reobote.custom', string="Matéria Prima", domain=[('campo', '=', 'materia_prima')])
    aco = fields.Many2one('reobote.custom', string="Aço", domain=[('campo', '=', 'aco')])
    fornecimento = fields.Many2one('reobote.custom', string="Fornecimento", domain=[('campo', '=', 'fornecimento')])
    superficie = fields.Many2one('reobote.custom', string="Superfície", domain=[('campo', '=', 'superficie')])
    faces = fields.Many2one('reobote.custom', string="Faces", domain=[('campo', '=', 'faces')])
    embalagem = fields.Many2one('reobote.custom', string="Embalagem", domain=[('campo', '=', 'embalagem')])
    obs = fields.Text(string="Observações")

    # Campo concatenado - usado como input
    concatenado = fields.Text(string="Concatenado")

    def _update_reobote_custom_campo(self, record, fields_to_update):
        """Atualiza o campo 'campo' na tabela reobote.custom."""
        for field_name in fields_to_update:
            if record[field_name]:
                custom = self.env['reobote.custom'].browse(record[field_name].id)
                if custom and custom.campo != field_name:
                    custom.write({'campo': field_name})
            else:
                # Busca o registro antigo antes da alteração
                old_record = record.read([field_name])[0]
                old_custom_id = old_record.get(field_name)
                if old_custom_id:
                    if isinstance(old_custom_id, tuple):
                        old_custom_id = old_custom_id[0]
                    custom = self.env['reobote.custom'].browse(old_custom_id)
                    if custom and custom.campo == field_name:
                        custom.write({'campo': False})

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
        if 'concatenado' in vals and vals['concatenado']:
            self.processar_concatenado(vals)

        res = super(ProductTemplate, self).write(vals)
        for record in self:
            self._update_reobote_custom_campo(record, [
                'codigo_cliente', 'diametro_externo', 'diametro_interno', 'espessura',
                'comprimento', 'perfil_externo', 'perfil_interno', 'norma',
                'materia_prima', 'aco', 'fornecimento', 'superficie', 'faces', 'embalagem'
            ])
        return res

    def processar_concatenado(self, vals):
        valores = [v.strip() for v in vals['concatenado'].split('|')]
        campos = [
            'codigo_cliente', 'diametro_externo', 'diametro_interno', 'espessura',
            'comprimento', 'variacao', 'dint_tolerancia_maior', 'dint_tolerancia_menor',
            'dext_tolerancia_maior', 'dext_tolerancia_menor', 'comp_tolerancia_maior',
            'comp_tolerancia_menor','esp_tolerancia_maior', 'esp_tolerancia_menor', 'perfil_externo', 'perfil_interno', 'norma',
            'materia_prima', 'aco', 'fornecimento', 'superficie', 'faces', 'embalagem'
        ]

        # Garante que 'valores' tenha pelo menos o mesmo número de elementos que 'campos'
        valores += [''] * (len(campos) - len(valores))
        
        # Adiciona list_price ao final
        campos.append('list_price')

        # Usar busca única para todos os valores
        reobote_customs = self.env['reobote.custom'].search([('name', 'in', valores)])
        reobote_customs_dict = {rc.name: rc for rc in reobote_customs}

        vals_to_write = {}
        for i, campo in enumerate(campos):
            valor = valores[i]
            if campo == 'list_price':
                try:
                    preco = float(valor)
                    vals_to_write['list_price'] = preco
                except ValueError:
                    pass
            elif valor:
                reobote_custom = reobote_customs_dict.get(valor)
                if reobote_custom:
                    vals_to_write[campo] = reobote_custom.id
                else:
                    # Cria um novo registro em 'reobote.custom'
                    new_custom = self.env['reobote.custom'].create({'name': valor, 'campo': campo})
                    vals_to_write[campo] = new_custom.id
            else:
                vals_to_write[campo] = False


        # Atualiza vals com os novos valores
        vals.update(vals_to_write)
        # Remove o campo 'concatenado' de vals
        del vals['concatenado']