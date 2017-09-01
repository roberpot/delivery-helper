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
  File: entregausuario.py
  Purpose:
"""

from django import forms

from delivery_helper_core.models import Entrega, Direccion, Delegacion

__author__ = u"Roberto García Carvajal"

__all__ = ['EntregaUsuarioForm']


class EntregaUsuarioForm(forms.ModelForm):
    """
        Repartidor Form class.
    """

    def __init__(self, *args, **kwargs):
        super(EntregaUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['direccion']._set_queryset(Direccion.objects.all().filter(usuario=self.instance.usuario))
        self.fields['delegacion']._set_queryset(Delegacion.objects.all().filter(empresa=self.instance.empresa))

    def clean(self):
        data = super(EntregaUsuarioForm, self).clean()
        direccion = data.get('direccion', None)
        delegacion = data.get('delegacion', None)
        if direccion is None and delegacion is None:
            raise forms.ValidationError("Non change specified.")
        if direccion is not None and delegacion is not None:
            raise forms.ValidationError("Both change specified.")
        return data

    class Meta(object):
        """
            EntregaUsuarioForm form options.
        """
        model = Entrega
        fields = ('delegacion', 'direccion')

