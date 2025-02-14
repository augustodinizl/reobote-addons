from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64

class MrpProductionReobote(models.Model):
    _inherit = 'mrp.production'

    # --- Campos existentes ---
    lote_ok = fields.Many2one('reobote.mrp.custom', string="LOTE?", domain=[('campo', '=', 'lote')])
    quimica_ok = fields.Many2one('reobote.mrp.custom', string="QUÍMICA?", domain=[('campo', '=', 'quimica')])
    processo_ok = fields.Many2one('reobote.mrp.custom', string="PROCESSO?", domain=[('campo', '=', 'processo')])
    reducao = fields.Many2one('reobote.mrp.custom', string="REDUÇÃO", domain=[('campo', '=', 'reducao')])
    perdas = fields.Many2one('reobote.mrp.custom', string="PERDAS", domain=[('campo', '=', 'perdas')])
    obs = fields.Html(string="Observações")

    # --- Campos para o certificado (Mantenha) ---
    certificado_qualidade = fields.Binary(string="Certificado de Qualidade", attachment=True, readonly=True,
        help="Certificado de qualidade gerado automaticamente.")
    certificado_qualidade_nome = fields.Char(string="Nome do Arquivo", readonly=True)
    show_generate_button = fields.Boolean(string='Mostrar Botão Gerar Certificado', compute='_compute_show_button')

    # --- Métodos existentes ---
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

    # --- Método para gerar o certificado (Mantenha) ---
    def gerar_certificado_qualidade(self):
        if self.state != 'done':
            raise UserError(_("A ordem de produção deve estar no estado 'Concluído' para gerar o certificado."))

        report_name = 'mrp_custom_reobote.report_certificado_qualidade'  # Nome do SEU módulo!
        pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(report_name, self.ids)

        filename = "Certificado_Qualidade_MO_{}.pdf".format(self.name)

        self.write({
            'certificado_qualidade': base64.b64encode(pdf_content),
            'certificado_qualidade_nome': filename,
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/mrp.production/{}/certificado_qualidade/{}?download=true'.format(self.id, filename),
            'target': 'new',
            'res_id': self.id,
        }

    # --- Método para controlar a visibilidade do botão (Mantenha) ---
    @api.depends('state')
    def _compute_show_button(self):
        for record in self:
            if record.state == 'done':
                record.show_generate_button = True
            else:
                record.show_generate_button = False