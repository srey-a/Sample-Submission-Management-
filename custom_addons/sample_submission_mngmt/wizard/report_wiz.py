from odoo import models, fields, api


class SampleSubmissionReportWizard(models.TransientModel):
    _name = 'sample.submission.report.wizard'
    _description = 'Sample Submission Report Wizard'

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')


