"""Custom Registration form."""
# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 KTH Royal Institute of Technology Sweden
#
# invenio-config-kth is free software, you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file details.

from flask import current_app
from invenio_oauthclient.utils import create_registrationform
from invenio_userprofiles.forms import ProfileForm
from markupsafe import Markup
from werkzeug.local import LocalProxy
from wtforms import BooleanField, FormField, validators

# from flask import current_app, url_for

_security = LocalProxy(lambda: current_app.extensions["security"])


def kth_registration_form(*args, **kwargs):
    """KTH_registration_form."""
    # create a link to a PDF file containing the terms and conditions
    # the PDF file is located in the `static/documents` folder.
    # terms_of_use_url = url_for("static", filename=("documents/KTH-terms-of-use-en.pdf"))
    # terms_of_use_text = f"I confirm that I have read and fully understand the \
    # <a class='pull-right' href='{terms_of_use_url}' target='_blank'>terms and conditions</a>\
    # of KTH Royal Institute of Technology."

    # WARNING: This variable is populated with HTML content that is marked as safe using Markup.
    # It is assumed that only trusted admins have access to modify this variable.
    # Ensure that this assumption remains valid and that admin accounts are secure to mitigate the risk of XSS.
    # If this ever changes to accept user-controlled input, HTML sanitization will be necessary.
    # CWE-20,79,80
    terms_of_use_text = Markup(current_app.config["TERMS_OF_USE_TEXT"])
    current_remote_app = kwargs.get("oauth_remote_app")
    if not current_remote_app:
        # return default just in case something is wrong
        return create_registrationform(*args, **kwargs)
    # optionally, have different registration forms depending on the authentication
    # provider used by the user to login
    elif current_remote_app.name.lower() != "orcid":
        # show this form in case the user logged in with any method but ORCID
        class DefaultRegistrationForm(_security.confirm_register_form):
            """DefaultRegistrationForm."""

            # email = None  # remove the email field
            password = None  # remove the password field
            profile = FormField(ProfileForm, separator=".")
            recaptcha = None  # remove the captcha
            submit = None  # remove submit btn, already defined in the template
            terms_of_use = BooleanField(
                terms_of_use_text, [validators.required()]
            )  # add the new field

        return DefaultRegistrationForm(*args, **kwargs)
    else:
        # ORCID does not provide the user e-mail address, it must be input by the user.
        # the email field comes from `confirm_register_form` upper class.
        class OrcidRegistrationForm(_security.confirm_register_form):
            """OrcidRegistrationForm."""

            password = None  # remove the password field
            profile = FormField(ProfileForm, separator=".")
            recaptcha = None  # remove the captcha
            submit = None  # remove submit btn, already defined in the template
            terms_of_use = BooleanField(
                terms_of_use_text, [validators.required()]
            )  # add the new field

        return OrcidRegistrationForm(*args, **kwargs)
