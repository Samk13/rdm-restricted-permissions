# Patches

- You can create a patch by simply adding `.patch` to the end of the PR and then saving it in the patch folder

```bash
curl https://patch-diff.githubusercontent.com/raw/inveniosoftware/invenio-rdm-records/pull/1303.patch > patches/your_patch.patch
```

- Then cd to where the site packages is located like: `~/.pyenv/versions/3.9.17/envs/kth-rdm/lib/python3.9/site-packages` and then apply:

```bash
cd ~/.pyenv/versions/3.9.17/envs/kth-rdm/lib/python3.9/site-packages
patch -p1 < ~/dev/kth-rdm/patches/add_to_fixtures.patch

# You can also use -i
patch -p1 -i /path/to/patch/location
```

To undo the patch:

```bash
patch -R -p1 < ~/dev/kth-rdm/patches/add_to_fixtures.patch
```

## add_to_fixture Patch

If you are setting up the instance from scratch, there is no need to install this one. Running `invenio-cli services setup -N` will include all fixtures, making this one relevant only for instances that are already running and need to add vocabularies to it (keep in mind that you can't remove from existing ones al least for now).

Once the associated feature is merged into the codebase, this patch should be removed. You can follow the progress [here](https://github.com/inveniosoftware/invenio-rdm-records/pull/1303).

add_to_fixture Patch: It introduces the command:

```bash
invenio rdm-records add_to_fixture resourcetypes
```

, which allows for the addition of fixtures on a live instance. Ensure that you have adhered to the instructions available [here](https://inveniordm.docs.cern.ch/customize/vocabularies/resource_types/#customize-the-resource-types).
