from odoo import api, fields, models, _

class Student(models.Model):
    _name = "emaktab.student"
    _inherit = "mail.thread"
    _description = 'Emaktab Student'
    
    ref = fields.Char(string="Reference", default=lambda self: _('New Student'))
    name = fields.Char(string='Name', required=True, tracking=True)
    surname = fields.Char(string='Surname', required=True,tracking=True)
    dateofbirth = fields.Date(string='Date Of Birth', required=True,tracking=True)
    phone = fields.Char(string='Phone Number',tracking=True)
    email = fields.Char(string='Email',tracking=True)
    gender = fields.Selection([('male','Male'),('female','Female')],string='Gender',tracking=True)
    group_id = fields.Many2many('emaktab.group','emaktab_group_table', 'group_id','student_id', string="Groups")
    payment_id = fields.One2many('emaktab.income', 'student_id', string='Payments', readonly=True)

    # creating a serializer/sequence for this model's ref
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['ref'] = self.env['ir.sequence'].next_by_code('emaktab.student.list')
        return super(Student, self).create(vals_list)
    

    
    
    
    