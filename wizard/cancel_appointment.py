from odoo import api, fields, models
import datetime
from odoo.exceptions import ValidationError


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
        required=True,
        #here this domain is for demo only it one of the add filter only
        #domain=['|',('state','=','draft') , ('priority' , 'in' ,('0' ,'1'))]

    )
    reason = fields.Text(string='Reason')
    date_cancel = fields.Date(string='Cancel Date')


    def action_cancel(self):
        if self.appoinment_id.booking_date == fields.Date.today() :
            raise ValidationError('You cannot cancel the appoinment')
        self.appoinment_id.state='cancel'
        return
