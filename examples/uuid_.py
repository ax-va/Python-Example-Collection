"""
Create a UUID value and then return the hex string version of that value that is unique worldwide.

UUID = Universally Unique Identifier
"""
from uuid import uuid4
print(f"v_{uuid4().hex}")

# Run 1:
# v_7a98fc4acb994c92b4970d4dd4791314
# Run 2:
# v_84846547ef87447ab301fdb0db61b3ec
