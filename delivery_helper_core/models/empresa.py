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
  File: empresa.py
  Purpose: Empresa model module.
"""

import urllib
import urllib2

from django.db import models


__author__ = u"Roberto García Carvajal"

__all__ = ['Empresa']


EMPRESA_METODO_CONSULTA_CHOICES = (
    (1, 'GET'),
    (2, 'POST'),
)


class Empresa(models.Model):
    """
        Empresa model.
    """
    nombre = models.CharField(max_length=30)
    consulta = models.URLField()
    metodo_consulta = models.IntegerField(verbose_name=u"Método de consulta", choices=EMPRESA_METODO_CONSULTA_CHOICES)
    cadena_busqueda = models.CharField(verbose_name=u"Cadena de búsqueda", max_length=30)

    def __unicode__(self):
        return u"Empresa: %s" % self.nombre

    def esta_en_reparto(self, entrega):
        params = {}
        for param in self.parametroconsulta.all():
            if param.parametro == 1:  # NIF.
                params[param.nombre] = entrega.usuario.nif
            elif param.parametro == 2:  # CP.
                params[param.nombre] = entrega.direccion.codigo_postal
            elif param.parametro == 3: # Num_seg
                params[param.nombre] = entrega.numero_seguimiento
        if self.metodo_consulta == 1:
            url = u"%s?%s" % (self.consulta, u"&".join([u"%s=%s" % (key, val) for key, val in params.iteritems()]))
            content = urllib2.urlopen(url).read()
        elif self.metodo_consulta == 2:
            url = self.consulta
            content = urllib2.urlopen(url, urllib.urlencode(params)).read()
        decoded = False
        while not decoded:
            try:
                content = content.decode('utf8')
                decoded = True
            except UnicodeDecodeError, e:
                content = content.replace(content[e.start], '')
        if content.find(self.cadena_busqueda) != -1:
            return True
        return False

    class Meta(object):
        """
            Model options for Empresa.
        """
        app_label = 'delivery_helper_core'
