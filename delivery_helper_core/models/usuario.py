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
  File: usuario.py
  Purpose: 
"""

import hashlib

from .usuariobase import UsuarioBase

__author__ = u"Roberto García Carvajal"

__all__ = ['Usuario']


class Usuario(UsuarioBase):
    """
        Usuario model.
    """

    def __unicode__(self):
        return u"Usuario: %s, %s" % (self.user.last_name, self.user.first_name)

    def generate_api_key(self, password):
        self.apikey = hashlib.sha256("%s-%s-%s" % (self.user.username, password, 1)).hexdigest()
        self.save()
        return self.apikey

    class Meta(object):
        """
            Model options for Usuario.
        """
        app_label = 'delivery_helper_core'
