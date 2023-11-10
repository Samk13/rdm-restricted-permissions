#!/usr/bin/env sh
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 CERN.
#
# Demo-InvenioRDM is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

# Prompt to confirm action
# read -r -p "Are you sure you want to wipe everything and create a new empty instance? [y/N] " response
# if [[ ! ("$response" =~ ^([yY][eE][sS]|[yY])$) ]]
# then
#     exit 0
# fi

# Wipe
# ----
invenio shell --no-term-title -c "import redis; redis.StrictRedis.from_url(app.config['CACHE_REDIS_URL']).flushall(); print('Cache cleared')"
# NOTE: db destroy is not needed since DB keeps being created
#       Just need to drop all tables from it.
invenio db drop --yes-i-know
invenio index destroy --force --yes-i-know
invenio index queue init purge

# Recreate
# --------
# NOTE: db init is not needed since DB keeps being created
#       Just need to create all tables from it.
echo "Create DB ..."
invenio db create
echo "Set default file location ..."
invenio files location create --default 'default-location' $(invenio shell --no-term-title -c "print(app.instance_path)")'/data'
invenio roles create admin
invenio access allow superuser-access role admin
echo "Initate indecies ..."
invenio index init --force
echo "Initate custome feilds ..."
invenio rdm-records custom-fields init
echo "Initate communities custome feilds ..."
invenio communities custom-fields init

# Static page create
echo "Initate static pages ..."
invenio rdm pages create --force

# Add demo and fixtures data
# -------------

echo "Initate fixtures ..."
invenio rdm-records fixtures

# echo "Initate demo records ..."
# invenio rdm-records demo
# TODO uncomment on prod
# Import awards vocabulary
# invenio vocabularies import --vocabulary awards --origin "app_data/vocabularies/awards_sample.tar"

# Enable admin user
# echo "activate admin user ..."
# invenio users activate admin@inveniosoftware.org


# invenio shell --no-term-title -c "import redis; redis.StrictRedis.from_url(app.config['CACHE_REDIS_URL']).flushall(); print('Cache cleared')"
# NOTE: db destroy is not needed since DB keeps being created
#       Just need to drop all tables from it.
# invenio db drop --yes-i-know
# invenio index destroy --force --yes-i-know
# invenio index queue init purge

# # Recreate
# # --------
# # NOTE: db init is not needed since DB keeps being created
# #       Just need to create all tables from it.
# invenio db create
# # add back when pipenv access problem is fixed
# invenio files location create --default 'default-location'  $(pipenv run invenio shell --no-term-title -c "print(app.instance_path)")'/data'
# # invenio files location create --default 'default-location' /opt/invenio/var/instance/data           
# invenio alembic upgrade
# invenio queues declare
# invenio roles create admin
# invenio access allow superuser-access role admin
# invenio index init --force
# invenio rdm pages create --force

# # Add demo and fixtures data
# # -------------
# invenio rdm-records fixtures
# invenio rdm-records demo

# Enable admin user
# invenio users activate admin@test.se
