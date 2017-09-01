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
  File: delegacion.py
  Purpose: Delegacion model module.
"""

from django.db import models

from .empresa import *

__author__ = u"Roberto García Carvajal"

__all__ = ['Delegacion']


class Delegacion(models.Model):
    """
        Delegacion model.
    """
    direccion = models.CharField(verbose_name=u"Dirección", max_length=100)
    longitude = models.FloatField(verbose_name=u"Longitud")
    latitude = models.FloatField(verbose_name=u"Latitude")
    empresa = models.ForeignKey(Empresa, related_name='delegacion')

    def __unicode__(self):
        return u"Delegación %s (%s)" % (self.empresa.nombre, self.direccion)

    class Meta(object):
        """
            Model options for Delegacion.
        """
        app_label = 'delivery_helper_core'
        verbose_name = u"Delegación"
        verbose_name_plural = u"Delegaciones"
