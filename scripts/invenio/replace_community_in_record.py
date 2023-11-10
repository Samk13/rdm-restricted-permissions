# Strip out deleted community from a record, run:
# invenio shell scripts/strip_community_from_record.py <record-id>
import sys

from invenio_access.permissions import system_identity
from invenio_db import db
from invenio_rdm_records.proxies import current_rdm_records

try:
    RECORD_ID = sys.argv[1]
    NEW_COOMMUNITY_ID = sys.argv[2]
    # COMMUNITY_ID = "a5bdce3a-8945-44da-a802-1ece92eb469c"
except IndexError:
    sys.exit("You need to specify a RECORD_ID and COMMUNITY_ID as arguments")

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

# Add to new community
record.parent.communities.add(NEW_COOMMUNITY_ID, default=True)

# Commit changes
with db.session.begin_nested():
    record.parent.commit()
    record.commit()
db.session.commit()

# Reindex the record
current_rdm_records.records_service.indexer.index(record)
print(
    f"Community id:{community_id} has been replaced with {NEW_COOMMUNITY_ID} in record id: {RECORD_ID} successfully!"
)
