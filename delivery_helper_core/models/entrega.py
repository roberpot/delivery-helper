# -*- coding: utf-8 -*-

# This file is part of delivery_helper.
# delivery_helper is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# delivery_helper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with delivery_helper. If not, see <http://www.gnu.org/licenses/>.

"""
  File: entrega.py
  Purpose: Entrega model module.
"""

from django.db import models

from .delegacion import Delegacion
from .direccion import Direccion
from .empresa import Empresa
from .notificacion import Notificacion
from .repartidor import Repartidor
from .usuario import Usuario

__author__ = u"Roberto García Carvajal"

__all__ = ['Entrega']


class Entrega(models.Model):
    """
        Entrega model.
    """
    numero_seguimiento = models.CharField(verbose_name=u"Número de seguimiento", max_length=100)
    delegacion = models.ForeignKey(Delegacion, null=True, blank=True, related_name='entrega')
    direccion = models.ForeignKey(Direccion, related_name='entrega', null=True, blank=True)
    empresa = models.ForeignKey(Empresa, related_name='entrega')
    repartidor = models.ForeignKey(Repartidor, null=True, blank=True, related_name='entrega')
    usuario = models.ForeignKey(Usuario, related_name='entrega')
    en_reparto = models.BooleanField(default=False)
    entregado = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s/#%s" % (self.empresa.nombre, self.numero_seguimiento)

    def esta_en_reparto(self):
        if not self.en_reparto:
            self.en_reparto = self.empresa.esta_en_reparto(self)
            if self.en_reparto:
                self.save()
        return self.en_reparto

    def notificar_repartidor(self, texto):
        if self.repartidor is None:
            return
        notificacion = Notificacion(propietario=self.repartidor.user, texto=texto)
        notificacion.save()

    def notificar_receptor(self, texto):
        notificacion = Notificacion(propietario=self.usuario.user, texto=texto)
        notificacion.save()

    class Meta(object):
        """
            Model options for Entrega.
        """
        app_label = 'delivery_helper_core'
