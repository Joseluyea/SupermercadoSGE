from odoo import models, fields, api


class Seccion(models.Model):
    _name = "supermercado.seccion"
    _description = "Sección del supermercado"
    _rec_name = "nombre"

    nombre = fields.Char(string="Nombre", required=True, help="Nombre de la sección, por ejemplo Frutería")

    num_pasillo = fields.Integer(string="Pasillo", help="Número del pasillo donde está la sección")

    descripcion = fields.Text(string="Descripción", help="Descripción o notas de la sección")

    imagen = fields.Binary(string="Imagen", help="Foto de la sección")

    fecha_apertura = fields.Date(string="Fecha de apertura", help="Día en que se abrió la sección")

    # se rellena con el boton Revisar del formulario
    ultima_revision = fields.Datetime(string="Última revisión", readonly=True,
                                      help="Fecha y hora de la última revisión (limpieza, neveras...)")

    activa = fields.Boolean(string="Activa", default=True, help="Si la sección está abierta o no")

    # One2many: una seccion tiene muchos productos
    # 'seccion_id' es el Many2one que hay en el modelo producto
    producto_ids = fields.One2many("supermercado.producto", "seccion_id", string="Productos")

    # campo calculado, no lo rellena el usuario
    num_productos = fields.Integer(string="Nº de productos", compute="_compute_num_productos")

    # cada vez que cambian los productos de la seccion se vuelve a contar
    @api.depends("producto_ids")
    def _compute_num_productos(self):
        for seccion in self:
            seccion.num_productos = len(seccion.producto_ids)

    # metodo del boton Revisar: guarda la fecha y hora de ahora
    def action_revisar(self):
        for seccion in self:
            seccion.ultima_revision = fields.Datetime.now()
        return True
