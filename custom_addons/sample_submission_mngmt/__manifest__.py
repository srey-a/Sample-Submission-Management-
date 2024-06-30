# -*- coding: utf-8 -*-
{
    'name': "sample_submission_management",

    'summary': """Manage sample submissions, generate invoices, and reports""",

    'description': """
        The goal of this project is to create a custom Odoo app called "sample-submission".
        This app aims to streamline the management of sample submissions, connect
        customers to submission forms, keep track of materials as products related to
        sample-submission, and generate invoices. Additionally, the app will support the
        generation of PDF and Excel reports with specific data and formatting requirements.
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.0.1.0.0',
    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'account'],
    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'reports/pdf_template.xml',
        'reports/sample_pdf_template.xml',
        'reports/reports.xml',
        'wizard/material_wizard.xml',
        'wizard/generate_bill_wiz.xml',
        # 'wizard/report_wiz.xml',
        'views/sample_submission.xml',
        'views/res_partner.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
