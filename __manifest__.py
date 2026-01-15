{
    'name': 'HT Hospital',
    'version': '1.0',
    'summary': 'hospital demo new for data base',
    'description': 'This module demo',
    'author': 'harsh',
    'website': 'https://www.hthospital.com',

    'depends': ['base', 'mail' , 'product'],

    'data': [
        'security/ir.model.access.csv',

        'data/patient_tag_data.xml',
        'data/patient.tag.csv',
        'data/sequence_data.xml',
        
        'wizard/cancel_appointment_view.xml',

        'views/patient_view.xml',
        'views/manu.xml',
        'views/female_patient_view.xml',
        'views/appoinment_view.xml',
        'views/patient_tag_view.xml',
        'views/odoo_playgroung_view.xml',
        'views/res_config_settings_views.xml',
        'views/operation_view.xml',
],
    # 'assets': {
    #     'web.assets_backend': [
    #         'ht_hospital/static/src/css/statusbar.css', # THIS CSS IS NOT WORK IN BUTTON BORDER REMOVE
    #     ],
    # },

    'sequence': -100,
    'installable': True,
    'application': True,
}
