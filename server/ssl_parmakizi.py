import hashlib

with open("server.crt", "rb") as f:
    cert = f.read()

fingerprint = hashlib.sha1(cert).hexdigest()
print(fingerprint)
