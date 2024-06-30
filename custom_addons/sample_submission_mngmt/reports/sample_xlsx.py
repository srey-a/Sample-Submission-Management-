import io
import base64
import xlsxwriter
from odoo import models
class SampleSubmission(models.Model):
    _name = 'sample.submission'
    _description = 'Sample Submission'

    def generate_excel_report(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        title_format = workbook.add_format({'bold': True, 'font_size': 14})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#CCCCCC'})

        worksheet.write(0, 0, 'Sample Submission Report', title_format)
        worksheet.write(1, 0, 'Date', header_format)
        worksheet.write(1, 1, 'Customer', header_format)
        worksheet.write(1, 2, 'Name', header_format)
        worksheet.write(1, 3, 'Price', header_format)

        row = 2
        for record in self:
            worksheet.write(row, 0, str(record.submission_date))
            worksheet.write(row, 1, record.customer_id.name)
            worksheet.write(row, 2, record.name)
            worksheet.write(row, 3, record.price)
            row += 1

        workbook.close()
        output.seek(0)

        return {
            'type': 'ir.actions.act_url',
            'url': 'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,' + base64.b64encode(output.read()).decode('utf-8'),
            'target': 'new',
        }
