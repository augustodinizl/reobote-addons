from odoo import fields, models

class ReoboteMRPCustom(models.Model):
    _name = 'reobote.mrp.custom'
    _description = 'Reobote MRP Custom'

    name = fields.Char()

    campo = fields.Char()

    valor = fields.Char()

    campo = fields.Selection(
		selection=[('lote', 'Lote'), ('quimica', 'Química'), ('processo', 'Processo'), ('reducao', 'Redução'),
				   ('perdas', 'Perdas')],
		string="Campo",
		help="Campo ao qual este registro se refere"
	)

_sql_constraints = [
    ('name_uniq', 'unique (name)', 'Já existe um registro com este nome!')
]