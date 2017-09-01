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
  File: direccion.py
  Purpose: Direccion model module.
"""

import geocoder

from django.conf import settings
from django.db import models
from django.utils.encoding import smart_str

from delivery_helper_core.fields import NIFField

from .usuario import Usuario


__author__ = u"Roberto García Carvajal"

__all__ = ['Direccion']


DIRECCION_TIPOVIA_CHOICES = (
    (u"calle", u"Calle"),
    (u"plaza", u"Plaza"),
    (u"avenida", u"Avenida"),
)


class Direccion(models.Model):
    """
        Direccion model.
    """
    tipovia = models.CharField(verbose_name=u"Tipo de vía", max_length=7, choices=DIRECCION_TIPOVIA_CHOICES)
    nombre_via = models.CharField(verbose_name=u"Nombre vía", max_length=50)
    numero = models.IntegerField(verbose_name=u"Número", blank=True, null=True)
    planta = models.CharField(max_length=10, blank=True, null=True)
    puerta = models.CharField(max_length=3, blank=True, null=True)
    localidad = models.CharField(max_length=20)
    provincia = models.CharField(max_length=20)
    codigo_postal = models.IntegerField(verbose_name=u"Código postal")
    nif = NIFField(verbose_name=u"NIF/NIE")
    nombre_completo = models.CharField(max_length=50)
    alias = models.CharField(max_length=20)
    usuario = models.ForeignKey(Usuario, related_name='direccion')
    longitude = models.FloatField(verbose_name=u"Longitud", blank=True, null=True)
    latitude = models.FloatField(verbose_name=u"Latitude", blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.alias

    def get_geolocalization(self):
        try:
            address = "%s %s %s, %s, %s" % (self.tipovia, self.nombre_via, self.numero, self.localidad, self.provincia)
            for x, y in zip(u"áéíóúÁÉÍÓÚñÑ", u"aeiouAEIOUnN"):
                address = address.replace(x, y)
            g = geocoder.google(address)
            self.longitude = g.geometry['coordinates'][0]
            self.latitude = g.geometry['coordinates'][1]
            return True
        except:
            return False

    class Meta(object):
        """
            Model options for Direccion.
        """
        app_label = 'delivery_helper_core'
