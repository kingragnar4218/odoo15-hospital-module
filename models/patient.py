# -*- coding: utf-8 -*-
from sys import api_version

from odoo import api ,models, fields
from datetime import datetime , date


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"
    #_rec_name = "name"


    name = fields.Char(string="Patient Name" , tracking=True)

    date_of_birth = fields.Date(string="Date of Birth" , tracking=True  )

    ref = fields.Char(string="Reference" , tracking=True)
    # ref = fields.Char(string="Patient Reference")

    age = fields.Integer(string="Age" , compute="_compute_age" , tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender" , tracking=True)
    active = fields.Boolean(string="Active"  , default=True , tracking=True)
    appoinment_id = fields.Many2one('hospital.appoinment', string="Appoinment" , tracking=True)

    @api.depends('date_of_birth')
    #if here you don't import api from odoo so it give you internal server error when you restart server
    def _compute_age(self):
        ''' Compute age of patients '''
        for rec in self:
            if rec.date_of_birth:
                today = date.today()
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0


#Asctivate virtual environment :- source venv/bin/activate
# Password superadmin (database) in office system  : Md09kHHDNrfpoDnw
# Start Odoo service: sudo service odoo15-server start
# Stop Odoo service: sudo service odoo15-server stop
# Restart Odoo service: sudo service odoo15-server restart

