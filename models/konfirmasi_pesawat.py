from odoo import api, fields, models, _

class KonfirmasiPesawat(models.Model):
    _name = "konfirmasi.pesawat"
    _description = "Konfirmasi Pesawat"
    reference = fields.Char(string='ID Pemesanan', required= True, readonly=True, copy=False, default=lambda self:_('New'))
    reference_nama_pesawat = fields.Reference(selection=[('nama.pesawat','Nama Pesawat')], string='Pesawat', ondelete='restrict')
    
    name = fields.Char(string='Nama Lengkap', required=True, tracking=True)

    message = fields.Text(string='Message')
    
    tanggal = fields.Date(string='Tanggal Penerbangan')
    
    umur = fields.Integer(string='Umur')

    gender = fields.Selection([
        ('male', 'Laki-laki'),
        ('female', 'Perempuan')], required=True, string='Jenis Kelamin', default='male')
    
    asal = fields.Selection([
        ('surabaya', 'Surabaya'),
        ('tarakan', 'Tarakan'),
        ('jakarta', 'Jakarta'),
        ('bandung', 'Bandung')],
        required=True, string='Kota Asal', default='surabaya')
    
    tujuan = fields.Selection([
        ('surabaya', 'Surabaya'),
        ('tarakan', 'Tarakan'),
        ('jakarta', 'Jakarta'),
        ('bandung', 'Bandung')],
        required=True, string='Kota Tujuan', default='jakarta')
    
    kelas = fields.Selection([
        ('ekonomi', 'Kelas Ekonomi'),
        ('bisnis', 'Kelas Bisnis'),
        ('first', 'Kelas First')],
        required=True, default='ekonomi')
    
    harga = fields.Float(string='Harga')
    
    note = fields.Text(string='Description')
    
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Cancel')], default='draft', string="Status")
    
    def action_confirm(self):
        self.state = 'done'
    
    def action_cancel(self):
        self.state = 'cancel'

    def action_draft(self):
        self.state = 'draft'






    def duplicate_confirm(self):
        for penumpang in self:
            vals = {
                # 'reference': penumpang.reference, 
                # 'reference_nama_pesawat': penumpang.reference_nama_pesawat,
                'name': penumpang.name,
                'tanggal': penumpang.tanggal,
                'umur': penumpang.umur,
                'gender': penumpang.gender,
                'asal': penumpang.asal,
                'tujuan': penumpang.tujuan,
                'kelas': penumpang.kelas,
                'state': penumpang.state,
                'harga': penumpang.harga,
                'note': penumpang.note,
            }
            
            status_pesawat = self.env['status.pesawat'].create(vals)
