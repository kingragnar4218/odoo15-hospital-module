# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class HospitalAppoinment(models.Model):
    _name = "hospital.appoinment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appoinment"
    _rec_name = "patient_id"
    _order = 'id'

    # --------- declaration of fields start  ---------
    active = fields.Boolean(string="Active", default=True, tracking=True)
    patient_id = fields.Many2one('hospital.patient', string="Patient", ondelete='cascade', tracking=True)
    # here add readonly = True that's means you can not change that value if it false so you can change it
    gender = fields.Selection(related="patient_id.gender", readonly=False)
    # this field set default date to today
    appoinment_date = fields.Datetime(string="Appoinment Date", default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)
    ref = fields.Char(string="Reference", tracking=True)
    # here this field use html
    precreation = fields.Html(string="Precreation",  tracking=True)
    # priority widget
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High'),
    ], string="Priority")
    # statusbar
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled '),
    ], default="draft", string="status", required=True)
    doctor_id = fields.Many2one('res.users', string="Doctor", tracking=True)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appoinment_id')  # string="Pharmacy Lines"
    hide_sales_price = fields.Boolean(string="Hide Sales Price", tracking=True)
    operation_name = fields.Many2one('hospital.operation', string='Operation')
    progress = fields.Integer(string="Progress", compute='_compute_progress', store=True )
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',related='company_id.currency_id',store=True,readonly=True)
    total_amount = fields.Monetary(string="Total Amount", compute="_compute_total_amount", store=True,currency_field='currency_id')

    # --------- declaration of fields finish ---------

    # --------- declaration of function start ---------
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def unlink(self):
        print("check for demo ________________________________________")

        if self.state != 'draft':
            raise ValidationError(_("You cannot delete an appointment in Done state"))

        return super(HospitalAppoinment, self).unlink()

    def action_test(self):
        print("button clickkkkkkkkkkk")
        return{
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': 'https://www.itsedgar.tech/',
        }
        # return {
        #     'effect': {
        #         'fadeout': 'slow',
        #         'message': 'Click Successfull',
        #         'type': 'rainbow_man',
        #     }
        #}

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        # for rec in self:
        #     rec.state = 'cancel'
        action = self.env.ref('ht_hospital.action_cancel_appoinment')
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.depends('state')
    def _compute_progress(self):
        ''' progressbar method  '''
        for rec in self:
            if rec.state == 'draft':
                progress = 25
            elif rec.state == 'in_consultation':
                progress = 50
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress

    #total amount method
    @api.depends('pharmacy_line_ids.price_subtotal')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(
                rec.pharmacy_line_ids.mapped('price_subtotal')
            )

    # --------- declaration of function finish---------
# new model
# class AppointmentPharmacyLines(models.Model):
#     _name = 'appointment.pharmacy.lines'
#     _description = 'Appointment Pharmacy Lines'
#
#     product_id = fields.Many2one('product.product', string='Product', required=True)
#     price_unit = fields.Float(string='Price')
#     qty = fields.Integer(string='Quantity')
#     appoinment_id = fields.Many2one('hospital.appoinment', string="Appoinment")
#     currency_id = fields.Many2one('res.currency', related='company_id.currency_id', store=True, readonly=True)
#     price_subtotal = fields.Monetary(string='SubTotal')

# https://apps.odoo.com/apps/modules/15.0/om_hospital


class AppointmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.lines'
    _description = 'Appointment Pharmacy Lines'

    appoinment_id = fields.Many2one(
        'hospital.appoinment',
        string="Appoinment",
        ondelete='cascade'
    )

    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True
    )

    price_unit = fields.Float(string='Price')

    qty = fields.Integer(
        string='Quantity',
        default=1
    )

    currency_id = fields.Many2one(
        'res.currency',
        related='appoinment_id.currency_id',
        store=True,
        readonly=True
    )

    price_subtotal = fields.Monetary(
        string='SubTotal',
        compute='_compute_price_subtotal',
        store=True,
        currency_field='currency_id'
    )

    @api.depends('price_unit', 'qty')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.price_unit * line.qty