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
  File: nif.py
  Purpose: 
"""

from django.core.exceptions import ValidationError
from django.forms import RegexField

from delivery_helper_core.widgets import NIFWidget


__author__ = u"Roberto García Carvajal"

__all__ = ['NIFField']


class NIFField(RegexField):
    """
        Spanish NIF and NIE custom form field.
    """
    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = NIFWidget()
        super(NIFField, self).__init__(
            r"^[0-9xyzXYZ][0-9]{7}[a-zA-Z]$", *args, **kwargs
        )

    def clean(self, value):
        value = super(NIFField, self).clean(value)
        if len(value) == 9:
            num = value[:8]
            parity = value[8].upper()
            num = int(num.upper().replace("X", "0").replace("Y", "1").replace("Z", "2"))
            if "TRWAGMYFPDXBNJZSQVHLCKE"[num % 23] != parity:
                raise ValidationError(u"NIF/NIE is not valid.")
        return value
