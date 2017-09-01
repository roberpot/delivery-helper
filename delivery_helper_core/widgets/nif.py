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
  Purpose: Widget for Spanish NIF and NIE module.
"""

from django.forms import MultiWidget, TextInput


__author__ = u"Roberto García Carvajal"

__all__ = ['NIFWidget']


class NIFWidget(MultiWidget):
    """
        Widget for Spanish NIF and NIE.
    """
    def __init__(self, attrs=None):
        attrs_1 = {'size': 8, 'maxlength': 8}
        attrs_2 = {'size': 1, 'maxlength': 1}
        super(NIFWidget, self).__init__(
            [TextInput(attrs=attrs_1),
             TextInput(attrs=attrs_2)], attrs=attrs)

    def decompress(self, value):
        if not isinstance(value, basestring):
            return [None, None]
        value = value[:9]
        value_1 = value[:8]
        value_2 = u""
        if len(value) == 9:
            value_2 = value[8]
        return [value_1, value_2]

    def value_from_datadict(self, data, files, name):
        ret = super(NIFWidget, self).value_from_datadict(data, files, name)
        if isinstance(ret, list) and len(ret) == 2:
            return "".join(ret)
        return ret
