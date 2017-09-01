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

# Based on Imomaliev django_multiforms_view.py:
# https://gist.github.com/imomaliev/1889aac5b42ce33c5202dd328657a6eb.

"""
  File: base.py
  Purpose: 
"""

from __future__ import unicode_literals, absolute_import

from django import forms
from django.http import Http404
from django.http.response import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.generic.edit import ProcessFormView

from delivery_helper_core.models import Direccion, Entrega


__author__ = u"Roberto García Carvajal"


class MultiFormMixin(ContextMixin):
    form_classes = {}
    prefixes = {}
    success_urls = {}
    grouped_forms = {}

    initial = {}
    prefix = None
    success_url = None

    def get_context_data(self, **kwargs):
        forms = kwargs.pop('forms')
        context_data = super(MultiFormMixin, self).get_context_data(**kwargs)
        context_data.update({'%s_form' % key: value for key, value in forms.items()})
        return context_data

    def get_form_classes(self):
        return self.form_classes

    def get_forms(self, form_classes, form_names=None, bind_all=False):
        return dict(
            [(key, self._create_form(key, klass, (form_names and key in form_names) or bind_all)) for key, klass in form_classes.items()]
        )

    def get_form_kwargs(self, form_name, bind_form=False):
        kwargs = {}
        kwargs.update({'initial': self.get_initial(form_name)})
        if issubclass(self.form_classes[form_name], forms.ModelForm):
            instance = self.get_instance(form_name)
            if instance is not None:
                kwargs.update({'instance': instance})
        kwargs.update({'prefix': self.get_prefix(form_name)})

        if bind_form:
            kwargs.update(self._bind_form_data())

        return kwargs

    def get_instance(self, form_name):
        initial_method = 'get_%s_form_instance' % form_name
        if hasattr(self, initial_method):
            return getattr(self, initial_method)()
        return None

    def forms_valid(self, forms, form_name=None):
        if form_name is not None:
            form_valid_method = '%s_form_valid' % form_name
            if hasattr(self, form_valid_method):
                return getattr(self, form_valid_method)(forms[form_name])
        return self.redirect_to_success_url()

    def redirect_to_success_url(self, form_name=None):
        return HttpResponseRedirect(self.get_success_url(form_name))

    def forms_invalid(self, forms):
        return self.render_to_response(self.get_context_data(forms=forms))

    def get_initial(self, form_name):
        initial_method = 'get_%s_form_initial' % form_name
        if hasattr(self, initial_method):
            return getattr(self, initial_method)()
        else:
            return self.initial.copy()

    def get_prefix(self, form_name):
        return self.prefixes.get(form_name, self.prefix)

    def get_success_url(self, form_name=None):
        return self.success_urls.get(form_name, self.success_url)

    def _create_form(self, form_name, klass, bind_form):
        form_kwargs = self.get_form_kwargs(form_name, bind_form)
        form_create_method = 'create_%s_form' % form_name
        if hasattr(self, form_create_method):
            form = getattr(self, form_create_method)(klass, **form_kwargs)
        else:
            form = klass(**form_kwargs)
        return form

    def _bind_form_data(self):
        if self.request.method in ('POST', 'PUT'):
            return{'data': self.request.POST,
                   'files': self.request.FILES,}
        return {}


class ProcessMultipleFormsView(ProcessFormView):
    def get(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)
        return self.render_to_response(self.get_context_data(forms=forms))

    def post(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        form_name = request.POST.get('action')
        if self._individual_exists(form_name):
            return self._process_individual_form(form_name, form_classes)
        elif self._group_exists(form_name):
            return self._process_grouped_forms(form_name, form_classes)
        else:
            return self._process_all_forms(form_classes)

    def _individual_exists(self, form_name):
        return form_name in self.form_classes

    def _group_exists(self, group_name):
        return group_name in self.grouped_forms

    def _process_individual_form(self, form_name, form_classes):
        forms = self.get_forms(form_classes, (form_name,))
        form = forms.get(form_name)
        if not form:
            return HttpResponseForbidden()
        elif form.is_valid():
            return self.forms_valid(forms, form_name)
        else:
            return self.forms_invalid(forms)

    def _process_grouped_forms(self, group_name, form_classes):
        form_names = self.grouped_forms[group_name]
        forms = self.get_forms(form_classes, form_names)
        if all([forms.get(form_name).is_valid() for form_name in form_names.values()]):
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)

    def _process_all_forms(self, form_classes):
        forms = self.get_forms(form_classes, None, True)
        if all([form.is_valid() for form in forms.values()]):
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)


class BaseMultipleFormsView(MultiFormMixin, ProcessMultipleFormsView):
    """
    A base view for displaying several forms.
    """


class MultiFormsView(TemplateResponseMixin, BaseMultipleFormsView):
    """
    A view for displaying several forms, and rendering a template response.
    """


def usuario_required(f):
    def _usuario_required(*args, **kwargs):
        request = args[0]
        if request.user.usuario_set.all().count() != 1:
            raise Http404("Page not found")
        return f(*args, **kwargs)
    return _usuario_required


def repartidor_required(f):
    def _repartidor_required(*args, **kwargs):
        request = args[0]
        if request.user.repartidor_set.all().count() != 1:
            raise Http404("Page not found")
        return f(*args, **kwargs)
    return _repartidor_required


def owns_direccion(f):
    def _owns_direccion(*args, **kwargs):
        request = args[0]
        pk = kwargs.get("pk", None)
        if pk is None:
            raise Http404("Page not found")
        direcciones = Direccion.objects.all().filter(pk=pk)
        direcciones = direcciones.filter(usuario__user=request.user.pk).distinct()
        if direcciones.count() == 0:
            raise Http404("Page not found")
        return f(*args, **kwargs)
    return _owns_direccion


def owns_entrega(f):
    def _owns_entrega(*args, **kwargs):
        request = args[0]
        pk = kwargs.get("pk", None)
        if pk is None:
            raise Http404("Page not found")
        entregas = Entrega.objects.all().filter(pk=pk)
        entregas = entregas.filter(usuario__user=request.user.pk).distinct()
        if entregas.count() == 0:
            raise Http404("Page not found")
        return f(*args, **kwargs)
    return _owns_entrega


def owns_reparto(f):
    def _owns_reparto(*args, **kwargs):
        request = args[0]
        pk = kwargs.get("pk", None)
        if pk is None:
            raise Http404("Page not found")
        entregas = Entrega.objects.all().filter(pk=pk)
        entregas = entregas.filter(repartidor__user=request.user.pk).distinct()
        if entregas.count() == 0:
            raise Http404("Page not found")
        return f(*args, **kwargs)
    return _owns_reparto
