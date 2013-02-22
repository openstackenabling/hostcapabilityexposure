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

from nova.openstack.common import log as logging
from nova import context
from hostcapability.server import db

LOG = logging.getLogger(__name__)

def get_host_capability_by_id(id, ctxt=None, read_deleted="yes"):
    """Retrieve host capability by id.

    :raises: NotFound
    """
    if ctxt is None:
        ctxt = context.get_admin_context(read_deleted=read_deleted)

    return db.get_host_capability_by_id(ctxt, id)


def host_capability_get_all(ctxt=None, filters=None):
    if ctxt is None:
        ctxt = context.get_admin_context()

    capabilities = db.host_capability_get_all(ctxt, filters=filters)

    capabilities_dict = {}
    for capability in capabilities:
        capabilities_dict[capability['host']] = capability
    return capabilities_dict


def host_capability_create(values, ctxt=None):
    if ctxt is None:
        ctxt = context.get_admin_context()

    return db.host_capability_create(ctxt, values)


def host_capability_update(host_capability_id, values, ctxt=None):
    if ctxt is None:
        ctxt = context.get_admin_context()

    return db.host_capability_update(ctxt, host_capability_id, values)


def host_capability_destroy( host_capability_id, ctxt=None):
    if ctxt is None:
        ctxt = context.get_admin_context()
    return db.host_capability_destroy(ctxt, host_capability_id)