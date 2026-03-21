from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = create_date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline and offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days

    def action_accept(self):
        for offer in self:
            offer_ids = offer.property_id.offer_ids.filtered(lambda o: o.id != offer.id and o.status == 'accepted')
            if offer_ids:
                raise UserError("Another offer has already been accepted for this property.")
            if offer.partner_id:
                offer.property_id.buyer_id = offer.partner_id.id
                offer.property_id.selling_price = offer.price
                offer.status = 'accepted'

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
