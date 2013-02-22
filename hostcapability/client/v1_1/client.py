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

from novaclient.v1_1.client import Client as novaclient
from hostcapability import HostCapabilityManager

class Client(novaclient):
    def __init__(self, username, api_key, project_id, auth_url=None, insecure=False, timeout=None, proxy_tenant_id=None,
                 proxy_token=None, region_name=None, endpoint_type='publicURL', extensions=None, service_type='compute',
                 service_name=None, volume_service_name=None, timings=False, bypass_url=None, no_cache=False,
                 http_log_debug=False, auth_system='keystone'):
        super(Client, self).__init__(username, api_key, project_id, auth_url, insecure, timeout, proxy_tenant_id,
            proxy_token, region_name, endpoint_type, extensions, service_type, service_name, volume_service_name,
            timings, bypass_url, no_cache, http_log_debug, auth_system)
        self.hostcapabilities = HostCapabilityManager(self)