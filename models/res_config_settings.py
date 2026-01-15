from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # --------- declaration of fields start  ---------
    cancel_days = fields.Integer(string='Cancel Days' , config_parameter='ht_hospital.cancel_days')
    # --------- declaration of fields finish  ---------