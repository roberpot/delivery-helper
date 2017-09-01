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
  File: urls.py
  Purpose: 
"""


from django.conf.urls import url

from . import views


__author__ = u"Roberto García Carvajal"


urlpatterns = [
    # Registered on delivery_helper_api.views.general
    url(r'^login/$', views.APILoginView.as_view()),
    url(r'^empresa/$', views.APIEmpresaView.as_view()),
    url(r'^delegacion/$', views.APIDelegacionView.as_view()),

    # Registered on delivery_helper_api.views.usuario
    url(r'^direccion/$', views.APIDireccionView.as_view()),
    url(r'^entrega/$', views.APIEntregaView.as_view()),
    url(r'^notificaciones_usuario/$', views.APINotificacionesUsuario.as_view()),

    # Registered on delivery_helper_api.views.repartidor
    url(r'^reparto/$', views.APIRepartoView.as_view()),
    url(r'^entregadirecciones/$', views.APIRepartoDireccionesView.as_view()),
    url(r'^updategeo/$', views.APIUpdateGeoView.as_view()),
    url(r'^notificaciones_repartidor/$', views.APINotificacionesRepartidor.as_view()),

]
