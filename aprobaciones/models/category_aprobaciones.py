# -*- coding: utf-8 -*-

from odoo import fields, models

class Category(models.Model):
    _name='aprobaciones.category'
    name=fields.Char(string="Nombre de la categoria")
    is_category_aprobacion=fields.Boolean(string="Categoria de aprobacion")
    is_important= fields.Boolean(string="Es importante")