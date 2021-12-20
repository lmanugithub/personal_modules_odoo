# -*- coding: utf-8 -*-

import logging

from odoo import fields, models, api, exceptions


logger = logging.getLogger(__name__)


class RecursoCinamatografico(models.Model):
    _name = "recurso.cinematografico"
    name = fields.Char(string='Recurso')
    descripcion = fields.Char(string='Descripción')
    precio = fields.Float(srting='Precio')
    contacto = fields.Many2one(
        comodel_name='res.partner',
        domain = "[('is_company','=', False)]"
    )
    imagen = fields.Binary(string='Imagen')
