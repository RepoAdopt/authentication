import os

from jwcrypto import jwk


pub_file = 'public_key.pem'
priv_file = 'private_key.pem'

key = jwk.JWK(generate='RSA', size=2048)

pub_key = key.export_to_pem(private_key=False, password=None)
priv_key = key.export_to_pem(private_key=True, password=None)


def overwrite_file(file_name, content):
    if os.path.exists(file_name):
        os.remove(file_name)

    print(content)

    file = open(file_name, 'wb')
    file.write(content)
    file.close()


overwrite_file(pub_file, pub_key)
overwrite_file(priv_file, priv_key)
