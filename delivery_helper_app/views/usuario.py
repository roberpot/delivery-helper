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

from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.messages import error, success, warning
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic.list import ListView

from delivery_helper_app.forms import CreateUserForm, UsuarioForm, DireccionForm, EntregaForm, CambiarDireccionForm, \
    ChangeUserForm, CambiarDelegacionForm
from delivery_helper_core.models import Direccion, Entrega

from .base import MultiFormsView, owns_direccion, owns_entrega, usuario_required


__author__ = u"Roberto García Carvajal"

__all__ = ['CreateUsuario', 'CreateUsuarioSuccess', 'DireccionesList', 'CreateDireccion', 'ViewDireccion',
           'EditDireccion', 'RemoveDireccion', 'EntregasList', 'CreateEntrega', 'ViewEntrega', 'RemoveEntrega',
           'CambiarDireccionEntrega', 'EditUsuario', 'CambiarDelegacionEntrega', 'ViewEntregaGeo']


class CreateUsuario(MultiFormsView):
    """
        Create Usuario view.
    """
    form_classes = {'0': CreateUserForm, '1': UsuarioForm}
    template_name = "delivery_helper_app/usuario_create.html"
    success_urls = {None: reverse_lazy('createusuariosuccess')}

    def forms_valid(self, forms):
        user_form = forms['0']
        usuario_form = forms['1']
        user_form.save()
        usuario_form.save(commit=False)
        usuario = usuario_form.instance
        usuario.user = user_form.instance
        usuario.save()
        return self.redirect_to_success_url()


@method_decorator(login_required, name='dispatch')
@method_decorator(usuario_required, name='dispatch')
class EditUsuario(MultiFormsView):
    """
        Create Usuario view.
    """
    form_classes = {'0': ChangeUserForm, '1': UsuarioForm}
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
        return self.request.user.usuario_set.all().get()


class CreateUsuarioSuccess(TemplateView):
    template_name = 'delivery_helper_app/usuario_create_success.html'


@method_decorator(login_required, name='dispatch')
class DireccionesList(ListView):
    model = Direccion
    template_name = 'delivery_helper_app/direccion_list.html'

    def get_queryset(self):
        return Direccion.objects.all().filter(usuario__user=self.request.user)


@method_decorator(login_required, name='dispatch')
class CreateDireccion(FormView):
    """
        Create Direccion view.
    """
    form_class = DireccionForm
    template_name = 'delivery_helper_app/direccion_create.html'

    def form_invalid(self, form):
        error(self.request, u"Errores en el formulario.")
        return super(CreateDireccion, self).form_invalid(form)

    def form_valid(self, form):
        form.save(commit=False)
        direccion = form.instance
        direccion.usuario = self.request.user.usuario_set.all().get()
        success(self.request, u"Dirección %s registrada con éxito." % direccion)
        if direccion.get_geolocalization():
            success(self.request, u"Dirección %s geolocalizada con éxito." % direccion)
        else:
            warning(self.request, u"No se puede geolocalizar %s." % direccion)
        direccion.save()
        return HttpResponseRedirect(reverse_lazy('direccioneslist'))


@method_decorator(login_required, name='dispatch')
@method_decorator(owns_direccion, name='dispatch')
class ViewDireccion(DetailView):
    """
        View Direccion view.
    """
    template_name = 'delivery_helper_app/direccion_view.html'

    def get_object(self, queryset=None):
        direcciones = Direccion.objects.all()
        direcciones = direcciones.filter(usuario__user=self.request.user)
        direcciones = direcciones.filter(pk=self.kwargs['pk'])
        direcciones = direcciones.distinct()
        if direcciones.count() != 1:
            raise Http404("Page not found")
        direccion = direcciones.get()
        if direccion.latitude is None:
            if direccion.get_geolocalization():
                success(self.request, u"Dirección %s geolocalizada con éxito." % direccion)
                direccion.save()
            else:
                warning(self.request, u"No se puede geolocalizar %s." % direccion)
        return direccion


