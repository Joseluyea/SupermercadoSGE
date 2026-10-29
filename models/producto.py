from odoo import models, fields


class Producto(models.Model):
    _name = "supermercado.producto"
    _description = "Producto del supermercado"
    # campo que Odoo usa para mostrar el producto (si no, buscaria un campo llamado name)
    _rec_name = "nombre"

    nombre = fields.Char(string="Nombre", required=True, help="Nombre del producto")

    codigo_barras = fields.Char(string="Código de barras", help="Código de barras del producto")

    descripcion = fields.Text(string="Descripción", help="Descripción del producto")

    # el Binary es para guardar la foto del producto
    imagen = fields.Binary(string="Imagen", help="Foto del producto")

    precio = fields.Float(string="Precio sin IVA", required=True, help="Precio del producto sin el IVA")

    # el primer valor es el que se guarda en la base de datos y el segundo el que ve el usuario
    tipo_iva = fields.Selection(selection=[("4", "Superreducido (4%)"),
                                           ("10", "Reducido (10%)"),
                                           ("21", "General (21%)")],
                                string="Tipo de IVA", required=True, default="10",
                                help="IVA que lleva el producto")

    stock = fields.Integer(string="Stock", default=0, help="Unidades que quedan en la tienda")

    tipo_conservacion = fields.Selection(selection=[("ambiente", "Ambiente"),
                                                    ("refrigerado", "Refrigerado"),
                                                    ("congelado", "Congelado")],
                                         string="Conservación", default="ambiente",
                                         help="Cómo hay que guardar el producto")
    
    fecha_caducidad = fields.Date(string="Fecha de caducidad", help="Día en que caduca el producto")

    # se rellena sola con la fecha y hora del momento en que se crea el producto
    fecha_alta = fields.Datetime(string="Fecha de alta", default=fields.Datetime.now,
                                 help="Cuándo se dio de alta el producto")

    en_oferta = fields.Boolean(string="En oferta", default=False, help="Marcar si el producto está en oferta")
