# -*- coding: utf-8 -*-
{
    'name': "Supermercado El Granero",
    'summary': "Gestión de los productos, secciones, empleados y proveedores del supermercado",
    'description': "Aplicación para llevar el stock, las caducidades y el personal de un supermercado de barrio",
    'author': "José Luis",
    'website': "",
    'category': "Sales",
    'version': '0.1',
    'license': 'LGPL-3',

    # solo necesita el modulo base de Odoo
    'depends': ['base'],

    # archivos que se cargan al instalar, en este orden
    # los menus van al final porque usan las acciones de las vistas
    'data': [
        'security/ir.model.access.csv',
        'views/producto_view.xml',
        'views/seccion_view.xml',
        'views/menus.xml',
    ],

    'installable': True,
    'application': True,
}
