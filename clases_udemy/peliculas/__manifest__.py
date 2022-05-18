# -*- coding: utf-8 -*-
{
    'name': "Modulo de peliculas",
    'description': "Hacer presupuestos de peluliculas",

    'category': 'peliculas',
    'version': '0.1',
    'website': 'www.uneteya.org',
    'summary': 'Modulo de presupuesto para peliculas',
    'depends': [
        'base',
        'contacts',
                ],
    'author': 'Luis Manuel',

    'data': [
        'data/categoria.xml',
        'data/secuencia.xml',
        'views/menu.xml',
        'views/presupuesto_views.xml',
    ]
}