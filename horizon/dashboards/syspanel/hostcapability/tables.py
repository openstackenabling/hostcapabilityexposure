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

from hostcapability.horizon.api import api as api
from horizon import tables

LOG = logging.getLogger(__name__)

class DeleteHostCapability(tables.DeleteAction):
    data_type_singular = _("Host Capability")
    data_type_plural = _("Host Capabilities")

    def delete(self, request, obj_id):
        api.host_capability_delete(request, obj_id)


class CreateHostCapability(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Host Capability")
    url = "horizon:syspanel:hostcapability:create"
    classes = ("ajax-modal", "btn-create")


class EditHostCapability(tables.LinkAction):
    name = "edit"
    verbose_name = _("Edit Host Capability")
    url = "horizon:syspanel:hostcapability:edit"
    classes = ("ajax-modal", "btn-edit")


class HostCapabilityTable(tables.DataTable):
    host = tables.Column('host', verbose_name=_('Host Name'))
    ip = tables.Column('ip', verbose_name=_('IP'))
    rack_name = tables.Column('rack', verbose_name=_('Rack'))
    vtd_enabled_eth = tables.Column('vtd_enabled_eth', verbose_name=_('VTD enabled eth'))
    has_node_manager = tables.Column('has_node_manager', verbose_name=_('Has node manager'))

    def get_object_display(self, obj):
        return obj.host

    def get_object_id(self, datum):
        return str(datum.id)

    class Meta:
        name = "hostcapability"
        verbose_name = _("hostcapability")
        table_actions = (CreateHostCapability, DeleteHostCapability)
        row_actions = (EditHostCapability, DeleteHostCapability)
