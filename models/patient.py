from odoo import api ,models, fields , _
from datetime import datetime , date
from odoo.exceptions import ValidationError


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
    tag_ids = fields.Many2many('patient.tag',  string="Tags")
    image = fields.Image(string="Image" , tracking=True)

    appointment_count = fields.Integer(string="Appointment Count", compute="_compute_appointment_count",store=True)

    appointment_ids = fields.One2many('hospital.appoinment','patient_id',string="Appointments")

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appoinment'].search_count([
                ('patient_id', '=', rec.id)
            ])

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

    @api.constrains('date_of_birth')
    def check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("The entered date of birth is not acceptable !"))



    @api.model
    def create(self , vals):
        ''' override methods demoo   and sequence_data '''
        # print(".........", self.env['ir.sequence'])
        vals['ref']=self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient , self).create(vals)

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).write(vals)

    # def name_get(self):
    #     patient_list = []
    #     for record in self:
    #         name = record.ref + record.name
    #         patient_list.append((record.id, name))
    #     return patient_list

    def name_get(self):
        return [(record.id , "[%s]:%s" % (record.ref, record.name)) for record in self ]

    # def name_get(self):
    #     result = []
    #     for record in self:
    #         if record.ref:
    #             display_name = f"[{record.ref}] {record.name}"
    #         else:
    #             display_name = record.name
    #         result.append((record.id, display_name))
    #     return result

#Asctivate virtual environment :- source venv/bin/activate
# Password superadmin (database) in office system  : Md09kHHDNrfpoDnw
# Start Odoo service: sudo service odoo15-server start
# Stop Odoo service: sudo service odoo15-server stop
# Restart Odoo service: sudo service odoo15-server restart

