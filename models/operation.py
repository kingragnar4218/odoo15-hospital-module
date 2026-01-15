from odoo import api, fields, models, _


class HospitalOperation(models.Model):
    _name = 'hospital.operation'
    _description = "Hospital Operation"
    _log_access = False

    doctor_id = fields.Many2one('res.users',string='Doctor')
    operation_name = fields.Char(string='Operation Name')
    reference = fields.Reference( [('hospital.patient' , 'patient'),('hospital.appoinment' , 'appoinment')], string='Recode')

    @api.model
    def name_create(self, name):
        print("entered value -------->", name)
        return self.create({'operation_name': name}).name_get()[0]
