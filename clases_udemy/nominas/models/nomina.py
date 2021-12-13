# -*- coding: utf-8 -*-

import logging

from odoo import fields, models, api, exceptions


logger = logging.getLogger(__name__)


class Nomina(models.Model):
    _name = 'nomina'
    _inherit = ['image.mixin']