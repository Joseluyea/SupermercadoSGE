{
    'name': "Supermercado El Granero",
    'summary': "Gestión de los productos, secciones, empleados y proveedores del supermercado",
    'description': "Aplicación para llevar el stock, las caducidades y el personal de un supermercado de barrio",
    'author': "José Luis",
    'website': "",
    'category': "Sales",
    'version': '0.1',
    'license': 'LGPL-3',

    #solo depende de base
    'depends': ['base'],

    # archivos que se cargan al instalar, el orden importa
    # los menus van al final por que usan las acciones de las vistas
    'data': [
        'security/ir.model.access.csv',
        'views/producto_view.xml',
        'views/seccion_view.xml',
        'views/empleado_view.xml',
        'views/proveedor_view.xml',
        'views/menus.xml',
    ],

    #datos de prueba (solo se cargan si la bd tiene puesto lo de datos de demostracion)
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
}
