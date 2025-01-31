from Crypto.PublicKey import RSA

# Generate a new RSA key pair
key = RSA.generate(2048)

# Export the private key
private_key = key.export_key()
with open('private.pem', 'wb') as f:
    f.write(private_key)

# Export the public key
public_key = key.publickey().export_key()
with open('public.pem', 'wb') as f:
    f.write(public_key)
