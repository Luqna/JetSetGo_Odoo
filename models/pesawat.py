from odoo import api, fields, models, _
from odoo import models, fields, api


class PenumpangPesawat(models.Model):
    _name = "penumpang.pesawat"
    _description = "Penumpang Pesawat"

    name = fields.Char(string='Nama', required=True, tracking = True)
    reference = fields.Char(string='reference', required=True, copy=False, readonly=True, 
                            default=lambda self: _('New'))
    tanggal = fields.Date(string='Tanggal Penerbangan')
    umur = fields.Integer(string='Umur')
    gender = fields.Selection([
        ('male','Laki-laki'),
        ('female', 'Perempuan')], 
        required=True, default = 'male')
    
    asal = fields.Selection([
        ('surabaya','Surabaya'),
        ('tarakan', 'Tarakan'),
        ('jakarta','Jakarta'),
        ('bandung','Bandung')], 
        required=True, default = 'surabaya')

    tujuan = fields.Selection([
        ('surabaya','Surabaya'),
        ('tarakan', 'Tarakan'),
        ('jakarta','Jakarta'),
        ('bandung','Bandung')], 
        required=True, default = 'jakarta')
    
    plane = fields.Selection([
            ('garuda','Garuda Indonesia - GI123'),
            ('citilink', 'Citilink - CL870'),
            ('airasia','Air Asia - AA234')], 
            required=True, default = 'citilink')

    kelas = fields.Selection([
            ('ekonomi','Kelas Ekonomi'),
            ('bisnis', 'Kelas Bisnis'),
            ('first','Kelas First')], 
            required=True, default = 'ekonomi')

    harga = fields.Float(string='Harga', compute='_compute_harga', store=True)

    @api.depends('kelas')
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
    state = fields.Selection([('draft','Draft'), ('done','Done'), ('cancel','Cancel')], default='draft', string="Status")

    def action_confirm(self):
        self.state = 'done'
    
    def action_cancel(self):
        self.state = 'cancel'

    def action_draft(self):
        self.state = 'draft'
 
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New'
        if vals.get('reference', _('New'))== _('New'):
            #vals['reference'] = self.env['ir.sequence'].next_by_code('penumpang.pesawat') or 'New'
            vals['reference'] = self.env["ir.sequence"].next_by_code('penumpang.pesawat') or _('New')
        res = super(PenumpangPesawat, self).create(vals)
        return res 
