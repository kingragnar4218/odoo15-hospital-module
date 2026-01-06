# -*- coding: utf-8 -*-
from odoo import api ,models, fields

class HospitalAppoinment(models.Model):
    _name = "hospital.appoinment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appoinment"

    patient_id = fields.Many2one('hospital.patient' , string="Patient")

    #here add readonly = True that's means you can not change that value if it false so you can change it
    gender = fields.Selection(related="patient_id.gender" , readonly=False)

    #this field set default date to today
    appoinment_date = fields.Datetime(string="Appoinment Date" , default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date" , default=fields.Date.context_today)
    ref = fields.Char(string="Reference", tracking=True)

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref