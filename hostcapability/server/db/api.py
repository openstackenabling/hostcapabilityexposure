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

"""Defines interface for DB access.
"""
from hostcapability.server.db.sqlalchemy import api

def get_host_capability_by_id(context, id):
    """Get host capability by id"""
    return api.get_host_capability_by_id(context, id)


def host_capability_get_all(context, filters=None):
    """Get all the host capabilities"""
    return api.host_capability_get_all(context, filters=filters)


def host_capability_create(context, values):
    return api.host_capability_create(context, values)


def host_capability_update(context, host_capability_id, values):
    return api.host_capability_update(context, host_capability_id, values)


def host_capability_destroy(context, host_capability_id):
    return api.host_capability_destroy(context, host_capability_id)


