from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

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

    active = fields.Boolean(default=True)

    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        copy=False,
        default="new",
    )

    property_type_id = fields.Many2one(comodel_name="estate.property.type", string="Property Type")

    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)

    salesperson_id = fields.Many2one(comodel_name="res.users", string="Salesperson", default=lambda self: self.env.user, copy=False)

    tag_ids = fields.Many2many(comodel_name="estate.property.tag", string="Tags")

    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id", string="Offers")

    total_area = fields.Float(string="Total Area", compute="_compute_total_area")

    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    _check_expected_price = models.Constraint(
        'CHECK(expected_price >= 0)',
        'Expected price must be positive.'
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'Selling price must be positive.'
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0.0

    @api.onchange('garden')
    def _onchange_enabled_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def mark_as_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("You cannot sell a cancelled property.")
            record.state = 'sold'

    def mark_as_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("You cannot cancel a sold property.")
            record.state = 'cancelled'

    @api.constrains('selling_price', 'expected_price')
    def _check_price_validity(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue  # Allow zero selling price (not sold yet)

            min_price = record.expected_price * 0.9
            if float_compare(record.selling_price, min_price, precision_digits=2) < 0:
                raise UserError(_("The selling price cannot be less than 90%% of the expected price."))
