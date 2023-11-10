# KTH SSO Authentication
# Authentication - Invenio-Accounts and Invenio-OAuthclient
# See: https://inveniordm.docs.cern.ch/customize/authentication/
# ==============================================================

import jwt
from flask import abort, current_app, flash, redirect, url_for
from flask_login import current_user
from invenio_db import db
from invenio_i18n import lazy_gettext as _
from invenio_oauthclient import (
    current_oauthclient,
    oauth_link_external_id,
    oauth_unlink_external_id,
)
from invenio_oauthclient.contrib.settings import OAuthSettingsHelper
from invenio_oauthclient.handlers.rest import response_handler
from invenio_oauthclient.handlers.utils import require_more_than_one_external_account
from invenio_oauthclient.models import RemoteAccount


class AzureOAuthSettingsHelper(OAuthSettingsHelper):
    """Default configuration for Azure OAuth provider."""

    # import pdb;pdb.pdb.set_trace()
    def __init__(
        self,
        title=None,
        description=None,
        base_url=None,
        request_token_params=None,
        app_key=None,
        access_token_url=None,
        authorize_url=None,
        precedence_mask=None,
        signup_options=None,
    ):
        """Constructor."""
        base_url = "https://login.ug.kth.se/adfs"
        access_token_url = "https://login.ug.kth.se/adfs/oauth2/token/"
        authorize_url = "https://login.ug.kth.se/adfs/oauth2/authorize/"
        signup_options = {"auto_confirm": True, "send_register_msg": False}
        request_token_params = {
            "scope": "openid email profile"
        }  # https://learn.microsoft.com/en-us/azure/active-directory/develop/scopes-oidc"
        content_type = "application/json"
        super().__init__(
            title=title or "KTH SSO",
            description=description or "Microsoft Outlook",
            base_url=base_url,
            request_token_params=request_token_params,
            app_key=app_key or "AZURE_APP_CREDENTIALS",
            access_token_url=access_token_url,
            precedence_mask=precedence_mask,
            content_type=content_type,
            signup_options=signup_options,
            authorize_url=authorize_url,
        )
        self._handlers = dict(
            authorized_handler="invenio_oauthclient.handlers"
            ":authorized_signup_handler",
            disconnect_handler=azure_disconnect_handler,
            signup_handler=dict(
                info_serializer=azure_account_info_serializer,
                info=azure_account_info,
                setup=azure_account_setup,
                view="invenio_oauthclient.handlers:signup_handler",
            ),
        )

        self._rest_handlers = dict(
            authorized_handler="invenio_oauthclient.handlers.rest"
            ":authorized_signup_handler",
            disconnect_handler=disconnect_rest_handler,
            signup_handler=dict(
                info=azure_account_info,
                setup=azure_account_setup,
                view="invenio_oauthclient.handlers.rest:signup_handler",
            ),
            response_handler="invenio_oauthclient.handlers.rest"
            ":default_remote_response_handler",
            authorized_redirect_url="/",
            disconnect_redirect_url="/",
            signup_redirect_url="/",
            error_redirect_url="/",
        )

    def get_handlers(self):
        """Return Azure auth handlers."""
        return self._handlers

    def get_rest_handlers(self):
        """Return Azure auth REST handlers."""
        return self._rest_handlers


@require_more_than_one_external_account
def _disconnect(remote, *args, **kwargs):
    """Handle unlinking of remote account.

    :param remote: The remote application.
    """
    # import pdb;pdb.pdb.set_trace()
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()

    account = RemoteAccount.get(
        user_id=current_user.get_id(), client_id=remote.consumer_key
    )
    user_external_id = account.extra_data.get("external_id")

    if user_external_id:
        oauth_unlink_external_id({"method": "azure", "id": user_external_id})
    if account:
        # pylint: disable=no-member
        with db.session.begin_nested():
            account.delete()


def azure_disconnect_handler(remote, *args, **kwargs):
    """Handle unlinking of remote account.

    :param remote: The remote application.
    """
    _disconnect(remote, *args, **kwargs)
    return redirect(url_for("invenio_oauthclient_settings.index"))


def disconnect_rest_handler(remote, *args, **kwargs):
    """Handle unlinking of remote account.

    :param remote: The remote application.
    """
    _disconnect(remote, *args, **kwargs)
    redirect_url = current_app.config["OAUTHCLIENT_REST_REMOTE_APPS"][remote.name][
        "disconnect_redirect_url"
    ]
    return response_handler(remote, redirect_url)


def azure_account_info_serializer(remote, resp, **kwargs):
    """Serialize the account info response object.

    :param remote: The remote application.
    :param resp: The response of the `authorized` endpoint.
    :returns: A dictionary with serialized user information.
    """
    try:
        graph_data = extract_user_info(resp["access_token"])
        external_id = str(graph_data.get("kthid"))
        email = str(graph_data.get("email")).lower()
        username = f"{graph_data.get('username')}"
        full_name = str(graph_data.get("unique_name")[0])
        external_method = str(remote.name)
        affiliation = str(graph_data.get("affiliation")[0])
        return dict(
            user=dict(
                email=email,
                profile=dict(username=username, full_name=full_name),
            ),
            external_id=external_id,
            external_method=external_method,
            affiliations=affiliation,
            active=True,
        )
    except AttributeError:
        current_app.logger.warning(
            "Something went wrong while authenticating you!", exc_info=True
        )
        flash(_("Unable to serialize auth response!"), category="danger")
        abort(401)


def extract_user_info(token):
    """Fetch Microsoft Graph data for current user."""
    jwt_decode_params = dict(
        options=dict(
            verify_signature=False,
            verify_aud=False,
        ),
        algorithms=[
            "HS256",
            "HS384",
            "HS512",
            "RS256",
            "RS384",
            "RS512",
            "ES256",
            "ES384",
            "ES512",
            "PS256",
            "PS384",
            "PS512",
        ],
    )
    if not token:
        current_app.logger.warning("Token is empty or None", exc_info=True)
        flash(_("Token is empty or None"), category="danger")
        abort(401)
    try:
        graph_data = jwt.decode(token, **jwt_decode_params)
        return graph_data
    except jwt.InvalidTokenError:
        current_app.logger.warning("Invalid token", exc_info=True)
        flash(_("Invalid token"), category="danger")
        abort(401)


def azure_account_info(remote, resp):
    """Retrieve remote account information used to find local user."""
    handlers = current_oauthclient.signup_handlers[remote.name]
    if "access_token" in resp:
        return handlers["info_serializer"](resp)


def azure_account_setup(remote, token, resp):
    """Perform additional setup after user have been logged in."""
    # pylint: disable=no-member
    with db.session.begin_nested():
        graph_data = extract_user_info(token.access_token)
        user = token.remote_account.user
        external_id = str(graph_data.get("kthid"))
        token.remote_account.extra_data = {
            "external_id": external_id,
        }
        oauth_link_external_id(user, dict(id=external_id, method="azure"))
