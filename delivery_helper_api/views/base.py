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
  File: base.py
  Purpose: 
"""


from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, View

from delivery_helper_core.models import Usuario, Repartidor


__author__ = u"Roberto García Carvajal"


class ApiView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.GET(request, request.GET)
        if request.method == 'POST':
            return self.POST(request, request.POST)
        if request.method == 'PUT':
            return self.PUT(request, request.GET)
        if request.method == 'PATCH':
            return self.PATCH(request, request.GET)
        if request.method == 'DELETE':
            return self.DELETE(request, request.GET)
        if request.method == 'HEAD':
            return self.HEAD(request, request.GET)
        if request.method == 'OPTIONS':
            return self.OPTIONS(request, request.GET)
        if request.method == 'TRACE':
            return self.TRACE(request, request.GET)
        return JsonResponse({'success': 0, 'error': "Method not allowed here."})

    def GET(self, request, data):
        return JsonResponse({'success': 0, 'error': "Method not allowed here."})

    def POST(self, request, data):
        return JsonResponse({'success': 0, 'error': "Method not allowed here."})

    def PUT(self, request, data):
        return JsonResponse({'success': 0, 'error': "Method not allowed here."})

    def PATCH(self, request, data):
        return JsonResponse({'success': 0, 'error': "Method not allowed here."})

    def DELETE(self, request, data):
        return JsonResponse({'success': 0, 'error': "Method not allowed here."})

    def HEAD(self, request, data):
        return JsonResponse({'success': 0, 'error': "Method not allowed here."})

    def OPTIONS(self, request, data):
        return JsonResponse({'success': 0, 'error': "Method not allowed here."})

    def TRACE(self, request, data):
        return JsonResponse({'success': 0, 'error': "Method not allowed here."})


def usuario_apikey_required(f):
    def _usuario_apikey_required(*args, **kwargs):
        request = args[1]
        apikey = request.GET.get("key", None)
        if apikey is None:
            return JsonResponse({'success': 0, 'error': "API KEY not found."})
        usuarios = Usuario.objects.all()
        usuarios = usuarios.filter(apikey=apikey)
        usuarios = usuarios.distinct()
        if usuarios.count() != 1:
            return JsonResponse({'success': 0, 'error': "API KEY error."})
        request.session['usuario'] = usuarios.get()
        ret = f(*args, **kwargs)
        del(request.session['usuario'])
        return ret
    return _usuario_apikey_required


def repartidor_apikey_required(f):
    def _repartidor_apikey_required(*args, **kwargs):
        request = args[1]
        apikey = request.GET.get("key", None)
        if apikey is None:
            return JsonResponse({'success': 0, 'error': "API KEY not found."})
        repartidores = Repartidor.objects.all()
        repartidores = repartidores.filter(apikey=apikey)
        repartidores = repartidores.distinct()
        if repartidores.count() != 1:
            return JsonResponse({'success': 0, 'error': "API KEY error."})
        request.session['repartidor'] = repartidores.get()
        ret = f(*args, **kwargs)
        del(request.session['repartidor'])
        return ret
    return _repartidor_apikey_required
