# -*- coding: utf-8 -*-
from odoo import models, fields

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"

    name = fields.Char(string="Patient Name")
    ref = fields.Char(string="Reference")
    # ref = fields.Char(string="Patient Reference")

    age = fields.Integer(string="Age")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender")
    active = fields.Boolean(string="Active"  , default=True)

    


#Asctivate virtual environment :- source venv/bin/activate
# Password superadmin (database): Md09kHHDNrfpoDnw
# Start Odoo service: sudo service odoo15-server start
# Stop Odoo service: sudo service odoo15-server stop
# Restart Odoo service: sudo service odoo15-server restart

