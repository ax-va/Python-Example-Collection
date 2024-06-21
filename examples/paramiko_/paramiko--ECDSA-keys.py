import os
import stat
from paramiko import ecdsakey

# ECDSA = Elliptic Curve Digital Signature Algorithm
pkey = ecdsakey.ECDSAKey.generate()
# PKey(alg=ECDSA, bits=256, fp=SHA256:WOlCts...4NvmJI)

public_key = pkey.get_base64()
# 'AAAAE2...xDSOyM='

with open("key.pub", "w") as f:
    f.write(public_key)

# the *minimum* to safely write a file
with open("key.priv", "w") as f:
    # Set the file mode to 0o600 before writing the sensitive bits to avoid race conditions.
    os.chmod("key.priv", 0o600)
    pkey.write_private_key(f)

# This gives read and write permissions to the owner,
# no permissions to non-owner group members,
# and no permissions for anyone else
oct(stat.S_IWRITE | stat.S_IREAD)
# '0o600'
