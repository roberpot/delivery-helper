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
  File: spanishphone.py
  Purpose: 
"""

from django.db import models

from delivery_helper_core.form_fields import SpanishPhoneField as SpanisPhoneFormField

__author__ = u"Roberto García Carvajal"

__all__ = ['SpanishPhoneField']


class SpanishPhoneField(models.CharField):
    """
        Spanish Phone model field.
    """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 12
        super(SpanishPhoneField, self).__init__(*args, **kwargs)

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        return super(SpanishPhoneField, self).formfield(form_class=SpanisPhoneFormField,
                                                        choices_form_class=choices_form_class, **kwargs)
