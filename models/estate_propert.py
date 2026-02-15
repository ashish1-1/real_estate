from odoo import models, fields
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Title", required=True)

    description = fields.Text(string="Description")

    postcode = fields.Char(string="Postcode")

    date_availability = fields.Date(string="Available From", copy=False, default=fields.Date.today()+ relativedelta(months=3))

    expected_price = fields.Float(string="Expected Price", required=True)

    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)

    bedrooms = fields.Integer(string="Bedrooms", default=2)

    living_area = fields.Integer(string="Living Area (sqm)")

    facades = fields.Integer(string="Facades")

    garage = fields.Boolean(string="Garage")

    garden = fields.Boolean(string="Garden")

    garden_area = fields.Integer(string="Garden Area")

    garden_orientation = fields.Selection([('north','North'),('south','South'),('east','East'),('west','West')], string="Garden Orientation")

    property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('villa', 'Villa')
    ], string="Property Type")

    active = fields.Boolean(default=True)

    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        copy=False,
        default="new",
    )
