from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Empleado(models.Model):
    _name = "supermercado.empleado"
    _description = "Empleado del supermercado"
    _rec_name = "nombre"

    nombre = fields.Char(string="Nombre", required=True, help="Nombre del empleado")

    apellidos = fields.Char(string="Apellidos", help="Apellidos del empleado")

    dni = fields.Char(string="DNI", help="DNI del empleado")

    foto = fields.Binary(string="Foto", help="Foto del empleado")

    fecha_nacimiento = fields.Date(string="Fecha de nacimiento", required=True, help="Fecha de nacimiento del empleado")

    #se calcula con la fecha de nacimiento
    edad = fields.Integer(string="Edad", compute="_compute_edad")

    puesto = fields.Selection(selection=[("cajero", "Cajero"),
                                         ("reponedor", "Reponedor"),
                                         ("carnicero", "Carnicero"),
                                         ("frutero", "Frutero"),
                                         ("encargado", "Encargado")],
                              string="Puesto", required=True, default="reponedor",
                              help="Puesto de trabajo del empleado")

    turno = fields.Selection(selection=[("manana", "Mañana"),
                                        ("tarde", "Tarde")],
                             string="Turno", required=True, default="manana",
                             help="Turno en el que trabaja")

    salario = fields.Float(string="Salario", help="Salario bruto al mes")

    jornada_completa = fields.Boolean(string="Jornada completa", default=True,
                                      help="Si trabaja a jornada completa o a media jornada")

    #se rellena al darle a Fichar
    ultimo_fichaje = fields.Datetime(string="Último fichaje", readonly=True,
                                     help="Fecha y hora de la última vez que fichó")

    observaciones = fields.Text(string="Observaciones", help="Notas sobre el empleado")

    #Many2one a seccion, el One2many esta en seccion.py
    seccion_id = fields.Many2one("supermercado.seccion", string="Sección", help="Sección en la que trabaja")

    #calcula la edad cada vez que cambia la fecha de nacimiento
    @api.depends("fecha_nacimiento")
    def _compute_edad(self):
        hoy = fields.Date.today()
        for empleado in self:
            if empleado.fecha_nacimiento:
                nacimiento = empleado.fecha_nacimiento
                #se le resta 1 si este año todavia no a cumplido
                empleado.edad = hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
            else:
                empleado.edad = 0

    # Si tiene menos de 16 años no deja guardarlo
    @api.constrains("fecha_nacimiento")
    def _check_edad(self):
        for empleado in self:
            if empleado.edad < 16:
                raise ValidationError("El empleado tiene que tener por lo menos 16 años.")

    #metodo del boton fichar
    def action_fichar(self):
        for empleado in self:
            empleado.ultimo_fichaje = fields.Datetime.now()
        return True
