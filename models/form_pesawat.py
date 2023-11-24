import odoo
from odoo import api, fields, models, _
from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime

class PenumpangPesawat(models.Model):
    _name = "penumpang.pesawat"
    _description = "Penumpang Pesawat"
    # _inherit = ['mail.thread', 'ir.needaction_mixin']
    _inherit = 'mail.thread'
    reference = fields.Char(string='ID Pemesanan', required= True, readonly=True, copy=False, default=lambda self:_('New'))
    reference_nama_pesawat = fields.Reference(selection=[('nama.pesawat','Nama Pesawat')], string='Pesawat', ondelete='restrict')
    # reference_nama_pesawat = fields.Many2one('nama.pesawat', string='Nama Pesawat')

    name = fields.Char(string='Nama Lengkap', required=True, tracking = True)

    email = fields.Char(string='Email Aktif', required=True, tracking = True)

    tanggal = fields.Date(string='Tanggal Penerbangan',required=True, tracking = True)
   
    @api.constrains('tanggal')
    def _check_tanggal_penerbangan(self):
        for record in self:
            if record.tanggal and record.tanggal < fields.Date.today():
                raise UserError("Anda tidak dapat memilih tanggal penerbangan sebelum dari hari ini.")

    umur = fields.Integer(string='Umur', required=True, tracking = True)
    gender = fields.Selection([
        ('male','Laki-laki'),
        ('female', 'Perempuan')], 
        required=True, string='Jenis Kelamin', default = 'male')
    
    asal = fields.Selection([
        ('surabaya','Surabaya'),
        ('tarakan', 'Tarakan'),
        ('jakarta','Jakarta'),
        ('bandung','Bandung')], 
        required=True,string='Kota Asal', default = 'surabaya')

    tujuan = fields.Selection([
        ('surabaya','Surabaya'),
        ('tarakan', 'Tarakan'),
        ('jakarta','Jakarta'),
        ('bandung','Bandung')], 
        required=True,string='Kota Tujuan', default = 'jakarta')
    
    @api.onchange('asal', 'tujuan')
    def _onchange_asal_tujuan(self):
        if self.asal == self.tujuan:
            raise UserError("Kota asal dan tujuan tidak boleh sama!")


    kelas = fields.Selection([
            ('ekonomi','Kelas Ekonomi'),
            ('bisnis', 'Kelas Bisnis'),
            ('first','Kelas First')], 
            required=True, default = 'ekonomi', tracking = True)

    harga = fields.Float(string='Harga', compute='_compute_harga', store=True)

    @api.depends('kelas', 'asal', 'tujuan')
    def _compute_harga(self):
        for rec in self:
            if rec.kelas == 'ekonomi':
                rec.harga = 1000000
            elif rec.kelas == 'bisnis':
                rec.harga = 4000000
            elif rec.kelas == 'first':
                rec.harga = 10000000
            else:
                rec.harga = 0

    note = fields.Text(string='Description')
 
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New'
        if vals.get('reference', _('New'))== _('New'):
            vals['reference'] = self.env["ir.sequence"].next_by_code('penumpang.pesawat') or _('New')
        res = super(PenumpangPesawat, self).create(vals)
        return res 


    def duplicate_to_confirmation(self):
        for penumpang in self:
            vals = {
                'reference': penumpang.reference, 
                # 'reference_nama_pesawat': penumpang.reference_nama_pesawat,
                'name': penumpang.name,
                'tanggal': penumpang.tanggal,
                'umur': penumpang.umur,
                'gender': penumpang.gender,
                'asal': penumpang.asal,
                'tujuan': penumpang.tujuan,
                'kelas': penumpang.kelas,
                'harga': penumpang.harga,
                'note': penumpang.note,
            }
            
            konfirmasi_pesawat = self.env['konfirmasi.pesawat'].create(vals)
