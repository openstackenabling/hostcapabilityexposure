#!/usr/bin/env bash
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

set -o xtrace

TARGET_HOST=10.238.145.79
TOP_DIR='/usr/lib/python2.7/dist-packages'

scp -r hostcapability root@$TARGET_HOST:$TOP_DIR
scp -r locale root@$TARGET_HOST:$TOP_DIR
scp  nova/api/openstack/compute/contrib/host_capability.py root@$TARGET_HOST:$TOP_DIR/nova/api/openstack/compute/contrib/host_capability.py
scp -r horizon/dashboards/syspanel/hostcapability root@$TARGET_HOST:$TOP_DIR/horizon/dashboards/syspanel/
