from odoo import api, models, fields, _
import datetime
from datetime import date
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class CancelAppoinmentWizard(models.TransientModel):
    _name = 'cancel.appoinment.wizard'
    _description = 'Cancel Appoinment Wizard'

    # --------- declaration of fields start  ---------
    appoinment_id = fields.Many2one(
        'hospital.appoinment',
        string='Appoinment',
        required=True,
        # here this domain is for demo only it one of the add filter only
        # domain=['|',('state','=','draft') , ('priority' , 'in' ,('0' ,'1'))]
    )

    reason = fields.Text(string='Reason')
    date_cancel = fields.Date(string='Cancel Date')

    # --------- declaration of fields finish  ---------

    # --------- declaration of function start ---------
    @api.model
    def default_get(self, fields):
        #print("default get executed ", fields)
        res = super(CancelAppoinmentWizard, self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        return res


    # def action_cancel(self):
    #     if self.appoinment_id.booking_date == fields.Date.today():
    #         raise ValidationError('You cannot cancel the appoinment')
    #     self.appoinment_id.state = 'cancel'
    #     return

    def action_cancel(self):
        cancel_day = self.env['ir.config_parameter'].sudo().get_param('om_hospital.cancel_day')
        allowed_date = self.appoinment_id.booking_date - relativedelta(days=int(cancel_day))
        if allowed_date < date.today():
            raise ValidationError(_("Sorry, cancellation is not allowed for this booking!"))
        self.appoinment_id.state = 'cancel'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    # --------- declaration of function start ---------