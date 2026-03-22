# -*- coding: utf-8 -*-
from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(string='Name', required=True)

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'Property type name must be unique.'
    )
