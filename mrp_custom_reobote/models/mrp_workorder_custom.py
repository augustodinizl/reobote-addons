from odoo import fields, models, api

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    # Definição dos campos Many2one
    requisitos = fields.Many2one('reobote.mrp.custom', string="Requisitos", domain=[('campo', '=', 'requisitos')])
    controle = fields.Many2one('reobote.mrp.custom', string="Controle", domain=[('campo', '=', 'controle')])
    frequencia = fields.Many2one('reobote.mrp.custom', string="Frequência", domain=[('campo', '=', 'frequencia')])
    referencia = fields.Many2one('reobote.mrp.custom', string="Referência", domain=[('campo', '=', 'referencia')])
    encontrado = fields.Many2one('reobote.mrp.custom', string="Encontrado", domain=[('campo', '=', 'encontrado')])
    instrumento = fields.Many2one('reobote.mrp.custom', string="Instrumento", domain=[('campo', '=', 'instrumento')])
    obs = fields.Html(string="Observações")

    routing_workcenter_reobote_id = fields.Many2one('mrp.routing.workcenter.reobote', string="Roteamento Reobote")

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
        res = super(MrpWorkorder, self).create(vals)
        self._update_reobote_mrp_custom_campo(res, [
            'requisitos', 'controle', 'frequencia', 'referencia', 'encontrado', 'instrumento'
        ])
        res._preencher_campos_reobote() # Preenche após a criação
        return res

    def write(self, vals):
        res = super(MrpWorkorder, self).write(vals)
        for record in self:
            self._update_reobote_mrp_custom_campo(record, [
                'requisitos', 'controle', 'frequencia', 'referencia', 'encontrado', 'instrumento'
            ])
            record._preencher_campos_reobote()  # Preenche após a edição
        return res

    def _preencher_campos_reobote(self):
        if self.routing_workcenter_reobote_id:
            self.requisitos = self.routing_workcenter_reobote_id.requisitos
            self.controle = self.routing_workcenter_reobote_id.controle
            self.frequencia = self.routing_workcenter_reobote_id.frequencia
            self.referencia = self.routing_workcenter_reobote_id.referencia
            self.encontrado = self.routing_workcenter_reobote_id.encontrado
            self.instrumento = self.routing_workcenter_reobote_id.instrumento
            self.obs = self.routing_workcenter_reobote_id.obs

    @api.onchange('routing_workcenter_reobote_id')
    def _onchange_routing_workcenter_reobote(self):
        self._preencher_campos_reobote()