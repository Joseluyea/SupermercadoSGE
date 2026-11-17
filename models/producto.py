from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Producto(models.Model):
    _name = "supermercado.producto"
    _description = "Producto del supermercado"
    #el campo que sale como nombre del producto, sino buscaria uno que se llame name
    _rec_name = "nombre"

    nombre = fields.Char(string="Nombre", required=True, help="Nombre del producto")

    codigo_barras = fields.Char(string="Código de barras", help="Código de barras del producto")

    descripcion = fields.Text(string="Descripción", help="Descripción del producto")

    #binary para la foto
    imagen = fields.Binary(string="Imagen", help="Foto del producto")

    precio = fields.Float(string="Precio sin IVA", required=True, help="Precio del producto sin el IVA")

    # en el selection el primer valor es lo que se guarda y el segundo lo que se ve
    tipo_iva = fields.Selection(selection=[("4", "Superreducido (4%)"),
                                           ("10", "Reducido (10%)"),
                                           ("21", "General (21%)")],
                                string="Tipo de IVA", required=True, default="10",
                                help="IVA que lleva el producto")

    #se calcula con el precio y el iva, con store=True se guarda en la base de datos
    precio_final = fields.Float(string="Precio con IVA", compute="_compute_precio_final", store=True,
                                help="Precio con el IVA ya sumado")

    stock =fields.Integer(string="Stock", default=0, help="Unidades que quedan en la tienda")

    tipo_conservacion = fields.Selection(selection=[("ambiente", "Ambiente"),
                                                    ("refrigerado", "Refrigerado"),
                                                    ("congelado", "Congelado")],
                                         string="Conservación", default="ambiente",
                                         help="Cómo hay que guardar el producto")

    fecha_caducidad = fields.Date(string="Fecha de caducidad", help="Día en que caduca el producto")

    #este no lleva store porque tiene que mirar la fecha de hoy cada vez
    caducado = fields.Boolean(string="Caducado", compute="_compute_caducado",
                              help="Se marca solo si ya ha pasado la fecha de caducidad")

    # se pone sola la fecha y hora de cuando se crea
    fecha_alta = fields.Datetime(string="Fecha de alta", default=fields.Datetime.now,
                                 help="Cuándo se dio de alta el producto")

    en_oferta = fields.Boolean(string="En oferta", default=False, help="Marcar si el producto está en oferta")

    #Many2one, cada producto esta en una seccion. El One2many esta en seccion.py
    seccion_id = fields.Many2one("supermercado.seccion", string="Sección", help="Sección donde está el producto")

    #Many2many con proveedor, se guarda en una tabla intermedia que tiene producto_id y proveedor_id
    proveedor_ids = fields.Many2many("supermercado.proveedor",
                                     relation="supermercado_producto_proveedor_rel",
                                     column1="producto_id",
                                     column2="proveedor_id",
                                     string="Proveedores",
                                     help="Proveedores que nos traen este producto")

    #Calcula el precio con iva cuando cambia el precio o el tipo de iva
    #si el precio es negativo salta un error, es la excepcion en un depends que pide el trabajo
    @api.depends("precio", "tipo_iva")
    def _compute_precio_final(self):
        for producto in self:
            if producto.precio < 0:
                raise ValidationError("El precio no puede ser negativo.")
            #tipo_iva es texto ("4", "10", "21") asi que hay que pasarlo a numero
            iva = float(producto.tipo_iva or 0)
            producto.precio_final = producto.precio + producto.precio * iva / 100

    #caducado si la fecha es anterior a hoy
    @api.depends("fecha_caducidad")
    def _compute_caducado(self):
        hoy = fields.Date.today()
        for producto in self:
            if producto.fecha_caducidad and producto.fecha_caducidad < hoy:
                producto.caducado = True
            else:
                producto.caducado = False

    # no se puede guardar con el stock negativo
    @api.constrains("stock")
    def _check_stock(self):
        for producto in self:
            if producto.stock < 0:
                raise ValidationError("El stock no puede ser negativo.")

    #cuando cambias la fecha en el formulario si le quedan 3 dias o menos lo pone en oferta solo
    @api.onchange("fecha_caducidad")
    def _onchange_fecha_caducidad(self):
        hoy = fields.Date.today()
        for producto in self:
            if producto.fecha_caducidad and hoy <= producto.fecha_caducidad <= hoy + timedelta(days=3):
                producto.en_oferta = True
