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
  File: parametroconsulta.py
  Purpose: ParametroConsulta model module.
"""

from django.db import models

from .empresa import Empresa

__author__ = u"Roberto García Carvajal"

__all__ = ['ParametroConsulta']


PARAMETROCONSULTA_PARAMETRO_CHOICES = (
    (1, 'nif'),
    (2, 'codigo_postal'),
    (3, 'numero_seguimiento'),
)


class ParametroConsulta(models.Model):
    """
        ParametroConsulta model.
    """
    nombre = models.CharField(max_length=40)
    parametro = models.IntegerField(choices=PARAMETROCONSULTA_PARAMETRO_CHOICES)
    empresa = models.ForeignKey(Empresa, related_name='parametroconsulta')

    def __unicode__(self):
        return u"[%s] (%s) -> %s" % (self.empresa.nombre, self.nombre, self.get_parametro_display())

    class Meta(object):
        """
            Model options for ParametroConsulta.
        """
        app_label = 'delivery_helper_core'
        verbose_name = u"Parámetro consulta"
        verbose_name_plural = u"Parámetros consulta"
