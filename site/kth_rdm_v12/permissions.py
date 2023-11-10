# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 KTH Royal Institute of Technology Sweden
#
# invenio-config-kth is free software, you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file details.

from flask import abort, current_app
from flask_principal import RoleNeed
from invenio_administration.generators import Administration
from invenio_communities.permissions import CommunityPermissionPolicy
from invenio_i18n import lazy_gettext as _
from invenio_rdm_records.services import RDMRecordPermissionPolicy
from invenio_rdm_records.services.errors import RecordCommunityMissing
from invenio_records_permissions.generators import (
    ConditionalGenerator,
    Disable,
    Generator,
    SystemProcess,
)


class CommunityManager(Generator):
    """Allows users with the "trusted-user" role."""

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        role_name = current_app.config.get(
            "CONFIG_KTH_COMMUNITY_MANAGER_ROLE", "community-manager"
        )
        return [RoleNeed(role_name)]


class IfInCommunity(ConditionalGenerator):
    """Conditional generator to check if the record is in a community."""

    def _condition(self, record, **kwargs):
        """Check if the record is part of a community."""
        if not record or not record.parent.communities.ids:
            abort(403, description=_("Please select a community before publishing."))
        return True


class IfOneCommunity(ConditionalGenerator):
    """Conditional generator to check if the record has at least one community."""

    def _condition(self, record, **kwargs):
        """Check if the record is part of a community."""
        if not record or len(record.parent.communities.ids) == 1:
            raise RecordCommunityMissing("", "One community per record is required")
        return True


class KTHCommunitiesPermissionPolicy(CommunityPermissionPolicy):
    """Communities permission policy of KTH.

    This will enable community managers and admins only to create communities.

    deprecating:  https://pypi.org/project/invenio-config-kth/ for versions <= V11.
    """

    can_create = [CommunityManager(), Administration(), SystemProcess()]

    can_include_directly = [Disable()]


class KTHRecordPermissionPolicy(RDMRecordPermissionPolicy):
    """Record permission policy of KTH.

    This will enable curators to publish records.
    Tested on: invenio-rdm-records==4.20.1
    """

    can_publish = [
        IfInCommunity(
            then_=RDMRecordPermissionPolicy.can_publish, else_=[SystemProcess()]
        )
    ]

    can_remove_community = [
        IfOneCommunity(
            then_=RDMRecordPermissionPolicy.can_remove_community,
            else_=[SystemProcess()],
        )
    ]
