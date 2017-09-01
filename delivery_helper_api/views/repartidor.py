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
  Purpose: 
"""

from django.http import JsonResponse

from delivery_helper_core.models import Entrega, Notificacion
from delivery_helper_app.forms import RepartoForm

from delivery_helper_api.forms import RepartoRepartidorForm, GeoUpdateForm

from .base import ApiView, repartidor_apikey_required

__author__ = u"Roberto García Carvajal"

__all__ = ['APIRepartoView', 'APIRepartoDireccionesView', 'APIUpdateGeoView', 'APINotificacionesRepartidor']


class APIRepartoView(ApiView):

    def entregas(self, request, data):
        entregas = Entrega.objects.all()
        entregas = entregas.filter(repartidor=request.session['repartidor'])
        entregas = entregas.distinct()
        pk = data.get("pk", None)
        if pk is not None:
            entregas = entregas.filter(pk=pk)
        return entregas

    @repartidor_apikey_required
    def GET(self, request, data):
        entregas = self.entregas(request, data)
        output = [{
            'pk': e.pk,
            'numero_seguimiento': e.numero_seguimiento,
            'direccion': e.direccion is None and "0" or e.direccion.pk,
            'delegacion': e.delegacion is None and "0" or e.delegacion.pk,
        } for e in entregas]
        return JsonResponse({'success': 1, 'data': output})

    @repartidor_apikey_required
    def POST(self, request, data):
        repartidor = request.session['repartidor']
        if request.GET.get("pk", None) is not None:
            entregas = self.entregas(request, request.GET)
            entregas = entregas.filter(entregado=False)
            if entregas.count() != 1:
                return JsonResponse({'success': 0, 'error': "Does not exists."})
            instance = entregas.get()
            form = RepartoRepartidorForm(data, instance=instance)
            if form.is_valid():
                form.save()
                instance = form.instance
                if instance.entregado:
                    instance.repartidor = None
                    instance.notificar_receptor(u"Entrega de %s realizada." % instance.numero_seguimiento)
                    instance.save()
                else:
                    instance.notificar_receptor(
                        u"Dirección de entrega de %s actualizado por el repartidor." % instance.numero_seguimiento)
                return JsonResponse({'success': 1, 'pk': instance.pk})
            else:
                return JsonResponse({'success': 0, 'error': form.errors})
        else:
            form = RepartoForm(data, repartidor=repartidor)
            if form.is_valid():
                instance = form.entrega
                instance.repartidor = repartidor
                instance.save()
                return JsonResponse({'success': 1, 'pk': instance.pk})
            else:
                return JsonResponse({'success': 0, 'error': form.errors})

    @repartidor_apikey_required
    def DELETE(self, request, data):
        instance = self.entregas(request, data)
        if instance.count() != 1:
            return JsonResponse({'success': 0, 'error': "Does not exists."})
        if instance.repartidor != request.session['repartidor']:
            return JsonResponse({'success': 0, 'error': "Does not exists."})
        instance = instance.get()
        instance.repartidor = None
        instance.save()
        return JsonResponse({'success': 1})


class APIRepartoDireccionesView(ApiView):

    def entregas(self, request, data):
        entregas = Entrega.objects.all()
        entregas = entregas.filter(repartidor=request.session['repartidor'])
        entregas = entregas.distinct()
        pk = data.get("pk", None)
        if pk is not None:
            entregas = entregas.filter(pk=pk)
        return entregas

    @repartidor_apikey_required
    def GET(self, request, data):
        pk = data.get('pk', None)
        if pk is None:
            return JsonResponse({'success': 0, 'error': "Does not exists."})
        entregas = self.entregas(request, data)
        entrega = entregas.get()
        direcciones = entrega.usuario.direccion.all()
        output = [{
            'pk': d.pk,
            'alias': d.alias,
            'tipovia': d.tipovia,
            'nombre_via': d.nombre_via,
            'numero': d.numero,
            'planta': d.planta,
            'puerta': d.puerta,
            'localidad': d.localidad,
            'provincia': d.provincia,
            'codigo_postal': d.codigo_postal,
            'nif': d.nif,
            'nombre_completo': d.nombre_completo,
            'lon': d.longitude,
            'lat': d.latitude,
        } for d in direcciones]
        return JsonResponse({'success': 1, 'data': output})


class APIUpdateGeoView(ApiView):

    @repartidor_apikey_required
    def POST(self, request, data):
        repartidor = request.session['repartidor']
        form = GeoUpdateForm(data, instance=repartidor)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': 1})
        else:
            return JsonResponse({'success': 0, 'error': form.errors})


class APINotificacionesRepartidor(ApiView):
    @repartidor_apikey_required
    def GET(self, request, data):
        notificaciones = Notificacion.get_for_user(request.session['repartidor'].user)
        output = [{
            'date': n.fecha,
            'msg': n.texto
        } for n in notificaciones]
        notificaciones.delete()
        return JsonResponse({'success': 1, 'data': output})
