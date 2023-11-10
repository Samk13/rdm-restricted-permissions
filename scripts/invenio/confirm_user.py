# Use this script to confirm and reindex a user.

import sys

from click import secho
from flask import current_app
from flask_security.confirmable import confirm_user
from invenio_accounts.proxies import current_datastore
from invenio_db import db
from invenio_users_resources.services.users.tasks import reindex_users


def main(email):
    with current_app.app_context():
        user = current_datastore.get_user(email)
        if not user:
            secho(f"No user found with email {email}", fg="red", file=sys.stderr)
            sys.exit(1)

        confirm_user(user)
        db.session.commit()
        reindex_users([user.id])
        secho(f"User {email} confirmed and reindexed.", fg="green")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        secho("Usage: python confirm_user.py <email>", fg="red", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
