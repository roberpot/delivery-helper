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
  Purpose: Repartidor form class module.
"""

from django import forms

from delivery_helper_core.models import Repartidor


__author__ = u"Roberto García Carvajal"

__all__ = ['RepartidorForm']


class RepartidorForm(forms.ModelForm):
    """
        Repartidor Form class.
    """
    class Meta(object):
        """
            Form options for RepartidorForm.
        """
        model = Repartidor
        fields = ('nif', 'phone', 'empresa')
