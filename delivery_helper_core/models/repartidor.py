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
  File: repartidor.py
  Purpose: 
"""

import hashlib

from django.db import models

from .usuariobase import UsuarioBase
from .empresa import Empresa

__author__ = u"Roberto García Carvajal"

__all__ = ['Repartidor']


class Repartidor(UsuarioBase):
    """
        Repartidor model.
    """
    empresa = models.ForeignKey(Empresa, related_name='repartidor')

    def __unicode__(self):
        return u"Repartidor: %s, %s" % (self.user.last_name, self.user.first_name)

    def generate_api_key(self, password):
        self.apikey = hashlib.sha256("%s-%s-%s" % (self.user.username, password, 2)).hexdigest()
        self.save()
        return self.apikey

    class Meta(object):
        """
            Model options for Repartidor.
        """
        app_label = 'delivery_helper_core'
        verbose_name_plural = u"Repartidores"
