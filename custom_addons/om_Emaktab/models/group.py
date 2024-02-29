from odoo import api, fields, models, _

class Group(models.Model):
    _name = "emaktab.group"
    _inherit = "mail.thread"
    _description = 'Emaktab Group'
    
    ref = fields.Char(string="Reference", default=lambda self: _('New Group'))
    course_name = fields.Char(string='Name', required=True, tracking=True)
    description = fields.Char(string='Description', tracking=True)
    student_id = fields.Many2many('emaktab.student','emaktab_group_table', 'student_id', 'group_id', string="Students")
    teacher_id = fields.Many2one('emaktab.teacher', string='Group Teacher')
    payment_id = fields.One2many('emaktab.income', 'group_id', string='Payments', readonly=True)
    
    #method so the name of the group gets returned as id + crouse_name in ui
    def name_get(self):
        return [(group.id, group.course_name) for group in self]
    
    # creating a serializer/sequence for this model's ref
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['ref'] = self.env['ir.sequence'].next_by_code('emaktab.group.list')
        return super(Group, self).create(vals_list)
    

    