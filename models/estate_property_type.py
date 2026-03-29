# -*- coding: utf-8 -*-
from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence')

    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_type_id', string='Properties')

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'Property type name must be unique.'
    )
