from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from lxml import etree

class SampleSubmission(models.Model):
    _name = 'sample.submission'
    _description = 'Sample Submission'

    name = fields.Char('Name', required=True)
    sequence = fields.Char('Sequence', readonly=True)
    customer_id = fields.Many2one('res.partner', string='Customer')
    submission_date = fields.Date('Date of Submission', default=fields.Date.context_today)
    description = fields.Text('Description')
    price = fields.Float('Price')
    stage = fields.Selection([
        ('pending', 'Pending'),
        ('doing', 'Doing'),
        ('completed', 'Completed')
    ], default='pending', string='Stage')
    invoiced = fields.Boolean('Invoiced', default=False)
    material_line_ids = fields.One2many('sample.submission.material', 'submission_id', string='Materials')
    discount = fields.Float('Discount')
    vat = fields.Char(string='GSTIN')
    confirmed_date = fields.Date('Date of Confirmation')
    complete_date = fields.Date('Date of Completion')
    collected_payment = fields.Float(string='Collected Payment', compute='_compute_collected_payment')
    balance = fields.Float(string='Balance', compute='_compute_balance')
    total_product_qty = fields.Float(string='Total Product Quantity', compute='_compute_total_product_qty')
    sum_cost = fields.Float(string='Sum of Cost', compute='_compute_sum_cost')
    profit = fields.Float(string='Profit', compute='_compute_profit')
    invoice_id = fields.Many2one('account.move', string='Invoice')

    @api.depends('invoice_id')
    def _compute_collected_payment(self):
        for record in self:
            record.collected_payment = record.invoice_id.amount_total if record.invoice_id else 0.0

    @api.depends('invoice_id', 'collected_payment')
    def _compute_balance(self):
        for record in self:
            record.balance = record.price - record.collected_payment

    @api.depends('material_line_ids.quantity')
    def _compute_total_product_qty(self):
        for record in self:
            record.total_product_qty = sum(line.quantity for line in record.material_line_ids)

    @api.depends('material_line_ids.product_id.standard_price', 'material_line_ids.quantity')
    def _compute_sum_cost(self):
        for record in self:
            record.sum_cost = sum(line.product_id.standard_price * line.quantity for line in record.material_line_ids)

    @api.depends('price', 'sum_cost')
    def _compute_profit(self):
        for record in self:
            record.profit = record.price - record.sum_cost

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('sample.submission') or '/'
        return super(SampleSubmission, self).create(vals)

    @api.onchange('customer_id')
    def onchange_customer_id(self):
        for rec in self:
            rec.vat = rec.customer_id and rec.customer_id.vat or False

    @api.constrains('submission_date')
    def _check_submission_date(self):
        for rec in self:
            if rec.submission_date:
                if rec.submission_date > fields.Date.context_today(self):
                    raise ValidationError(_('Sorry, Date cannot be a future date.'))

    def confirm_submission(self):
        for rec in self:
            rec.stage = 'doing'
            rec.confirmed_date = fields.Date.context_today(self)

    def complete_submission(self):
        for rec in self:
            rec.stage = 'completed'
            rec.complete_date = fields.Date.context_today(self)

    def action_generate_bills(self):
        generate_bills = self.env['generate.bills.wiz']
        for record in self:
            context = self._context.copy()
            context.update({
                'active_model': 'sample.submission',
                'active_id': record.id,
                'active_ids': [record.id],
            })
            generate_bills_obj = generate_bills.with_context(context).create({'submission_id': record.id})
            form_view_id = self.env.ref('sample_submission_mngmt.generate_bills_wiz_form').id
            return {
                'name': _('Generate Bills'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'generate.bills.wiz',
                'views': [(form_view_id, 'form')],
                'view_id': form_view_id,
                'target': 'new',
                'res_id': generate_bills_obj.id,
            }

    def print_sample_pdf(self):
        return self.env.ref('sample_submission_mngmt.sample_print_id').report_action(self)


class SampleSubmissionMaterial(models.Model):
    _name = 'sample.submission.material'
    _description = 'Sample Submission Material'

    sl_no = fields.Integer(string="Sl no.")
    product_id = fields.Many2one('product.product', string='Material/Product')
    quantity = fields.Float('Quantity')
    remarks = fields.Text('Remarks')
    submission_id = fields.Many2one('sample.submission', string='Sample Submission')
