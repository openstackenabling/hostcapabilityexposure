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
SQLAlchemy models for host capability.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  DateTime, Boolean
from nova.db.sqlalchemy.models import NovaBase

BASE = declarative_base()

class HostCapability(BASE, NovaBase):
    """Represents host_ni on a host."""

    __tablename__ = 'host_capability'
    id = Column(Integer, primary_key=True)
    host = Column(String(255))
    ip = Column(String(255))
    rack = Column(String(255))
    vtd_enabled_eth = Column(Boolean, default=True)
    has_node_manager = Column(Boolean, default=True)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    created_at = Column(DateTime)
    deleted = Column(Boolean, default=True)
