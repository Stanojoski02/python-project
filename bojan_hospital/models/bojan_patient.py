from odoo import models, fields


class BojanPatient(models.Model):
    _name = 'bojan.patient'
    _description = "This is model for Odoo16"

    name = fields.Char("Name:")
    surename = fields.Char("Surename")
    custom_field = fields.Integer(required=True)
