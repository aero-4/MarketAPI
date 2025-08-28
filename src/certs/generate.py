from OpenSSL import crypto

key = crypto.PKey()
key.generate_key(crypto.TYPE_RSA, 2048)

private_pem = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)
with open("private.txt", "w") as f:
    f.write(str(private_pem))

public_pem = crypto.dump_publickey(crypto.FILETYPE_PEM, key)
with open("public.txt", "w") as f:
    f.write(str(public_pem))

