from odoo import api ,models, fields , _
from datetime import datetime , date
from odoo.exceptions import ValidationError
from dateutil import relativedelta



class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"
    #_rec_name = "name"

    #--------- declaration of fields start  ---------
    name = fields.Char(string="Patient Name" , tracking=True)
    date_of_birth = fields.Date(string="Date of Birth" , tracking=True  )
    ref = fields.Char(string="Reference" , tracking=True)
    # ref = fields.Char(string="Patient Reference")
    age = fields.Integer(string="Age" , compute="_compute_age" , search="_search_age" , tracking=True)
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
    parent= fields.Char(string="Parent Name" , tracking=True)
    marital_status = fields.Selection([('married' , 'Married'), ('single' , 'Single') ], string="Marital Status", tracking=True)
    partner_name = fields.Char(string="Partner Name" , tracking=True)
    is_birthday = fields.Boolean(string="Is Birthday" , tracking=True , compute="_compute_is_birthday")
    phone = fields.Char(string="Phone Number" , tracking=True)
    email = fields.Char(string="Email" , tracking=True)
    website = fields.Char(string="Website" , tracking=True)

    # --------- declaration of fields finish   ---------

    # --------- declaration of function start ---------

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        # here you also inverse function see video in youtube :--- [99.add How To Set Inverse Function For Computed Field In Odoo]
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

    def _search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_of_year) , ('date_of_birth', '<=', end_of_year)]

    @api.constrains('date_of_birth')
    def check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("The entered date of birth is not acceptable !"))

    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(
                    _("You cannot delete patient with appointments!"))

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

    def action_test(self):
        print("click.....action test")
        return

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

    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if (
                        today.day == rec.date_of_birth.day
                        and today.month == rec.date_of_birth.month
                ):
                    is_birthday = True
            rec.is_birthday = is_birthday

    # --------- declaration of function finish ---------


#Asctivate virtual environment :- source venv/bin/activate
# Password superadmin (database) in office system  : Md09kHHDNrfpoDnw
# Start Odoo service: sudo service odoo15-server start
# Stop Odoo service: sudo service odoo15-server stop
# Restart Odoo service: sudo service odoo15-server restart

