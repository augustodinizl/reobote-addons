from odoo import fields, models, api

class ReoboteLotMany(models.Model):
    _name = 'reobote.lot.many'
    _description = 'Reobote LOT Many'

    # Definição dos campos Many2one
    especificacao = fields.Many2one('reobote.mrp.custom', string="Especificação", domain=[('campo', '=', 'especificacao')])
    unidade = fields.Many2one('reobote.mrp.custom', string="Unidade", domain=[('campo', '=', 'controle')])
    ref_min = fields.Many2one('reobote.mrp.custom', string="Referência Mín.", domain=[('campo', '=', 'ref_min')])
    ref_max = fields.Many2one('reobote.mrp.custom', string="Referência Máx.", domain=[('campo', '=', 'ref_max')])
    enc_1 = fields.Many2one('reobote.mrp.custom', string="Encontrado 1", domain=[('campo', '=', 'enc_1')])
    enc_2 = fields.Many2one('reobote.mrp.custom', string="Encontrado 2", domain=[('campo', '=', 'enc_2')])
    avaliacao = fields.Many2one('reobote.mrp.custom', string="Avaliação", domain=[('campo', '=', 'avaliacao')])

    def _update_reobote_mrp_custom_campo(self, record, fields_to_update):
        """Atualiza o campo 'campo' na tabela reobote.mrp.custom."""
        for field_name in fields_to_update:
            if record[field_name]:
                custom = self.env['reobote.mrp.custom'].browse(record[field_name].id)
                if custom and custom.campo != field_name:
                    custom.write({'campo': field_name})
            else:
                old_record = record.read([field_name])[0]
                old_custom_id = old_record.get(field_name)
                if old_custom_id:
                    if isinstance(old_custom_id, tuple):
                        old_custom_id = old_custom_id[0]
                    custom = self.env['reobote.mrp.custom'].browse(old_custom_id)
                    if custom and custom.campo == field_name:
                        custom.write({'campo': False})

    @api.model
    def create(self, vals):
        res = super(ReoboteLotMany, self).create(vals)  # Correção do super()
        self._update_reobote_mrp_custom_campo(res, [
            'especificacao', 'requisitos', 'controle', 'frequencia', 'referencia', 'encontrado', 'instrumento'
        ])
        return res

    def write(self, vals):
        res = super(ReoboteLotMany, self).write(vals)  # Correção do super()
        for record in self:
            self._update_reobote_mrp_custom_campo(record, [
                'especificacao', 'requisitos', 'controle', 'frequencia', 'referencia', 'encontrado', 'instrumento'
        return res