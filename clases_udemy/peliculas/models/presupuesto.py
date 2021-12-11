# -*- coding: utf-8 -*-

# from typing_extensions import ParamSpecArgs <- neta que no se de donde salio esto
import logging

from odoo import fields, models, api

logger = logging.getLogger(__name__)

class Presupuesto(models.Model):
    _name = 'presupuesto'
    _inherit = ['image.mixin']
    name = fields.Char(string='Película')
    clasificacion = fields.Selection(selection=[
        ('G','G'), # Publico en general
        ('PG','PG'), # Se recomienda la compañia de un adulto
        ('PG-13','PG13'), # Mayor de 13
        ('R','R'), # En compañia de un adulto obligatorio
        ('NC-17','NC-17'), # Mayores de 18
    ],string='Clasificación')

    fch_estreno = fields.Date(string='Fecha Estreno')
    puntuacion = fields.Integer(string='Puntuación', related="puntuacion2") # relacionamos el valor de otra variable
    puntuacion2 = fields.Integer(string='Puntuación2')
    active = fields.Boolean(string='Activo', default=True) # para ocultar o no algunos datos y el usuario no los pueda ver o no
    director_id = fields.Many2one(
        comodel_name='res.partner', # es el _name del modelo
        string='Director'
    )
    categoria_director_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Categoria Director',
        default=lambda self: self.env['res.partner.category'].search([('name','=','Director')])
    )
    genero_ids = fields.Many2many(
        comodel_name='genero', # es el _name del modelo
        string='Generos'
    )
    vista_general = fields.Text(string='Descripción')
    link_trailer = fields.Char(string='Trailer')
    es_libro = fields.Boolean(string='Versión Libro')
    libro = fields.Binary(string='Libro')
    libro_filename = fields.Char(string='Nombre del Libro')
    
    # Creación de la barra de estado state
 
    state = fields.Selection(selection=[
        ('borrador','Borrador'),
        ('aprobado','Aprovado'),
        ('cancelado','Cancelado'),
    ], default='borrador', string='Estados', copy=False)

    fch_aprobado = fields.Datetime(string='Fecha aprobación', copy=False)

    # Definimos funciones para nuestros botones

    def aprobar_presupuesto(self):
        logger.info('Entro a la fucnión aprobar')
        self.state = 'aprobado'
        self.fch_aprobado = fields.Datetime.now()


    def cancelar_presupuesto(self):
        self.state = 'cancelado'
