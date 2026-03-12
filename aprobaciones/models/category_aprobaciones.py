# -*- coding: utf-8 -*-

from odoo import fields, models

class Category(models.Model):
    _name='aprobaciones.category'
    name=fields.Char(string="Nombre de la categoria")