class EditDireccion(UpdateView):
    """
        View Direccion view.
    """
    form_class = DireccionForm
    model = Direccion
    template_name = 'delivery_helper_app/direccion_edit.html'

    def form_valid(self, form):
        success(self.request, u"Dirección editada correctamente.")
        ret = super(EditDireccion, self).form_valid(form)
        direccion = form.instance
        if direccion.get_geolocalization():
            success(self.request, u"Dirección %s geolocalizada con éxito." % direccion)
            direccion.save()
        else:
            warning(self.request, u"No se puede geolocalizar %s." % direccion)
        return ret

    def form_invalid(self, form):
        error(self.request, u"Error editando dirección.")
        return super(EditDireccion, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('editdireccion', kwargs=self.kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(owns_direccion, name='dispatch')
class RemoveDireccion(DeleteView):
    """
        Remove Direccion view.
    """
    model = Direccion
    template_name = 'delivery_helper_app/direccion_remove.html'

    def get_success_url(self):
        return reverse_lazy('direccioneslist')

    def post(self, *args, **kwargs):
        success(self.request, u"Dirección eliminada correctamente.")
        return super(RemoveDireccion, self).post(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class EntregasList(ListView):
    model = Entrega
    template_name = 'delivery_helper_app/entrega_list.html'

    def get_queryset(self):
        return Entrega.objects.all().filter(usuario=self.request.user.usuario_set.all().get())


@method_decorator(login_required, name='dispatch')
class CreateEntrega(FormView):
    """
        Create Entrega view.
    """
    form_class = EntregaForm
    template_name = 'delivery_helper_app/entrega_create.html'

    def get_form_kwargs(self):
        kwargs = super(CreateEntrega, self).get_form_kwargs()
        kwargs['usuario'] = self.request.user.usuario_set.all().get()
        return kwargs

    def form_invalid(self, form):
        error(self.request, u"Errores en el formulario.")
        return super(CreateEntrega, self).form_invalid(form)

    def form_valid(self, form):
        form.save(commit=False)
        entrega = form.instance
        entrega.usuario = self.request.user.usuario_set.all().get()
        entrega.save()
        success(self.request, u"Entrega %s registrada con éxito." % entrega)
        if entrega.esta_en_reparto():
            success(self.request, u"La entrega %s está en reparto." % entrega)
        else:
            warning(self.request, u"No se puede determinar si la entrega %s está ya en reparto." % entrega)
        return HttpResponseRedirect(reverse_lazy('entregaslist'))


@method_decorator(login_required, name='dispatch')
@method_decorator(owns_entrega, name='dispatch')
class ViewEntrega(DetailView):
    """
        View Entrega view.
    """
    template_name = 'delivery_helper_app/entrega_view.html'

    def get_object(self, queryset=None):
        entregas = Entrega.objects.all()
        entregas = entregas.filter(usuario__user=self.request.user)
        entregas = entregas.filter(pk=self.kwargs['pk'])
        entregas = entregas.distinct()
        if entregas.count() != 1:
            raise Http404("Page not found")
        entrega = entregas.get()
        if not entrega.en_reparto:
            if entrega.esta_en_reparto():
                success(self.request, u"La entrega %s está en reparto." % entrega)
            else:
                warning(self.request, u"No se puede determinar si la entrega %s está ya en reparto." % entrega)
        return entrega


@method_decorator(login_required, name='dispatch')
@method_decorator(owns_entrega, name='dispatch')
class RemoveEntrega(DeleteView):
    """
        Remove Entrega view.
    """
    model = Entrega
    template_name = 'delivery_helper_app/entrega_remove.html'

    def get_success_url(self):
        return reverse_lazy('entregaslist')

    def post(self, *args, **kwargs):
        success(self.request, u"Entrega eliminada correctamente.")
        self.object.notificar_repartidor(u"Reparto %s eliminado por el usuario." % self.object.numero_seguimiento)
        return super(RemoveEntrega, self).post(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(owns_entrega, name='dispatch')
class CambiarDireccionEntrega(FormView):
    """
        Create Entrega view.
    """
    form_class = CambiarDireccionForm
    template_name = 'delivery_helper_app/entrega_cambiardireccion.html'
    entrega = None

    def get_entrega(self):
        if self.entrega is not None:
            return self.entrega
        entregas = Entrega.objects.all()
        entregas = entregas.filter(usuario__user=self.request.user)
        entregas = entregas.filter(pk=self.kwargs['pk'])
        entregas = entregas.filter(entregado=False)
        entregas = entregas.distinct()
        if entregas.count() != 1:
            raise Http404("Page not found")
        self.entrega = entregas.get()
        return self.entrega

    def get_form_kwargs(self):
        entrega = self.get_entrega()
        kwargs = super(CambiarDireccionEntrega, self).get_form_kwargs()
        kwargs['usuario'] = entrega.usuario
        kwargs['direccion_previa'] = entrega.direccion
        return kwargs

    def form_invalid(self, form):
        error(self.request, u"Errores en el formulario.")
        return super(CambiarDireccionEntrega, self).form_invalid(form)

    def form_valid(self, form):
        entrega = self.get_entrega()
        entrega.direccion = form.cleaned_data['direccion']
        entrega.delegacion = None
        entrega.save()
        entrega.notificar_repartidor(u"Dirección de entrega de %s actualizado por el usuario." % entrega.numero_seguimiento)
        success(self.request, u"Dirección de entrega de %s actualizada con éxito." % entrega)
        return HttpResponseRedirect(reverse_lazy('entregaslist'))


@method_decorator(login_required, name='dispatch')
@method_decorator(owns_entrega, name='dispatch')
class CambiarDelegacionEntrega(FormView):
    """
        Create Entrega view.
    """
    form_class = CambiarDelegacionForm
    template_name = 'delivery_helper_app/entrega_cambiardelegacion.html'
    entrega = None

    def get_entrega(self):
        if self.entrega is not None:
            return self.entrega
        entregas = Entrega.objects.all()
        entregas = entregas.filter(usuario__user=self.request.user)
        entregas = entregas.filter(pk=self.kwargs['pk'])
        entregas = entregas.filter(entregado=False)
        entregas = entregas.distinct()
        if entregas.count() != 1:
            raise Http404("Page not found")
        self.entrega = entregas.get()
        return self.entrega

    def get_form_kwargs(self):
        entrega = self.get_entrega()
        kwargs = super(CambiarDelegacionEntrega, self).get_form_kwargs()
        kwargs['empresa'] = entrega.empresa
        return kwargs

    def form_invalid(self, form):
        error(self.request, u"Errores en el formulario.")
        return super(CambiarDelegacionEntrega, self).form_invalid(form)

    def form_valid(self, form):
        entrega = self.get_entrega()
        entrega.delegacion = form.cleaned_data['delegacion']
        entrega.direccion = None
        entrega.save()
        entrega.notificar_repartidor(u"Delegación de entrega de %s actualizado por el usuario." % entrega.numero_seguimiento)
        success(self.request, u"Delegación de entrega de %s actualizada con éxito." % entrega)
        return HttpResponseRedirect(reverse_lazy('entregaslist'))


@method_decorator(login_required, name='dispatch')
@method_decorator(owns_entrega, name='dispatch')
class ViewEntregaGeo(DetailView):
    """
        View Entrega view.
    """
    template_name = 'delivery_helper_app/entrega_view_geo.html'

    def get_object(self, queryset=None):
        entregas = Entrega.objects.all()
        entregas = entregas.filter(usuario__user=self.request.user)
        entregas = entregas.filter(entregado=False)
        entregas = entregas.exclude(repartidor=None)
        entregas = entregas.filter(en_reparto=True)
        entregas = entregas.filter(pk=self.kwargs['pk'])
        entregas = entregas.distinct()
        if entregas.count() != 1:
            raise Http404("Page not found")
        entrega = entregas.get()
        return entrega
