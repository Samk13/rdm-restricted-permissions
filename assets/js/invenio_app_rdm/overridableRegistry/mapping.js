// This file is part of InvenioRDM
// Copyright (C) 2023 CERN.
//
// Invenio App RDM is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

/**
 * Add here all the overridden components of your app.
 */

// This file is part of InvenioRDM
// Copyright (C) 2020-2022 CERN.
// Copyright (C) 2020-2022 Northwestern University.
// Copyright (C) 2021-2022 Graz University of Technology.
// Copyright (C) 2022-2023 KTH Royal Institute of Technology.
//
// Invenio App RDM is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

// This overrides is been updated to v12.0.0b2.dev35
// https://github.com/inveniosoftware/invenio-app-rdm/blob/v12.0.0b2.dev35/invenio_app_rdm/theme/assets/semantic-ui/js/invenio_app_rdm/deposit/RDMDepositForm.js
//
import { i18next } from "@translations/invenio_app_rdm/i18next";
import React from "react";
import { AccordionField, FieldLabel } from "react-invenio-forms";
import { FileUploader, CommunityHeader } from "@js/invenio_rdm_records";
import { Card, Container, Grid, Form, Divider } from "semantic-ui-react";
import PropTypes from "prop-types";

// Had issues with localization,this is another working approach...
const REQ_COMM_MSG = {
  en: i18next.t("Community is required in order to submit your data."),
  sv: "Community krävs för att skicka in din data.",
};
const getCurrentLocalReqCommMsg = (locale) =>
  REQ_COMM_MSG[locale] || REQ_COMM_MSG["en"];

export const CommunityHeaderOverride = ({
  record,
  permissions,
  filesLocked,
  noFiles,
  config,
}) => {
  const currentLocalReqCommMsg = getCurrentLocalReqCommMsg(config.current_locale);

  const hasCommunity = record?.parent?.review?.receiver?.community ?? false;

  return (
    <>
      <AccordionField active label={i18next.t("Community")}>
        <Grid>
          <Grid.Row className="pb-0">
            <Grid.Column>
              {!hasCommunity && (
                <>
                  <Form.Field required id="communityRequiredMessage">
                    <Card.Content>
                      <Card.Header>
                        <FieldLabel
                          className="ui grid visible info message header "
                          htmlFor="communityHeader"
                          label={currentLocalReqCommMsg}
                        />
                      </Card.Header>
                    </Card.Content>
                  </Form.Field>
                  <Divider horizontal />
                </>
              )}
              <Container className="ui grid page-subheader pb-5">
                <CommunityHeader
                  imagePlaceholderLink="/static/images/square-placeholder.png"
                  record={record}
                />
              </Container>
            </Grid.Column>
          </Grid.Row>
        </Grid>
      </AccordionField>
      <AccordionField
        includesPaths={["files.enabled"]}
        active
        label={i18next.t("Files")}
      >
        {noFiles && record.is_published && (
          <div className="text-align-center pb-10">
            <em>{i18next.t("The record has no files.")}</em>
          </div>
        )}
        <FileUploader
          isDraftRecord={!record.is_published}
          quota={config.quota}
          decimalSizeDisplay={config.decimal_size_display}
          showMetadataOnlyToggle={permissions?.can_manage_files}
          filesLocked={filesLocked}
        />
      </AccordionField>
    </>
  );
};

CommunityHeaderOverride.propTypes = {
  config: PropTypes.object.isRequired,
  record: PropTypes.object.isRequired,
  permissions: PropTypes.object,
  filesLocked: PropTypes.bool,
  noFiles: PropTypes.bool,
};

CommunityHeaderOverride.defaultProps = {
  permissions: null,
  filesLocked: false,
  noFiles: false,
};

export const overriddenComponents = {
  "InvenioAppRdm.Deposit.CommunityHeader.container": () => null,
  "InvenioAppRdm.Deposit.AccordionFieldFiles.container": CommunityHeaderOverride,
};
