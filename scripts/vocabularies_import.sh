#!/usr/bin/env sh
# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2023 KTH.


echo "Vocabularies Import: names  ..."
invenio vocabularies import -v names -f app_data/vocabularies-future.yaml
echo "Vocabularies Import: funders ..."
invenio vocabularies import -v funders -f app_data/vocabularies-future.yaml
echo "Vocabularies Import: awards ..."
# Uncomment on deploy, Takes long time to index 
# invenio vocabularies import -v awards -f app_data/vocabularies-future.yaml
echo "Done!"

