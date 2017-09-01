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
  File: non_model_related.py
  Purpose: 
"""


from django.contrib.auth import login, logout
from django.contrib.messages import error, success
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views import View

from delivery_helper_core.models import Notificacion


__author__ = u"Roberto García Carvajal"

__all__ = ['Index', 'Login', 'Logout', 'RemoveNotification']


class Index(TemplateView):
    template_name = 'delivery_helper_app/index.html'


class Login(FormView):
    """
        Login view.
    """
    form_class = AuthenticationForm

    def form_invalid(self, form):
        error(self.request, u"Error de acceso: Credenciales incorrectas.")
        return HttpResponseRedirect(reverse_lazy('index'))

    def form_valid(self, form):
        user = form.get_user()
        if user is not None:
            login(self.request, user)
            success(self.request, u"Bienvenido al sistema.")
        else:
            error(self.request, u"Error de acceso: Credenciales incorrectas.")
        return HttpResponseRedirect(reverse_lazy('index'))


class Logout(View):
    """
        Logout view.
    """

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('index'))


class RemoveNotification(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or not request.POST or request.POST.get('pk', None) is None:
            return JsonResponse({'success': 0})
        try:
            pk = int(request.POST.get('pk', None))
        except ValueError:
            return JsonResponse({'success': 0})
        notificaciones = Notificacion.objects.all()
        notificaciones = notificaciones.filter(pk=pk)
        notificaciones = notificaciones.filter(propietario=request.user)
        notificaciones = notificaciones.distinct()
        if notificaciones.count() != 1:
            return JsonResponse({'success': 0})
        notificaciones.delete()
        return JsonResponse({'success': 1})


