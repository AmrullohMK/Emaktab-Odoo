from odoo import api, fields, models, _
from datetime import datetime, timedelta

class Income(models.Model):
    _name = "emaktab.income"
    _inherit = "mail.thread"
    _description = 'Emaktab Income'
    _rec_name = 'ref'
    
    ref = fields.Char(string="Reference", default=lambda self: _('New Income'))
    cheque = fields.Char(string="Cheque Number",tracking=True, required=True)
    currency_id = fields.Many2one("res.currency", string='Currency',tracking=True,required=True)
    amount = fields.Monetary(string='Payment Amount',tracking=True,required=True)
    comment = fields.Char(string="Comment",tracking=True)
    student_id = fields.Many2one('emaktab.student', string='Payment From Student',required=True)
    status = fields.Selection([('inreview','In Review'),('accepted','Accepted'),('rejected',"Rejected")],string='Status',tracking=True, default='inreview', 
                              readonly=True)
    group_id = fields.Many2one('emaktab.group', string='Group')
    is_within_last_7_days = fields.Boolean(string='Within Last 7 Days', compute='_compute_within_last_7_days',store=True)
    
    #accept button method to change status, sudo is used to bypass administrator group's inability to write/edit, admin can use the button without sudo
    def action_accept(self):
        self.sudo().write({'status': 'accepted'})
        
    #reject button method to change status
    def action_reject(self):
        self.sudo().write({'status': 'rejected'})
        
    #displays the selection options of the group_id based on the student_id selected
    @api.onchange('student_id')
    def _onchange_student_id(self):
        if self.student_id:
            # Update the domain of group_id based on the selected student
            return {'domain': {'group_id': [('id', 'in', self.student_id.group_id.ids)]}}
        else:
            # If no student is selected, reset the domain of group_id
            return {'domain': {'group_id': []}}
    #serialzer for ref
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['ref'] = self.env['ir.sequence'].next_by_code('emaktab.income.list')
        return super(Income, self).create(vals_list)
    #used to track if the object was created within 7 days, so the administrator can only view it
    @api.depends('create_date')
    def _compute_within_last_7_days(self):
        for record in self:
            create_date = fields.Datetime.from_string(record.create_date)
            seven_days_ago = datetime.now() - timedelta(days=7)
            record.is_within_last_7_days = create_date >= seven_days_ago
    

#only admin can access spending model   
class Spending(models.Model):
    _name = "emaktab.spending"
    _inherit = "mail.thread"
    _description = 'Emaktab Spendings'
    _rec_name = 'ref'
    
    ref = fields.Char(string="Reference", default=lambda self: _('New Spending'))
    cheque = fields.Char(string="Cheque Number",tracking=True)
    currency_id = fields.Many2one("res.currency", string='Currency',tracking=True)
    amount = fields.Monetary(string='Payment Amount',tracking=True)
    comment = fields.Char(string="Comment",tracking=True)
    teacher_id = fields.Many2one('emaktab.teacher', string='Payment To Teacher')
    status = fields.Selection([('inreview','In Review'),('accepted','Accepted'),('rejected',"Rejected")],string='Status',tracking=True, default='inreview', readonly=True)
    
    def action_accept(self):
        self.status = 'accepted'
        
    def action_reject(self):
        self.status = 'rejected'
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['ref'] = self.env['ir.sequence'].next_by_code('emaktab.spending.list')
        return super(Spending, self).create(vals_list)