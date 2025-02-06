from odoo import models, fields, api

class MrpProductionReobote(models.Model):
    _inherit = 'mrp.production'

    lote_ok = fields.Many2one('reobote.mrp.custom', string="LOTE?", domain=[('campo', '=', 'lote')])
    quimica_ok = fields.Many2one('reobote.mrp.custom', string="QUÍMICA?", domain=[('campo', '=', 'quimica')])
    processo_ok = fields.Many2one('reobote.mrp.custom', string="PROCESSO?", domain=[('campo', '=', 'processo')])
    reducao = fields.Many2one('reobote.mrp.custom', string="REDUÇÃO", domain=[('campo', '=', 'reducao')])
    perdas = fields.Many2one('reobote.mrp.custom', string="PERDAS", domain=[('campo', '=', 'perdas')])
    obs = fields.Html(string="Observações")

    def _update_reobote_mrp_custom_campo(self, record, fields_to_update):
        """Atualiza o campo 'campo' na tabela reobote.mrp.custom."""
        for field_name in fields_to_update:
            if record[field_name]:
                custom = self.env['reobote.mrp.custom'].browse(record[field_name].id)
                if custom and custom.campo != field_name:
                    custom.write({'campo': field_name})
            else:
                # Busca o registro antigo antes da alteração
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
        res = super(MrpProductionReobote, self).create(vals)
        self._update_reobote_mrp_custom_campo(res, [
            'lote_ok', 'quimica_ok', 'processo_ok', 'reducao', 'perdas'
        ])
        return res

    def write(self, vals):
        res = super(MrpProductionReobote, self).write(vals)
        for record in self:
            self._update_reobote_mrp_custom_campo(record, [
                'lote_ok', 'quimica_ok', 'processo_ok', 'reducao', 'perdas'
            ])
        return res