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

from django.utils.translation import ugettext_lazy as _

from hostcapability.horizon.api import api
from horizon import exceptions
from horizon import forms
from horizon import messages


LOG = logging.getLogger(__name__)


class CreateHostCapability(forms.SelfHandlingForm):
    host = forms.CharField(max_length="25", label=_("Host"))
    ip = forms.IPAddressField(label=_("IP"), required=False)
    rack = forms.CharField(max_length="25", label=_("Rack"), required=False)
    vtd_enabled_eth = forms.BooleanField(label=_("VTD_enabled_eth"), required=False)
    has_node_manager = forms.BooleanField(label=_("Has_node_manager"), required=False)

    def handle(self, request, data):
        try:
            capability = api.host_capability_create(request,
                data['host'],
                data['ip'],
                data['rack'],
                data['vtd_enabled_eth'],
                data['has_node_manager'])
            if not capability.host:
                raise exceptions.AlreadyExists(data['host'], 'host capability')
            msg = _('Created capability for host "%s".') % data['host']
            messages.success(request, msg)
            return capability
        except exceptions.AlreadyExists:
            exceptions.handle(request, capability)
        except:
            exceptions.handle(request, _("Unable to create host capability."))


class EditHostCapability(CreateHostCapability):
    host_id = forms.IntegerField(widget=forms.widgets.HiddenInput)

    def handle(self, request, data):
        try:
            # First mark the existing host capability as deleted.
            api.host_capability_delete(request, data['host_id'])
            # Then create a new host capability with the same name but a new ID.
            # This is in the same try/except block as the delete call
            # because if the delete fails the API will error out because
            # active host capability can't have the same name.
            capability = api.host_capability_create(request,
                data['host'],
                data['ip'],
                data['rack'],
                data['vtd_enabled_eth'],
                data['has_node_manager'])
            msg = _('Updated capability for host "%s".') % data['host']
            messages.success(request, msg)
            return capability
        except:
            exceptions.handle(request, _("Unable to update host capability."))
