from odoo import api, fields, models
import datetime

class CancelAppoinmentWizard(models.TransientModel):
    _name = 'cancel.appoinment.wizard'
    _description = 'Cancel Appoinment Wizard'

    @api.model
    def default_get(self , fields):
        #print("default get executed " , fields)
        res = super(CancelAppoinmentWizard , self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        return res


    appoinment_id = fields.Many2one(
        'hospital.appoinment',
        string='Appoinment',
        required=True
    )
    reason = fields.Text(string='Reason')
    date_cancel = fields.Date(string='Cancel Date')


    def action_cancel(self):
        return
