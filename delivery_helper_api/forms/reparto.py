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
  File: reparto.py
  Purpose:
"""

from django import forms

from delivery_helper_core.models import Entrega, Direccion

__author__ = u"Roberto García Carvajal"

__all__ = ['RepartoRepartidorForm']


class RepartoRepartidorForm(forms.ModelForm):
    """
        Repartidor Form class.
    """

    def __init__(self, *args, **kwargs):
        super(RepartoRepartidorForm, self).__init__(*args, **kwargs)
        self.fields['direccion']._set_queryset(Direccion.objects.all().filter(usuario=self.instance.usuario))

    class Meta(object):
        """
            EntregaUsuarioForm form options.
        """
        model = Entrega
        fields = ('direccion', 'entregado')

