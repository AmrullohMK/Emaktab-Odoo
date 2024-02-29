from odoo import api, fields, models, _


class Teacher(models.Model):
    _name = "emaktab.teacher"
    _inherit = "mail.thread"
    _description = 'Emaktab Teacher'
    
    ref = fields.Char(string="Reference", default=lambda self: _('New Teacher'))
    name = fields.Char(string='Name', required=True, tracking=True)
    surname = fields.Char(string='Surname', required=True,tracking=True)
    dateofbirth = fields.Date(string='Date Of Birth', required=True,tracking=True)
    phone = fields.Char(string='Phone Number',tracking=True)
    email = fields.Char(string='Email',tracking=True)
    gender = fields.Selection([('male','Male'),('female','Female')],string='Gender',tracking=True)
    group_id = fields.One2many('emaktab.group', 'teacher_id',string='Groups')
    payment_id = fields.One2many('emaktab.spending', 'teacher_id', string='Payments', readonly=True)
    
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['ref'] = self.env['ir.sequence'].next_by_code('emaktab.teacher.list')
        return super(Teacher, self).create(vals_list)
    
