from odoo import fields, models

class ReoboteCustom(models.Model):
    _name = 'reobote.custom'
    _description = 'Reobote Custom'

    name = fields.Char()

    campo = fields.Char()

    valor = fields.Char()
