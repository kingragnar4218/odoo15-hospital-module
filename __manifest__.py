{
    'name': 'HT Hospital',
    'version': '1.0',
    'summary': 'hospital demo new for data base',
    'description': 'This module demo',
    'author': 'harsh',
    'website': 'https://www.hthospital.com',

    'depends': ['base' ,'mail'],

    'data': [
        'security/ir.model.access.csv',
        'views/patient_view.xml',   # action first
        'views/manu.xml',           # menu after action
        'views/female_patient_view.xml',
        'views/appoinment_view.xml',
    ],

    'sequence': -100,
    'installable': True,
    'application': True,
}
