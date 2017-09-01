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
  File: wsgi.py
  Purpose: WSGI config for delivery_helper project.
           It exposes the WSGI callable as a module-level variable named ``application``.
           For more information on this file, see
           https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

#import os

from django.core.wsgi import get_wsgi_application

# On this project,
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "delivery_helper.settings")

application = get_wsgi_application()
