from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class MaterialWizard(models.TransientModel):
    _name = 'material.wizard.wiz'
    _description = 'Material Wizard'

    @api.model
    def default_get(self, fields):
        res = super(MaterialWizard, self).default_get(fields)
        if self._context.get('active_model') == 'sample.submission' and self._context.get('active_id'):
            submission_id = self.env['sample.submission'].browse(self._context.get('active_id'))
            res.update({
                'submission_id': submission_id and submission_id.id or False
            })
        elif self._context.get('active_model') == 'sample.submission.material' and self._context.get('active_id'):
            material_line_id = self.env['sample.submission.material'].browse(self._context.get('active_id'))
            res.update({
                'product_id': material_line_id.product_id and material_line_id.product_id.id or False,
                'quantity': material_line_id.quantity or 0.00,
                'psr_line_id': material_line_id.id,
                'remarks': material_line_id.remarks or ''
            })
        return res

    product_id = fields.Many2one('product.product', string='Material/Product')
    quantity = fields.Float('Quantity')
    remarks = fields.Text('Remarks')
    submission_id = fields.Many2one('sample.submission', string='Sample Submission')

    def add_material(self):
        for rec in self:
            if self._context.get('active_model') == 'sample.submission' and self._context.get('active_id'):
                if rec.quantity <= 0:
                    raise ValidationError(_('Quantity should be positive.'))
                next_sl_no = self.env['sample.submission.material'].search_count(
                    [('submission_id', '=', rec.submission_id.id)]) + 1
                vals = {
                    'submission_id': rec.submission_id.id,
                    'product_id': rec.product_id and rec.product_id.id or False,
                    'remarks': rec.remarks or '',
                    'quantity': rec.quantity,
                    'sl_no': next_sl_no
                }
                self.env['sample.submission.material'].create(vals)
