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
  Purpose: 
"""

from django import forms

from delivery_helper_core.models import Entrega, Direccion

__author__ = u"Roberto García Carvajal"

__all__ = ['RepartoForm']


class RepartoForm(forms.Form):
    """
        Repartidor Form class.
    """
    numero_seguimiento = forms.IntegerField(u"Número de seguimiento")

    def __init__(self, *args, **kwargs):
        self.repartidor = kwargs.pop('repartidor')
        self.entrega = None
        super(RepartoForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(RepartoForm, self).clean()
        num = data.get('numero_seguimiento', None)
        if num is None:
            return data
        entregas = Entrega.objects.all()
        entregas = entregas.filter(empresa=self.repartidor.empresa)
        entregas = entregas.filter(repartidor=None)
        entregas = entregas.filter(numero_seguimiento=num)
        entregas = entregas.filter(entregado=False)
        entregas = entregas.distinct()
        if entregas.count() != 1:
            self.add_error('numero_seguimiento', u"Número de seguimiento incorrecto.")
            return data
        self.entrega = entregas.get()
        return data
