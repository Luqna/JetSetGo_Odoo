from odoo import api, fields, models, _

class NamaPesawat(models.Model):
    _name = "nama.pesawat"
    _description = "Nama Pesawat"
    _rec_name = 'name_pesawat'
    reference_pesawat = fields.Char(string='Reference Pesawat', required=True, copy=False, default=lambda self: _('New'))

    # reference = fields.Reference([('penumpang.pesawat','Pesawat')],string='Reference')
    name_pesawat = fields.Char(string='Nama Pesawat', required=True, tracking = True)
    
    kode_pesawat = fields.Char(string='Kode Pesawat', required=True, tracking = True)
    
    note_pesawat = fields.Selection([
        ('domestik','Pesawat Domestik'),
        ('internasional', 'Pesawat Internasional')], 
        required=True, default = 'domestik')
    
    status_pesawat = fields.Selection([
        ('aktif','Pesawat Aktif'),
        ('nonaktif', 'Pesawat Non-Aktif')], 
        required=True, default = 'aktif')

    note2 = fields.Text(string='Description')

    @api.model
    def create(self, vals):
        if not vals.get('note2'):
            vals['note2'] = 'New'
        if vals.get('reference_pesawat', _('New'))== _('New'):
            vals['reference_pesawat'] = self.env["ir.sequence"].next_by_code('nama.pesawat') or _('New')
        res = super(NamaPesawat, self).create(vals)
        return res 

