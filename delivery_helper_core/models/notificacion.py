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
  File: notificacion.py
  Purpose: 
"""

from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models


__author__ = u"Roberto García Carvajal"

__all__ = ['Notificacion']


class Notificacion(models.Model):
    """
        Notificacion model.
    """
    propietario = models.ForeignKey(User)
    fecha = models.DateTimeField(auto_now_add=True)
    texto = models.CharField(max_length=200)

    @classmethod
    def remove_old(cls, propietario):
        notificaciones = cls.objects.all().filter(propietario=propietario)
        d = datetime.today() - timedelta(days=1)
        notificaciones = notificaciones.filter(fecha__lte=d)
        notificaciones.delete()

    @classmethod
    def get_for_user(cls, propietario):
        cls.remove_old(propietario)
        notificaciones = cls.objects.all().filter(propietario=propietario)
        notificaciones = notificaciones.order_by('fecha')
        return notificaciones

    class Meta(object):
        """
            Notificacion model options.
        """
        app_label = "delivery_helper_core"
        verbose_name = u"Notificación"
        verbose_name_plural = u"Notificaciones"
