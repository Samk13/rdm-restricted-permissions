# kth-rdm-v12

Welcome to your InvenioRDM instance.

## Getting started

Run the following commands in order to start your new InvenioRDM instance:

```console
invenio-cli containers start --lock --build --setup
```

The above command first builds the application docker image and afterwards
starts the application and related services (database, Elasticsearch, Redis
and RabbitMQ). The build and boot process will take some time to complete,
especially the first time as docker images have to be downloaded during the
process.

Once running, visit <https://127.0.0.1> in your browser.

**Note**: The server is using a self-signed SSL certificate, so your browser
will issue a warning that you will have to by-pass.

## Development

> NOTE: When modifying environment variables in your local development setup, ensure to also update the .env file located in Azure's secure files library to prevent pipeline failures.

## Documentation

To learn how to configure, customize, deploy and much more, visit
the [InvenioRDM Documentation](https://inveniordm.docs.cern.ch/).

## Docker commands

```bash
docker-compose -f docker-compose.full.yml up
# start the instance

docker-compose -f docker-compose.full.yml exec web-api /bin/bash
# enter all admin commands like set admin users

docker-compose -f docker-compose.full.yaml ps
# show running containers


```

## Local development

Couple changes you need to make:

- In [docker-services.yml](docker-services.yml):

```yml
app:
  build:
    # comment out Pull from ACR so you can build from local
    context: ./ # local
    # context: ./docker/base/
```

- in your `.env` file, make sure that `DB_HOST=localhost` NOT `DB_HOST=db`.

## [Scripts docs](scripts/scripts.md)

follow the link above.

> Note that Demo data will not load, as our KTH permissions will prevent that as no record can be published without a community. so when you the instance lunch there will be no demo records.

## i18n in Containerized Environments

When deploying the containerized application, it's important to ensure that the localization files (.po and .pot) comment dev paths are removed.

### Steps to Update Localization Files

1. **Run the Script to Replace Paths**: Execute the `./scripts/replace_locale_paths.sh` script to update the paths in the `.po` and `.pot` files. This script takes two arguments: the pattern to replace and the new path. For example:

   ```bash
   ./scripts/replace_locale_paths.sh "/old/path" "/new/path"
   ```

   This will replace all instances of `/old/path` with `/new/path` in the localization files.

2. **Compile Translations**: After updating the paths, compile the translations so that they take effect. Run the following command:

   ```bash
   invenio-cli translations compile
   ```

## KTH Overrides

### Templates

- [`/invenio_accounts/register_user.html`](templates/semantic-ui/invenio_accounts/register_user.html) Add KTH terms of service to the register form
- [`/invenio_app_rdm/footer.html`](templates/semantic-ui/invenio_app_rdm/footer.html) Override App footer with KTH links
- [`/invenio_app_rdm/intro_section.html`](templates/semantic-ui/invenio_app_rdm/intro_section.html) Override App intro section
- [`invenio_communities/details/members/invitations.html`](templates/semantic-ui/invenio_communities/details/members/invitations.html) add Terms of use and specific responsibilities as a community manager
- [`/invenio_communities/details/settings/base.html`](templates/semantic-ui/invenio_communities/details/settings/base.html) Remove curation policy menu
- [`/invenio_theme/trackingcode.html`](templates/semantic-ui/invenio_theme/trackingcode.html) make trackingcode template available for future use.

## TODO

- [x] Update translation
- [x] Migrate kth theme content
- [x] Write permissions tests
- [x] Translate app_data/vocabularies/resource_types.yaml to sv
- [x] Review swedish translation for [funders](app_data/vocabularies/kth_funders.yaml)

### Before Deploy

- [ ] Keep this [template](templates/semantic-ui/invenio_communities/details/settings/base.html) up to date when upgrading dependencies current version: "invenio-communities==7.7.2"
- [ ] Activate email and logins functionalities
- [ ] Uncomment [affiliations](app_data/vocabularies.yaml) before deploy as it takes long time to index.
