from odoo import models, fields, api, _
from odoo.exceptions import UserError  # Importe UserError
import base64 #Importe isso

class MrpProductionReobote(models.Model):
    _inherit = 'mrp.production'

    # --- Campos existentes ---
    lote_ok = fields.Many2one('reobote.mrp.custom', string="LOTE?", domain=[('campo', '=', 'lote')])
    quimica_ok = fields.Many2one('reobote.mrp.custom', string="QUÍMICA?", domain=[('campo', '=', 'quimica')])
    processo_ok = fields.Many2one('reobote.mrp.custom', string="PROCESSO?", domain=[('campo', '=', 'processo')])
    reducao = fields.Many2one('reobote.mrp.custom', string="REDUÇÃO", domain=[('campo', '=', 'reducao')])
    perdas = fields.Many2one('reobote.mrp.custom', string="PERDAS", domain=[('campo', '=', 'perdas')])
    obs = fields.Html(string="Observações")

    # --- Campos para o certificado (Mantenha, mas agora eles não são readonly) ---
    certificado_qualidade = fields.Binary(string="Certificado de Qualidade", attachment=True,
        help="Certificado de qualidade (gerado ao imprimir).")  # Remova readonly=True
    certificado_qualidade_nome = fields.Char(string="Nome do Arquivo") # Remova readonly=True


    # --- Métodos existentes (modificados para não dar conflito) ---
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

    # --- REMOVA o método gerar_certificado_qualidade ---
    # --- REMOVA o método _compute_show_button e o campo show_generate_button ---