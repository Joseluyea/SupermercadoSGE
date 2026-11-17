from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Proveedor(models.Model):
    _name = "supermercado.proveedor"
    _description = "Proveedor del supermercado"
    _rec_name = "nombre"

    nombre = fields.Char(string="Nombre", required=True, help="Nombre de la empresa")

    cif = fields.Char(string="CIF", help="CIF de la empresa")

    telefono = fields.Char(string="Teléfono", help="Teléfono de contacto")

    email = fields.Char(string="Correo", help="Correo electrónico de contacto")

    logo = fields.Binary(string="Logo", help="Logo del proveedor")

    fecha_alta = fields.Date(string="Fecha de alta", help="Desde cuándo trabajamos con este proveedor")

    ultimo_pedido = fields.Datetime(string="Último pedido", help="Fecha y hora del último pedido que le hicimos")

    dias_entrega = fields.Integer(string="Días de entrega", default=1, help="Días que tarda en traer un pedido")

    activo = fields.Boolean(string="Activo", default=True, help="Si seguimos trabajando con este proveedor")

    notas = fields.Text(string="Notas", help="Observaciones sobre el proveedor")

    #Many2many con producto, un proveedor trae muchos productos y un producto lo pueden traer varios proveedores
    #usa la misma tabal que en producto.py pero con las columnas al reves
    producto_ids = fields.Many2many("supermercado.producto",
                                    relation="supermercado_producto_proveedor_rel",
                                    column1="proveedor_id",
                                    column2="producto_id",
                                    string="Productos")

    #los dias de entrega tienen que ser mas de 0
    @api.constrains("dias_entrega")
    def _check_dias_entrega(self):
        for proveedor in self:
            if proveedor.dias_entrega <= 0:
                raise ValidationError("Los días de entrega tienen que ser mayores que cero.")
