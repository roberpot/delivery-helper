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
  Purpose: App url map.
"""


from django.conf.urls import url

from . import views


__author__ = u"Roberto García Carvajal"


urlpatterns = [
    # Registered on delivery_helper_app.views.non_model_related
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^notifications/$', views.RemoveNotification.as_view(), name='removenotifications'),

    # Registered on delivery_helper_app.views.usuario
    url(r'^usuario/register/$', views.CreateUsuario.as_view(), name='createusuario'),
    url(r'^usuario/register_success/$', views.CreateUsuarioSuccess.as_view(), name='createusuariosuccess'),
    url(r'^usuario/edit/$', views.EditUsuario.as_view(), name='editusuario'),
    url(r'^usuario/direcciones/$', views.DireccionesList.as_view(), name='direccioneslist'),
    url(r'^usuario/direcciones/create/$', views.CreateDireccion.as_view(), name='createdireccion'),
    url(r'^usuario/direcciones/(?P<pk>[0-9]+)/$', views.ViewDireccion.as_view(), name='viewdireccion'),
    url(r'^usuario/direcciones/(?P<pk>[0-9]+)/edit/$', views.EditDireccion.as_view(), name='editdireccion'),
    url(r'^usuario/direcciones/(?P<pk>[0-9]+)/remove/$', views.RemoveDireccion.as_view(), name='removedireccion'),
    url(r'^usuario/entregas/$', views.EntregasList.as_view(), name='entregaslist'),
    url(r'^usuario/entregas/create/$', views.CreateEntrega.as_view(), name='createentrega'),
    url(r'^usuario/entregas/(?P<pk>[0-9]+)/$', views.ViewEntrega.as_view(), name='viewentrega'),
    url(r'^usuario/entregas/(?P<pk>[0-9]+)/remove/$', views.RemoveEntrega.as_view(), name='removeentrega'),
    url(r'^usuario/entregas/(?P<pk>[0-9]+)/changedir/$', views.CambiarDireccionEntrega.as_view(), name='cambiardireccionentrega'),
    url(r'^usuario/entregas/(?P<pk>[0-9]+)/changedel/$', views.CambiarDelegacionEntrega.as_view(), name='cambiardelegacionentrega'),
    url(r'^usuario/entregas/(?P<pk>[0-9]+)/geo/$', views.ViewEntregaGeo.as_view(), name='viewgeoentrega'),

    # Registered on delivery_helper_app.views.repartidor
    url(r'^repartidor/register/$', views.CreateRepartidor.as_view(), name='createrepartidor'),
    url(r'^repartidor/register_success/$', views.CreateRepartidorSuccess.as_view(), name='createrepartidorsuccess'),
    url(r'^repartidor/register/edit/$', views.EditRepartidor.as_view(), name='editrepartidor'),
    url(r'^repartidor/repartos/$', views.RepartidorEntregasList.as_view(), name='repartidorentregaslist'),
    url(r'^repartidor/repartos/create/$', views.CreateReparto.as_view(), name='repartidorcreateentrega'),
    url(r'^repartidor/repartos/(?P<pk>[0-9]+)/$', views.ViewReparto.as_view(), name='viewreparto'),
    url(r'^repartidor/repartos/(?P<pk>[0-9]+)/remove/$', views.DeleteReparto.as_view(), name='removereparto'),
    url(r'^repartidor/repartos/(?P<pk>[0-9]+)/changedir/$', views.CambiarDireccionReparto.as_view(), name='cambiardireccionreparto'),
    url(r'^repartidor/repartos/(?P<pk>[0-9]+)/deliver/$', views.EntregarReparto.as_view(), name='entregarreparto'),
    url(r'^repartidor/updategeo/', views.UpdateGeolocalization.as_view(), name='updategeo')
]
