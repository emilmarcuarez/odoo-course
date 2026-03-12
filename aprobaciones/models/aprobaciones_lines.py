# -*- coding:utf-8 -*-
from odoo import models, fields

class AprobacionesLines(models.Model):
    _name="aprobaciones.lines"

    aprobacion_id=fields.Many2one('aprobaciones.custom',string="aprobacion_id")

    motivo = fields.Text(string="Motivo de la aprobacion")
    is_urgente = fields.Boolean(string="Urgente")
