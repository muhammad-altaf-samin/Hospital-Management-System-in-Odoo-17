from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread']
    _description = 'Patient Master'

    name = fields.Char(string = 'Patient Name', required=True, tracking=True)
    date_of_birth = fields.Date(string = 'Date of Birth', tracking=True)
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True
    )
    tag_ids = fields.Many2many(
        'patient.tag', 'patient_tag_rel', 'patient_id', 'tag_id', string='Tags'
    )
    is_minor = fields.Boolean(string='Minor')
    guardian = fields.Char(string='Guardian')
    weight = fields.Float(string='Weight')

    @api.ondelete(at_uninstall=False)
    def _check_patient_appointment(self):
        for rec in self:
            domain = [('patient_id', '=', rec.id)]
            appointments = self.env['hospital.appointment'].search(domain)
            if appointments:
                raise ValidationError(_("You cannot delete this patient. An appointment for this patient exists."))