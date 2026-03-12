# -*- coding:utf-8 -*-
from email.policy import default
from odoo import models , fields, api
from odoo.exceptions import ValidationError

class AprobacionesCustom(models.Model):
    _name='aprobaciones.custom'

    name =fields.Char(string='Nombre', required=True)
    fecha_creacion=fields.Date(string="Fecha de creacion", default=fields.Date.today(), readonly=True)
    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("approved", "Aprobado"),
            ("cancel", "Cancelado"),
            ("send","Enviado")
        ],
        default='draft',
        copy=True
    )

    aprobador_id = fields.Many2one('res.users', string="Usuario aprobador")

    aprobaciones_lines_ids = fields.One2many("aprobaciones.lines", "aprobacion_id", string="Detalles", copy=True)

    category_ids =fields.Many2many('aprobaciones.category', string="Categoria", domain=[('is_category_aprobacion', '=', True), ('is_important', '=', False)])

    qty_lines = fields.Integer(string="Numero de lineas", compute="_check_aprobaciones_lines_ids")
    qty_urgente = fields.Integer(string="Cantidad urgente", compute="_check_is_urgente")

    @api.onchange('fecha_creacion')
    def onchange_fecha_creacion(self):
        for record in self:
            if record['fecha_creacion'] and record['fecha_creacion'] < fields.Date.today():
                raise ValidationError("Fecha de creacion no valida, debe ser mayor")

    @api.depends('aprobaciones_lines_ids')
    def _check_aprobaciones_lines_ids(self):
        for record in self:
            record.qty_lines = len(record.aprobaciones_lines_ids)

    @api.depends('aprobaciones_lines_ids.is_urgente')
    def _check_is_urgente(self):
        for record in self:
            record.qty_urgente = sum(1 for line in record.aprobaciones_lines_ids if line.is_urgente)

    @api.constrains('category_ids')
    def _check_min_max_category(self):
        for record in self:
            if len(record.category_ids) < 1:
                raise ValidationError("No puedes crear una aprobacion sin una categoria")

            if len(record.category_ids) > 5:
                raise ValidationError("No puedes tener mas de 5 categorias")

    @api.constrains('name')
    def _check_min_max_aprobaciones(self):
        for record in self:
            if record.qty_lines < 1:
                raise ValidationError("Debes de tener al menos un motivo de aprobacion")

    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if not record.name:
                raise ValidationError("El nombre no puede estar vacío.")
            if len(record.name) < 3:
                raise ValidationError("El nombre debe tener al menos 3 caracteres.")

    #create, write, unlink, copy

    @api.model_create_multi
    def create(self, vals_list):
        name_black_list = ["prueba", "test", "juan", "miguel"]
        for vals in vals_list:
            if vals.get("name", '').lower() in name_black_list:
                raise ValidationError("EL NOMBRE ESTA EN LA BLACK LIST")
            if vals.get("state", "draft") != "draft":
                raise ValidationError("NO PUEDES MANIPULAR EL ESTADO")

        return super().create(vals_list)

    def write(self, vals):
        for record in self:
            if record.state != "draft" and 'name' in vals:
                raise ValidationError("NO PUEDES CAMBIAR EL NOMBRE SI LA APROBACION NO ESTA EN BORRADOR")

        return super().write(vals)

    def unlink(self):
        for record in self:
            if record.state in ['send', 'aprobado']:
                raise ValidationError("NO PUEDES ELIMINAR")

        return super().unlink()

    def copy(self, default=None):
        default=dict(default or {})

        for record in self:
            default['name'] = f"{record['name']} (copia)"

        return super().copy(default)