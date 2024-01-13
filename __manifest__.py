{
    'name' : 'JetSetGo',
    'author' : 'luqna',
    'summary' : 'Make us be your partner travel! ^^',
    'application' : True,
    'depends' : ['mail'],
    'images' : ['static/description/*.png'] ,
    'data' : [
        'views/form_pesawat.xml',
        'views/nama_pesawat.xml',
        'views/konfirmasi_pesawat.xml',
        'views/status_pesawat.xml',
        'views/dashboard.xml',
        'views/template.xml',

        'data/data_form.xml',
        'data/data_nama.xml',
        'data/data_status.xml',

        'report/report_status.xml',
        'report/surat_status.xml',
        'security/ir.model.access.csv'],
    'qweb':[
        'static/xml/*.xml',
    ]
}
