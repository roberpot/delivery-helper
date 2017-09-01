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

from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.messages import error, success
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from delivery_helper_core.models import Entrega

from delivery_helper_app.forms import CreateUserForm, RepartidorForm, RepartoForm, CambiarDireccionForm, ChangeUserForm

from .base import MultiFormsView, owns_reparto, repartidor_required


__author__ = u"Roberto García Carvajal"

__all__ = ['CreateRepartidor', 'CreateRepartidorSuccess', 'RepartidorEntregasList', 'CreateReparto', 'ViewReparto',
           'DeleteReparto', 'CambiarDireccionReparto', 'EntregarReparto', 'EditRepartidor', 'UpdateGeolocalization']


class CreateRepartidor(MultiFormsView):
    """
        Create Usuario view.
    """
    form_classes = {'0': CreateUserForm, '1': RepartidorForm}
    template_name = "delivery_helper_app/repartidor_create.html"
    success_urls = {None: reverse_lazy('createrepartidorsuccess')}

    def forms_valid(self, forms):
        user_form = forms['0']
        repartidor_form = forms['1']
        user_form.save()
        repartidor_form.save(commit=False)
        usuario = repartidor_form.instance
        usuario.user = user_form.instance
        usuario.save()
        return self.redirect_to_success_url()


class CreateRepartidorSuccess(TemplateView):
    template_name = 'delivery_helper_app/repartidor_create_success.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(repartidor_required, name='dispatch')
class EditRepartidor(MultiFormsView):
    """
        Create Usuario view.
    """
    form_classes = {'0': ChangeUserForm, '1': RepartidorForm}
    template_name = "delivery_helper_app/usuario_edit.html"
    success_urls = {None: reverse_lazy('index')}

    def forms_valid(self, forms):
        forms['0'].save()
        forms['1'].save()
        success(self.request, u"Perfil actualizado con éxito")
        return self.redirect_to_success_url()

    def get_0_form_instance(self):
        return self.request.user

    def get_1_form_instance(self):
        return self.request.user.repartidor_set.all().get()


@method_decorator(login_required, name='dispatch')
class RepartidorEntregasList(ListView):
    model = Entrega
    template_name = 'delivery_helper_app/repartidor_entrega_list.html'

    def get_queryset(self):
        return Entrega.objects.all().filter(repartidor__user=self.request.user)


@method_decorator(login_required, name='dispatch')
class CreateReparto(FormView):
    """
        Create Entrega view.
    """
    form_class = RepartoForm
    template_name = 'delivery_helper_app/entrega_create.html'

    def get_form_kwargs(self):
        kwargs = super(CreateReparto, self).get_form_kwargs()
        kwargs['repartidor'] = self.request.user.repartidor_set.all().get()
        return kwargs

    def form_invalid(self, form):
        error(self.request, u"Errores en el formulario.")
        return super(CreateReparto, self).form_invalid(form)

    def form_valid(self, form):
        reparto = form.entrega
        reparto.repartidor = form.repartidor
        reparto.save()
        success(self.request, u"Reparto %s asociado con éxito." % reparto)
        return HttpResponseRedirect(reverse_lazy('repartidorentregaslist'))


@method_decorator(login_required, name='dispatch')
@method_decorator(owns_reparto, name='dispatch')
class ViewReparto(DetailView):
    """
        View Reparto view.
    """
    template_name = 'delivery_helper_app/reparto_view.html'

    def get_object(self, queryset=None):
        repartos = Entrega.objects.all()
        repartos = repartos.filter(repartidor__user=self.request.user)
        repartos = repartos.filter(pk=self.kwargs['pk'])
        repartos = repartos.distinct()
        if repartos.count() == 1:
            return repartos.get()
        raise Http404("Page not found")


@method_decorator(login_required, name='dispatch')
@method_decorator(owns_reparto, name='dispatch')
class DeleteReparto(TemplateView):
    template_name = 'delivery_helper_app/reparto_remove.html'

    def post(self, *args, **kwargs):
        repartos = Entrega.objects.all()
        repartos = repartos.filter(repartidor__user=self.request.user)
        repartos = repartos.filter(pk=self.kwargs['pk'])
        repartos = repartos.distinct()
        if repartos.count() == 1:
            reparto = repartos.get()
            reparto.repartidor = None
            reparto.save()
            success(self.request, u"Reparto desvinculado con éxito.")
            return HttpResponseRedirect(reverse_lazy('repartidorentregaslist'))
        raise Http404("Page not found")


@method_decorator(login_required, name='dispatch')
@method_decorator(owns_reparto, name='dispatch')
class CambiarDireccionReparto(FormView):
    """
        Create Entrega view.
    """
    form_class = CambiarDireccionForm
    template_name = 'delivery_helper_app/reparto_cambiardireccion.html'
    reparto = None

    def get_reparto(self):
        if self.reparto is not None:
            return self.reparto
        repartos = Entrega.objects.all()
        repartos = repartos.filter(repartidor__user=self.request.user)
        repartos = repartos.filter(pk=self.kwargs['pk'])
        repartos = repartos.distinct()
        if repartos.count() != 1:
            raise Http404("Page not found")
        self.reparto = repartos.get()
        return self.reparto

    def get_form_kwargs(self):
        reparto = self.get_reparto()
        kwargs = super(CambiarDireccionReparto, self).get_form_kwargs()
        kwargs['usuario'] = reparto.usuario
        kwargs['direccion_previa'] = reparto.direccion
        return kwargs

    def form_invalid(self, form):
        error(self.request, u"Errores en el formulario.")
        return super(CambiarDireccionReparto, self).form_invalid(form)

    def form_valid(self, form):
        reparto = self.get_reparto()
        reparto.direccion = form.cleaned_data['direccion']
        reparto.save()
        reparto.notificar_receptor(u"Dirección de entrega de %s actualizado por el repartidor." % reparto.numero_seguimiento)
        success(self.request, u"Dirección de entrega de %s actualizada con éxito." % reparto)
        return HttpResponseRedirect(reverse_lazy('repartidorentregaslist'))


@method_decorator(login_required, name='dispatch')
@method_decorator(owns_reparto, name='dispatch')
class EntregarReparto(TemplateView):
    template_name = 'delivery_helper_app/reparto_delivery.html'
    reparto = None

    def get_reparto(self):
        if self.reparto is not None:
            return self.reparto
        repartos = Entrega.objects.all()
        repartos = repartos.filter(repartidor__user=self.request.user)
        repartos = repartos.filter(pk=self.kwargs['pk'])
        repartos = repartos.filter(entregado=False)
        repartos = repartos.distinct()
        if repartos.count() != 1:
            raise Http404("Page not found")
        self.reparto = repartos.get()
        return self.reparto

    def get(self, *args, **kwargs):
        self.get_reparto()
        return super(EntregarReparto, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        reparto = self.get_reparto()
        reparto.entregado = True
        reparto.repartidor = None
        reparto.save()
        reparto.notificar_receptor(u"Entrega de %s realizada." % reparto.numero_seguimiento)
        success(self.request, u"Reparto marcado como entregado.")
        return HttpResponseRedirect(reverse_lazy('repartidorentregaslist'))


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class UpdateGeolocalization(View):

    def dispatch(self, request, *args, **kwargs):
        repartidor = self.request.user.repartidor_set.all()
        if repartidor.count() != 1:
            raise Http404("Page not found")
        repartidor = repartidor.get()
        repartidor.longitude = request.POST['lon']
        repartidor.latitude = request.POST['lat']
        repartidor.save()
        return JsonResponse({'status': 'success'})
