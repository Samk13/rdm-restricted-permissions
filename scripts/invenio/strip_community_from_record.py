# Strip out deleted community from a record, run:
# invenio shell scripts/strip_community_from_record.py <record-id>
import sys

from invenio_access.permissions import system_identity
from invenio_db import db
from invenio_rdm_records.proxies import current_rdm_records

try:
    RECORD_ID = sys.argv[1]
except IndexError:
    sys.exit("You need to specify a record ID as an argument")

# Get the record
try:
    record_item = current_rdm_records.records_service.read(system_identity, RECORD_ID)
except Exception:
    sys.exit(f"Failed to retrieve record with ID {RECORD_ID}")

record = record_item._record

# Get the community ID
try:
    community_id = record_item.to_dict()["parent"]["communities"]["default"]
except KeyError:
    sys.exit("This record has no communities.")

# Strip out community
record.parent.communities.remove(community_id)

# Commit changes
with db.session.begin_nested():
    record.parent.commit()
    record.commit()
db.session.commit()

# Reindex the record
current_rdm_records.records_service.indexer.index(record)
print(
    f"Community id:{community_id} has been stripped off from record id: {RECORD_ID} successfully!"
)
