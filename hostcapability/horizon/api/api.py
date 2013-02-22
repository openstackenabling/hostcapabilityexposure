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

from __future__ import absolute_import

import logging
from django.conf import settings
from horizon.api.base import url_for
from hostcapability.client.v1_1.client import Client as host_capability_client

from horizon.utils.memoized import memoized

LOG = logging.getLogger(__name__)

def hostcapabilityclient(request):
    insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)
    LOG.debug('hostcapabilityclient connection created using token "%s" and url "%s"' %
              (request.user.token.id, url_for(request, 'compute')))
    c = host_capability_client(request.user.username,
        request.user.token.id,
        project_id=request.user.tenant_id,
        auth_url=url_for(request, 'compute'),
        insecure=insecure)
    c.client.auth_token = request.user.token.id
    c.client.management_url = url_for(request, 'compute')
    return c


def host_capability_create(request, host, ip, rack, vtd_enabled_eth, has_node_manager):
    LOG.debug("Create the host capability by "
              "id %s, host %s, ip %s,rack %s,vtd_enabled_eth %s,has_node_manager %s"
              % (id, host, ip, rack, vtd_enabled_eth, has_node_manager))
    return hostcapabilityclient(request).hostcapabilities.create(host, ip, rack, vtd_enabled_eth, has_node_manager)


def host_capability_delete(request, id):
    LOG.debug("Delete the host capability by id %s" % id)
    hostcapabilityclient(request).hostcapabilities.delete(id)


def host_capability_get(request, id):
    LOG.debug("Get the host capability by id %s" % id)
    return hostcapabilityclient(request).hostcapabilities.get(id)


@memoized
def host_capability_list(request):
    LOG.debug("List the host capability")
    return hostcapabilityclient(request).hostcapabilities.list()


