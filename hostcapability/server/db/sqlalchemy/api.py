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

"""Implementation of SQLAlchemy backend."""

from nova.db.sqlalchemy.session import get_session
from nova.db.sqlalchemy.api import model_query
from nova.db.sqlalchemy.api import require_context
from nova.db.sqlalchemy.api import require_admin_context
from nova.openstack.common import log as logging
from nova.openstack.common import timeutils
from sqlalchemy.sql.expression import literal_column
from nova import exception
from hostcapability.server.compute.exception import HostCapabilityExistsForHost
from models import HostCapability

LOG = logging.getLogger(__name__)

def host_capability_get_all(context, filters=None):
    session = get_session()
    return model_query(context, HostCapability, session=session)


def get_host_capability_by_id(context, host_id):
    """Returns a dict describing specific host_id"""
    session = get_session()
    result = model_query(context, HostCapability, session=session).filter_by(id=host_id).first()

    if not result:
        raise exception.NotFound("No host capability found by id %s" % id)

    return result


def host_capability_create(context, values):
    session = get_session()
    with session.begin():
        host_capability_ref = HostCapability()
        try:
            host_capability_get_by_host(context, values['host'], session)
            # if the host already exists, then return an empty host object
            return host_capability_ref
        except exception.NotFound:
            pass

        values["deleted"] = False
        try:
            host_capability_ref.update(values)
            host_capability_ref.save(session=session)
        except Exception, e:
            raise exception.DBError(e)
        return host_capability_ref


@require_admin_context
def host_capability_update(context, host_capability_id, values):
    session = get_session()
    with session.begin():
        host_capability_ref = session.query(HostCapability).filter_by(id=host_capability_id)
        host_capability_ref.update(values)
        host_capability_ref.save(session=session)


@require_admin_context
def host_capability_destroy(context, host_capability_id):
    """Marks specific host as deleted"""
    session = get_session()
    with session.begin():
        session.query(HostCapability).\
        filter_by(id=host_capability_id).\
        update({'deleted': True,
                'deleted_at': timeutils.utcnow(),
                'updated_at': literal_column('updated_at')})


@require_context
def host_capability_get_by_host(context, host, session=None):
    """Returns a host capability describing specific host"""
    result = _host_capability_get_query(context, session=session).\
    filter_by(host=host).\
    first()

    if not result:
        raise exception.NotFound("No host capability found by host %s" % host)

    return result


def _host_capability_get_query(context, session=None, read_deleted=None):
    return model_query(context, HostCapability, session=session, read_deleted=read_deleted)