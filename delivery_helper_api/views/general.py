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
  File: general.py
  Purpose: 
"""

from django.contrib.auth import authenticate
from django.http import JsonResponse

from delivery_helper_core.models import Empresa, Delegacion

from .base import ApiView

__author__ = u"Roberto García Carvajal"

__all__ = ['APILoginView', 'APIEmpresaView', 'APIDelegacionView']


class APILoginView(ApiView):
    def POST(self, request, data):
        user = authenticate(request, username=data.get("username", ""), password=data.get("password", ""))
        if user is not None:
            if user.usuario_set.all().count() == 1:
                usuario = user.usuario_set.all().get()
                apikey = usuario.generate_api_key(data["password"])
                type = 1
            elif user.repartidor_set.all().count() == 1:
                repartidor = user.repartidor_set.all().get()
                apikey = repartidor.generate_api_key(data["password"])
                type = 2
            else:
                return JsonResponse({'success': 0, 'error': "Account API access disabled"})
            return JsonResponse({'success': 1, 'token': apikey, 'type': type})
        return JsonResponse({'success': 0, 'error': "Invalid credentials."})


class APIEmpresaView(ApiView):
    def GET(self, request, data):
        empresas = Empresa.objects.all()
        pk = data.get("pk", None)
        if pk is not None:
            empresas = empresas.filter(pk=pk)
        output = [{
            'pk': empresa.pk,
            'nombre': empresa.nombre,
        } for empresa in empresas]
        return JsonResponse({'success': 1, 'data': output})


class APIDelegacionView(ApiView):
    def GET(self, request, data):
        delegaciones = Delegacion.objects.all()
        pk = data.get("pk", None)
        if pk is not None:
            delegaciones = delegaciones.filter(pk=pk)
        output = [{
            'pk': delegacion.pk,
            'empresa': delegacion.empresa.pk,
            'latitud': delegacion.latitude,
            'longitud': delegacion.latitude,
            'direccion': delegacion.direccion,
        } for delegacion in delegaciones]
        return JsonResponse({'success': 1, 'data': output})
