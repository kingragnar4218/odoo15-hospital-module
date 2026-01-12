from odoo import api, fields, models , _

class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string='Color')
    #color_2 = fields.Char(string='Color 2', required=True)
    sequence = fields.Integer(string='Sequence')

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}

        if not default.get('name'):
            default['name'] =_("%s (copy)" % self.name)

        default['sequence'] = 10

        return super(PatientTag, self).copy(default)



    _sql_constraints = [
        #here create unique tag name if you create same name tag so it show massage this
        ('unique_tag_unique', 'UNIQUE (name)', 'name must be unique'),
        ('check_sequence', 'CHECK(sequence > 0 )', 'sequence must be greater than 0'),

    ]


