# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
# Copyright (C) 2021 TU Wien.
# Copyright (C) 2023 KTH.
#
# Invenio-RDM-Records is free software; you can redistribute it
# and/or modify it under the terms of the MIT License; see LICENSE file for
# more details.

"""Permissions for Invenio RDM Records."""
"""Tests KTH permissions overrides."""
import pdb

import pytest
from flask_principal import UserNeed
from invenio_access.permissions import (
    any_user,
    authenticated_user,
    system_identity,
    system_process,
)
from invenio_drafts_resources.services.records.permissions import RecordPermissionPolicy
from invenio_rdm_records.records import RDMParent, RDMRecord
from invenio_rdm_records.services.generators import IfRestricted, RecordOwners
from invenio_records_permissions.generators import (
    AnyUser,
    AuthenticatedUser,
    Disable,
    SystemProcess,
)
from kth_rdm_v12.permissions import KTHRecordPermissionPolicy
from werkzeug.exceptions import Forbidden

from .conftest import kth_record_permission_policy_active


class TestRDMPermissionPolicy(RecordPermissionPolicy):
    """Define permission policies for RDM Records."""


def test_permission_policy_generators(
    app, anyuser_identity, authenticated_identity, superuser_identity
):
    """Test permission policies with given Identities."""
    policy = KTHRecordPermissionPolicy

    rest_record = RDMRecord.create({}, access={}, parent=RDMParent.create({}))
    rest_record.access.protection.set("restricted", "restricted")
    rest_record.parent.access.owner = {"user": 1}

    pub_record = RDMRecord.create({}, access={}, parent=RDMParent.create({}))
    pub_record.access.protection.set("public", "public")
    pub_record.parent.access.owner = {"user": 21}

    assert policy(action="search").allows(anyuser_identity)
    assert policy(action="search").allows(system_identity)
    assert policy(action="create").allows(authenticated_identity)
    assert policy(action="create").allows(system_identity)
    assert isinstance(policy(action="update").generators[0], Disable)
    assert isinstance(policy(action="delete").generators[0], SystemProcess)
    assert policy(action="read").generators[0].needs(record=rest_record) == {
        UserNeed(1),
        system_process,
    }
    assert policy(action="read").generators[0].needs(record=pub_record) == {
        system_process,
        any_user,
    }
    assert policy(action="read_files").generators[0].needs(record=rest_record) == {
        UserNeed(1),
        system_process,
    }
    assert isinstance(policy(action="update_files").generators[0], Disable)
    assert policy(action="read_draft").generators[0].needs(record=rest_record) == [
        UserNeed(1)
    ]
    assert policy(action="update_draft").generators[0].needs(record=rest_record) == [
        UserNeed(1)
    ]
    assert policy(action="delete_draft").generators[0].needs(record=rest_record) == [
        UserNeed(1)
    ]
    # Should be empty here rather then UserNeed(1)
    assert (
        policy(action="read_draft_files").generators[0].needs(record=rest_record) == []
    )
    assert (
        policy(action="read_update_files").generators[0].needs(record=rest_record) == []
    )
    assert policy(action="manage").generators[0].needs(record=rest_record) == [
        UserNeed(1)
    ]

    with pytest.raises(Exception) as e_info:
        policy(action="publish").generators[0].needs(record=rest_record)

    assert e_info.value.code == 403
    assert (
        str(e_info.value)
        == "403 Forbidden: Please select a community before publishing."
    )

    with pytest.raises(Exception) as e:
        policy(action="remove_community").needs(record=rest_record)

    assert e.typename == "RecordCommunityMissing"
    assert (
        str(e.value.description)
        == "The record  in not included in the community One community per record is required."
    )


def test_permission_policy_needs_excludes(superuser_role_need):
    """Test permission policy excluding 'superuser_role_need'."""
    search_perm = KTHRecordPermissionPolicy(action="search")
    create_perm = KTHRecordPermissionPolicy(action="create")
    update_perm = KTHRecordPermissionPolicy(action="update")
    delete_perm = KTHRecordPermissionPolicy(action="delete")
    updates_files_perm = KTHRecordPermissionPolicy(action="updates_files")

    assert search_perm.needs == {superuser_role_need, any_user, system_process}
    assert search_perm.excludes == set()

    assert create_perm.needs == {
        superuser_role_need,
        authenticated_user,
        system_process,
    }
    assert create_perm.excludes == set()

    assert update_perm.needs == {superuser_role_need}
    assert update_perm.excludes == {any_user}

    assert delete_perm.needs == {superuser_role_need, system_process}
    assert delete_perm.excludes == set()

    assert updates_files_perm.needs == {superuser_role_need}
    assert updates_files_perm.excludes == {any_user}


def test_record_creation_without_community(
    app, record_community, uploader, curator, community_owner, test_user, superuser
):
    # Default permissions will allow record creation
    rec = record_community.create_record()
    assert rec.id
    # test against different user roles
    users = [curator, test_user, uploader, community_owner, superuser]

    with kth_record_permission_policy_active(app):
        with pytest.raises(Forbidden):
            for user in users:
                record_community.create_record(uploader=user)
