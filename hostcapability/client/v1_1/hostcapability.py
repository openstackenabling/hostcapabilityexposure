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

"""
Host Capability interface.
"""
import logging
from novaclient import base
from novaclient.v1_1 import base as local_base

LOG = logging.getLogger(__name__)

class HostCapability(base.Resource):
    NAME_ATTR = "id"

    def __repr__(self):
        return "<HostCapability: %s>" % self.id


class HostCapabilityManager(local_base.BootingManagerWithFind):
    resource_class = HostCapability

    def list(self, detailed=False):
        """
        Get a list of all host capabilities.

        :rtype: list of :class:`HostCapability`.
        """
        return self._list("/os-host-capability", "hostcapabilities")

    def get(self, capability):
        """
        Get a specific host capability.

        :param capability: The ID of the :class:`HostCapability` to get.
        :rtype: :class:`HostCapability`
        """
        return self._get("/os-host-capability/%s" % base.getid(capability), "hostcapability")

    def delete(self, capability):
        """
        Delete a specific capability.

        :param capability: The ID of the :class:`HostCapability` to get.
        :param purge: Whether to purge record from the database'
        """
        LOG.debug("delete the host capability using id: %s" % base.getid(capability))
        self._delete("/os-host-capability/%s" % base.getid(capability))

    def create(self, host, ip, rack, vtd_enabled_eth, has_node_manager):
        """
        Create (allocate) a  floating ip for a tenant

        :param host: The host name of the host
        :param ip: IP address of the host
        :param rack: The name of the rack this host in
        :param id: Integer ID for the host capability
        :param vtd_enabled_eth: Does it has VTD enabled eth installed
        :param has_node_manager: Does it has node manager installed
        :rtype: :class:`HostCapability`
        """
        body = {
            "hostcapability": {
                "host": host,
                "ip": ip,
                "rack": rack,
                "vtd_enabled_eth": bool(vtd_enabled_eth),
                "has_node_manager": bool(has_node_manager),
            }
        }
        return self._create("/os-host-capability", body, "hostcapability")
