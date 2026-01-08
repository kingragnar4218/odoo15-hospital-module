from odoo import fields, models

class CancelAppoinmentWizard(models.TransientModel):
    _name = 'cancel.appoinment.wizard'
    _description = 'Cancel Appoinment Wizard'

    appoinment_id = fields.Many2one(
        'hospital.appoinment',
        string='Appoinment',
        required=True
    )

    def action_cancel(self):
        return
