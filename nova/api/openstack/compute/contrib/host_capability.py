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

"""Connect your vlan to the world."""

import webob
from nova.api.openstack import extensions
from nova.api.openstack import wsgi
from nova import exception
from nova import flags
from nova.api.openstack import common
from nova.openstack.common import log as logging
from hostcapability.server.compute import service as host_capability_service
from hostcapability.server.compute.exception import HostCapabilityExistsForHost

FLAGS = flags.FLAGS
LOG = logging.getLogger(__name__)
authorize = extensions.extension_authorizer('compute', 'hostcapability')

class ViewBuilder(common.ViewBuilder):
    _collection_name = "hostcapabilities"

    def basic(self, request, hostcapability):
        return {
            "hostcapability": {
                "id": hostcapability["id"],
                "host": hostcapability["host"],
                "ip": hostcapability["ip"],
                "rack": hostcapability["rack"],
                "vtd_enabled_eth": hostcapability["vtd_enabled_eth"],
                "has_node_manager": hostcapability["has_node_manager"],
                "updated_at": hostcapability["updated_at"],
                "deleted_at": hostcapability["deleted_at"],
                "deleted": hostcapability["deleted"],
            },
        }

    def show(self, request, hostcapability):
        dict = {
            "hostcapability": {
                "id": hostcapability["id"],
                "host": hostcapability["host"],
                "ip": hostcapability["ip"],
                "rack": hostcapability["rack"],
                "vtd_enabled_eth": hostcapability["vtd_enabled_eth"],
                "has_node_manager": hostcapability["has_node_manager"],
                "updated_at": hostcapability["updated_at"],
                "deleted_at": hostcapability["deleted_at"],
                "deleted": hostcapability["deleted"],
            },
        }

        return dict

    def index(self, request, hostcapability):
        """Return the 'index' view of hostcapability."""
        return self._list_view(self.basic, request, hostcapability)

    def detail(self, request, hostcapability):
        """Return the 'detail' view of hostcapability."""
        return self._list_view(self.show, request, hostcapability)


    def _list_view(self, func, request, hostcapabilities):
        """Provide a view for a list of hostcapability."""
        capability_list = [func(request, capability)["hostcapability"] for capability in hostcapabilities]
        capability_dict = dict(hostcapabilities=capability_list)
        return capability_dict


class HostCapabilityController(wsgi.Controller):
    """Handle creating and listing host capabilities."""

    _view_builder_class = ViewBuilder

    def index(self, req):
        """Return all host capability in brief."""
        host_capabilities = self._get_all_host_capabilities(req)
        result = self._view_builder.index(req, host_capabilities)
        return result

    def detail(self, req):
        """Return all host capability in detail."""
        host_capabilities = self._get_all_host_capabilities(req)
        result = self._view_builder.detail(req, host_capabilities)
        return result

    def delete(self, req, id):
        context = req.environ['nova.context']
        host_capability_service.host_capability_destroy(id, context)
        return webob.exc.HTTPNoContent()

    @wsgi.action("create")
    def _create(self, req, body):
        context = req.environ['nova.context']
        authorize(context)

        values = body['hostcapability']
        try:
            host_capability = host_capability_service.host_capability_create(values, context)
        except HostCapabilityExistsForHost as ex:
            return webob.exc.HTTPFound(detail=ex.message)

        return self._view_builder.show(req, host_capability)

    def show(self, req, id):
        """Return data about the given host id."""
        LOG.debug("Show host capability for %s" % id)
        try:
            capability = host_capability_service.get_host_capability_by_id(id)
        except exception.NotFound:
            raise webob.exc.HTTPNotFound()

        result = self._view_builder.show(req, capability)
        LOG.debug("result is: %s" % result)
        return result


    def _get_all_host_capabilities(self, req):
        """Helper function that returns a list of host capabilities dicts."""
        filters = {}
        context = req.environ['nova.context']

        host_capabilities = host_capability_service.host_capability_get_all(context, filters=filters)
        capability_list = host_capabilities.values()
        sorted_capabilities = sorted(capability_list, key=lambda item: item['host'])
        limited_capabilities = common.limited_by_marker(sorted_capabilities, req)
        return limited_capabilities


class Host_capability(extensions.ExtensionDescriptor):
    """Adds actions to create host capablility instances.  """
    name = "HostCapability"
    alias = "os-host-capability"
    namespace = "http://docs.openstack.org/compute/ext/hostcapability/api/v1.1"
    updated = "2012-12-24T00:00:00+00:00"

    def get_resources(self):
        resources = []
        res = extensions.ResourceExtension('os-host-capability', HostCapabilityController())
        resources.append(res)
        return resources
