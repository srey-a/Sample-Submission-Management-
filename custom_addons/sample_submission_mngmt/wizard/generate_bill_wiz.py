from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class GenerateBillWiz(models.TransientModel):
    _name = 'generate.bills.wiz'
    _description = 'Generate Bill Wiz'

    @api.model
    def default_get(self, fields):
        res = super(GenerateBillWiz, self).default_get(fields)
        if self._context.get('active_model') == 'sample.submission' and self._context.get('active_id'):
            sample_submission = self.env['sample.submission'].browse(self._context.get('active_id'))
            if sample_submission:
                res.update({
                    'submission_id': self._context.get('active_id'),
                    'reference': sample_submission.name,
                    'customer_id': sample_submission.customer_id.id if sample_submission.customer_id else False,
                    'amount': sample_submission.price,
                    'discount': sample_submission.discount,
                    'vat': sample_submission.vat,
                })
        return res

    @api.model
    def get_lines(self):
        lines = []
        if self._context.get('active_model') == 'sample.submission' and self._context.get('active_id'):
            sample_submission = self.env['sample.submission'].browse(self._context.get('active_id'))
            if sample_submission:
                for line in sample_submission.material_line_ids.filtered(lambda i: i.quantity):
                    vals = {
                        'sl_no': line.sl_no or '',
                        'product_id': line.product_id.id if line.product_id else False,
                        'quantity': line.quantity or 0.0,
                        'remarks': line.remarks or '',
                        'sample_line_id': line.id or False,
                    }
                    lines.append((0, 0, vals))
        return lines

    submission_id = fields.Many2one('sample.submission', string='Sample Submission')
    customer_id = fields.Many2one('res.partner', string='Customer')
    reference = fields.Char(string='Reference', required=True)
    amount = fields.Float(string='Amount', required=True)
    discount = fields.Float(string='Discount', required=True)
    vat = fields.Char(string='VAT', required=True)
    bills_line_ids = fields.One2many('generate.bills.wiz.lines', 'wiz_line_id', default=get_lines)

    def create_invoice(self):
        for wizard in self:
            sample_submission = wizard.submission_id
            if sample_submission.invoiced:
                raise ValidationError(_('Invoice already created for this sample submission.'))
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': wizard.customer_id.id,
                'invoice_line_ids': [(0, 0, {
                    'name': wizard.reference,
                    'quantity': 1,
                    'price_unit': wizard.amount,
                    'discount': wizard.discount,
                })],
            }
            invoice = self.env['account.move'].create(invoice_vals)
            sample_submission.write({'invoiced': True})
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': invoice.id,
                'target': 'current',
            }


class GenerateBillWizLines(models.TransientModel):
    _name = 'generate.bills.wiz.lines'
    _description = 'Generate Bill Wiz Lines'

    wiz_line_id = fields.Many2one('generate.bills.wiz')
    sl_no = fields.Integer(string="Sl no.")
    product_id = fields.Many2one('product.product', string='Material/Product')
    quantity = fields.Float('Quantity')
    remarks = fields.Text('Remarks')
    sample_line_id = fields.Many2one('sample.submission.material', string="Sample Submission Line")
