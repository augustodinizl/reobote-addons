from odoo import models, fields

class MrpRoutingWorkcenterReobote(models.Model):
    _name = 'mrp.routing.workcenter.reobote'
    _inherit = 'mrp.routing.workcenter'

    requisito = fields.Many2one('mrp.workorder', string="Requisito", domain="[('routing_id', '=', id)]")
    controle = fields.Many2one('mrp.workorder', string="Controle", domain="[('routing_id', '=', id)]")
    frequencia = fields.Many2one('mrp.workorder', string="Frequência", domain="[('routing_id', '=', id)]")
    referencia = fields.Many2one('mrp.workorder', string="Referência", domain="[('routing_id', '=', id)]")
    encontrado = fields.Many2one('mrp.workorder', string="Encontrado", domain="[('routing_id', '=', id)]")
    instrumento = fields.Many2one('mrp.workorder', string="Instrumento", domain="[('routing_id', '=', id)]")
    obs = fields.Html(string="Observações")