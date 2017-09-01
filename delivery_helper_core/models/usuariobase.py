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
  File: usuariobase.py
  Purpose: UsuarioBase model module.
"""

from django.db import models
from django.contrib.auth.models import User

from delivery_helper_core.fields import NIFField, SpanishPhoneField


__author__ = u"Roberto García Carvajal"

__all__ = ['UsuarioBase']


class UsuarioBase(models.Model):
    """
        UsuarioBase model.
        Base model for Usuario and Repartidor.
    """
    user = models.ForeignKey(User, verbose_name=u"Usuario")
    nif = NIFField(verbose_name=u"NIF/NIE")
    phone = SpanishPhoneField(verbose_name=u"Teléfono")
    email = models.EmailField(verbose_name=u"Correo electrónico")
    longitude = models.FloatField(verbose_name=u"Longitud", null=True, blank=True)
    latitude = models.FloatField(verbose_name=u"Latitude", null=True, blank=True)
    apikey = models.CharField(verbose_name=u"API Key", null=True, blank=True, max_length=64)

    class Meta(object):
        """
            Model options for UsuarioBase.
        """
        app_label = 'delivery_helper_core'
        abstract = True
