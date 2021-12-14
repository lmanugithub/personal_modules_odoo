# -*- coding: utf-8 -*-

# from typing_extensions import ParamSpecArgs <- neta que no se de donde salio esto
import logging

from odoo import fields, models, api, exceptions


logger = logging.getLogger(__name__)


class Presupuesto(models.Model):
    _name = 'presupuesto'
    _inherit = ['image.mixin']
    name = fields.Char(string='Película')
    clasificacion = fields.Selection(selection=[
        ('G', 'G'),  # Publico en general
        ('PG', 'PG'),  # Se recomienda la compañia de un adulto
        ('PG-13', 'PG13'),  # Mayor de 13
        ('R', 'R'),  # En compañia de un adulto obligatorio
        ('NC-17', 'NC-17'),  # Mayores de 18
    ], string='Clasificación')

    dsc_clasificacion = fields.Char(string='Descripción clasificación')

    fch_estreno = fields.Date(string='Fecha Estreno')
    # relacionamos el valor de otra variable
    puntuacion = fields.Integer(string='Puntuación', related="puntuacion2")
    puntuacion2 = fields.Integer(string='Puntuación2')
    # para ocultar o no algunos datos y el usuario no los pueda ver o no
    active = fields.Boolean(string='Activo', default=True)
    director_id = fields.Many2one(
        comodel_name='res.partner',  # es el _name del modelo
        string='Director'
    )
    categoria_director_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Categoria Director',
        # Segunda version
        default=lambda self: self.env.ref('peliculas.category_director')

        # Primera version
        # default=lambda self: self.env['res.partner.category'].search([('name', '=', 'Director')])
    )
    genero_ids = fields.Many2many(
        comodel_name='genero',  # es el _name del modelo
        string='Generos'
    )
    vista_general = fields.Text(string='Descripción')
    link_trailer = fields.Char(string='Trailer')
    es_libro = fields.Boolean(string='Versión Libro')
    libro = fields.Binary(string='Libro')
    libro_filename = fields.Char(string='Nombre del Libro')

    # Creación de la barra de estado state

    state = fields.Selection(selection=[
        ('borrador', 'Borrador'),
        ('aprobado', 'Aprovado'),
        ('cancelado', 'Cancelado'),
    ], default='borrador', string='Estados', copy=False)

    # Variables de pestañas
    # Pestaña 1

    fch_aprobado = fields.Datetime(string='Fecha aprobación', copy=False)
    fch_creacion = fields.Datetime(string='Fecha creación', copy=False, default=lambda self:fields.Datetime.now() )
    num_prespupuesto = fields.Char(string='Numero de presupuesto', copy=False)
    # Pestaña 2
    actor_ids = fields.Many2many(
        comodel_name='res.partner',  # es el _name del modelo
        string='Actores'
    )
    categoria_actor_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Categoria Actor',
        default=lambda self: self.env.ref('peliculas.category_actor')
    )
    opinion = fields.Html(string="Opinion")

    # Definimos funciones para nuestros botones

    def aprobar_presupuesto(self):
        logger.info('Entro a la fucnión aprobar')
        self.state = 'aprobado'
        self.fch_aprobado = fields.Datetime.now()

    def cancelar_presupuesto(self):
        self.state = 'cancelado'

    # Re-definimos las funciones propias de Odoo

    def unlink(self):
        '''
        Info: Esta función es para eliminar registros
        '''
        logger.info('************************Se disparo la función unlink')
        for record in self: 
            if record.state != 'cancelado':
                raise exceptions.UserError(
                    'No se puede eliminar sino está cancelado')
            super(Presupuesto, record).unlink()

    @api.model
    def create(self, variables):
        '''
        Info: Esta función es para crear registros
        '''
        logger.info(f'**************variable: {variables}')
        secuence_obj = self.env['ir.sequence']
        correlativo = secuence_obj.next_by_code(
            'secuencia.presupuesto.pelicula')
        variables['num_prespupuesto'] = correlativo
        return super(Presupuesto, self).create(variables)

    def write(self, variables):
        '''
        Info: Se dispara cuando se edita un registro
        Solo le llegaran las variables editadas
        '''
        logger.info(f'**************variable: {variables}')
        if 'clasificacion' in variables:
            raise exceptions.UserError('La clasificación no es editable')
        return super(Presupuesto, self).write(variables)

    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = self.name + ' (copia)'
        return super(Presupuesto, self).copy(default)

    @api.onchange('clasificacion')
    def _onchange_clasificacion(self):
        if self.clasificacion:
            if self.clasificacion == 'G':
                self.dsc_clasificacion = 'Publico en general'
            if self.clasificacion == 'PG':
                self.dsc_clasificacion = 'Se recomienda la compañia de un adulto'
            if self.clasificacion == 'PG-13':
                self.dsc_clasificacion = 'Mayor de 13'
            if self.clasificacion == 'R':
                self.dsc_clasificacion = 'En compañia de un adulto obligatorio'
            if self.clasificacion == 'NC-17':
                self.dsc_clasificacion = 'Mayores de 18'
        else:
            self.dsc_clasificacion = False
