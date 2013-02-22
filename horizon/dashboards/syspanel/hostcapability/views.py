#
#    Copyright (C) 2013 Intel Corporation.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from hostcapability.horizon.api import api
from horizon import exceptions
from horizon import forms
from horizon import tables
from .forms import CreateHostCapability, EditHostCapability
from .tables import HostCapabilityTable

LOG = logging.getLogger(__name__)

class IndexView(tables.DataTableView):
    table_class = HostCapabilityTable
    template_name = 'syspanel/hostcapability/index.html'

    def get_data(self):
        request = self.request
        capabilities_list = []
        try:
            capabilities_list = api.host_capability_list(request)
        except:
            exceptions.handle(request, _('Unable to retrieve host capability list.'))
        capabilities_list.sort(key=lambda h: (h.host, h.ip))
        return capabilities_list


class CreateView(forms.ModalFormView):
    form_class = CreateHostCapability
    template_name = 'syspanel/hostcapability/create.html'
    success_url = reverse_lazy('horizon:syspanel:hostcapability:index')


class EditView(forms.ModalFormView):
    form_class = EditHostCapability
    template_name = 'syspanel/hostcapability/edit.html'
    success_url = reverse_lazy('horizon:syspanel:hostcapability:index')

    def get_context_data(self, **kwargs):
        context = super(EditView, self).get_context_data(**kwargs)
        context['host_id'] = self.kwargs['id']
        return context

    def get_initial(self):
        try:
            capability = api.host_capability_get(self.request, self.kwargs['id'])
        except:
            exceptions.handle(self.request,
                _("Unable to retrieve hostcapability data."))
        return {'host_id': capability.id,
                'host': capability.host,
                'ip': capability.ip,
                'rack': capability.rack,
                'vtd_enabled_eth': capability.vtd_enabled_eth,
                'has_node_manager': capability.has_node_manager}
