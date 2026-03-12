# -*- coding:utf-8 -*-

from odoo import models, fields,api
from odoo.exceptions import ValidationError
class ContactCustom(models.Model):
    _inherit="res.partner"

    is_recurrente= fields.Boolean(string="Es recurrente?")


    @api.constrains("email")
    def _check_email(self):
        for record in self:
            if record.email and '@' not in record.email:
                raise ValidationError("El email no es valido")

    @api.model_create_multi
    def create(self, vals_list):
        for record in vals_list:
            if 'name' in record:
                record['name']=record['name'].upper()

        return super().create(vals_list)

    @api.constrains("phone", "mobile")
    def _check_number(self):
        for record in self:
            if record.phone and len(record.phone) < 9:
                raise ValidationError("El numero no es valido")