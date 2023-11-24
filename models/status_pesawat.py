from odoo import api, fields, models, _

class StatusPesawat(models.Model):
    _name = "status.pesawat"
    _description = "Status Pemesanan Tiket Pesawat"

    reference_penumpang = fields.Char(string='ID Penumpang', required=True, copy=False, default=lambda self: _('New'))

    
    name = fields.Char(string='Nama Lengkap', required=True, tracking=True)

    reference = fields.Char(string='Kode Pemesanan', required= True, readonly=True, copy=False, default=lambda self:_('New'))

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

    note3 = fields.Text(string='Description')

    @api.model
    def create(self, vals):
        if vals.get('note3'):
            vals['note3'] = 'New Penumpang'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('status.pesawat') or _('New')
        res = super(StatusPesawat, self).create(vals)
        return res