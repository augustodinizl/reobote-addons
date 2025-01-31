from odoo import fields, models

class ReoboteMRPCustom(models.Model):
    _name = 'reobote.mrp.custom'
    _description = 'Reobote MRP Custom'

    name = fields.Char()

    campo = fields.Char()

    valor = fields.Char()