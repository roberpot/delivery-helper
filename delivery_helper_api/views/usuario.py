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
  File: usuario.py
  Purpose: 
"""

from django.http import JsonResponse

from delivery_helper_core.models import Direccion, Entrega, Notificacion
from delivery_helper_app.forms import DireccionForm, EntregaForm

from delivery_helper_api.forms import EntregaUsuarioForm

from .base import ApiView, usuario_apikey_required

__author__ = u"Roberto García Carvajal"

__all__ = ['APIDireccionView', 'APIEntregaView', 'APINotificacionesUsuario']


DIC_BOOL = {True: "1", False: "0"}


class APIDireccionView(ApiView):
    def direcciones(self, request, data):
        direcciones = Direccion.objects.all()
        direcciones = direcciones.filter(usuario=request.session['usuario'])
        direcciones = direcciones.distinct()
        pk = data.get("pk", None)
        if pk is not None:
            direcciones = direcciones.filter(pk=pk)
        return direcciones


    @usuario_apikey_required
    def GET(self, request, data):
        direcciones = self.direcciones(request, data)
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

    @usuario_apikey_required
    def POST(self, request, data):
        if request.GET.get("pk", None) is not None:
            instance = self.direcciones(request, request.GET)
            if instance.count() != 1:
                return JsonResponse({'success': 0, 'error': "Does not exists."})
            instance = instance.get()
            form = DireccionForm(data, instance=instance)
        else:
            form = DireccionForm(data)
        if form.is_valid():
            form.save(commit=False)
            instance = form.instance
            instance.usuario = request.session['usuario']
            instance.save()
            if instance.get_geolocalization():
                instance.save()
                return JsonResponse({'success': 1, 'pk': form.instance.pk})
            else:
                return JsonResponse({'success': 2, 'pk': form.instance.pk, 'error': "Geo failed."})
        else:
            return JsonResponse({'success': 0, 'error': form.errors})

    @usuario_apikey_required
    def DELETE(self, request, data):
        instance = self.direcciones(request, data)
        if instance.count() != 1:
            return JsonResponse({'success': 0, 'error': "Does not exists."})
        instance = instance.get()
        instance.delete()
        return JsonResponse({'success': 1})


class APIEntregaView(ApiView):

    def entregas(self, request, data):
        entregas = Entrega.objects.all()
        entregas = entregas.filter(usuario=request.session['usuario'])
        entregas = entregas.distinct()
        pk = data.get("pk", None)
        if pk is not None:
            entregas = entregas.filter(pk=pk)
        return entregas

    @usuario_apikey_required
    def GET(self, request, data):
        entregas = self.entregas(request, data)
        output = [{
            'pk': e.pk,
            'empresa': e.empresa.pk,
            'numero_seguimiento': e.numero_seguimiento,
            'reparto': DIC_BOOL[e.esta_en_reparto()],
            'entregado': DIC_BOOL[e.entregado],
            'direccion': e.direccion is None and "0" or e.direccion.pk,
            'delegacion': e.delegacion is None and "0" or e.delegacion.pk,
            'repartidor': e.repartidor is None and "0" or "1",
            'latitud_repartidor': e.repartidor is not None and e.repartidor.latitude or "",
            'longitud_repartidor': e.repartidor is not None and e.repartidor.longitude or "",
            'latitud_destino': (
                (e.direccion is not None and e.direccion.latitude) or
                (e.delegacion is not None and e.delegacion.latitude) or
                ""),
            'longitud_destino': (
                (e.direccion is not None and e.direccion.longitude) or
                (e.delegacion is not None and e.delegacion.longitude) or
                "")
        } for e in entregas]
        return JsonResponse({'success': 1, 'data': output})

    @usuario_apikey_required
    def POST(self, request, data):
        if request.GET.get("pk", None) is not None:
            entregas = self.entregas(request, request.GET)
            entregas = entregas.filter(entregado=False)
            if entregas.count() != 1:
                return JsonResponse({'success': 0, 'error': "Does not exists."})
            instance = entregas.get()
            form = EntregaUsuarioForm(data, instance=instance)
            if form.is_valid():
                form.save()
                if instance is not None:
                    if form.cleaned_data.get('direccion', None) is not None:
                        instance.notificar_repartidor(
                            u"Dirección de entrega de %s actualizado por el usuario." % instance.numero_seguimiento)
                    else:
                        instance.notificar_repartidor(
                            u"Delegación de entrega de %s actualizado por el usuario." % instance.numero_seguimiento)
                return JsonResponse({'success': 1, 'pk': form.instance.pk})
            else:
                return JsonResponse({'success': 0, 'errors': form.errors})
        else:
            form = EntregaForm(data, usuario=request.session['usuario'])
            if form.is_valid():
                form.save(commit=False)
                instance = form.instance
                instance.usuario = request.session['usuario']
                instance.save()
                if instance.esta_en_reparto():
                    return JsonResponse({'success': 1, 'pk': instance.pk})
                else:
                    return JsonResponse({'success': 2, 'pk': instance.pk,
                                         'error': "Can not sync with delivery webpage."})
            else:
                return JsonResponse({'success': 0, 'errors': form.errors})

    @usuario_apikey_required
    def DELETE(self, request, data):
        instance = self.entregas(request, data)
        if instance.count() != 1:
            return JsonResponse({'success': 0, 'error': "Does not exists."})
        instance = instance.get()
        instance.notificar_repartidor(u"Reparto %s eliminado por el usuario." % instance.numero_seguimiento)
        instance.delete()
        return JsonResponse({'success': 1})


class APINotificacionesUsuario(ApiView):
    @usuario_apikey_required
    def GET(self, request, data):
        notificaciones = Notificacion.get_for_user(request.session['usuario'].user)
        output = [{
            'date': n.fecha,
            'msg': n.texto
        } for n in notificaciones]
        notificaciones.delete()
        return JsonResponse({'success': 1, 'data': output})
