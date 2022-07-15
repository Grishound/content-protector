# content-protector
A web app to store text. The content is stored in an encrypted format inside the database.
RSA encryption is used for encryption and decryption.

The first time a user logs in after registering, a public and a private key is generated. The public key is stored in the database whereas, the private key
is given to the user and the user is expected to store it somewhere safe.

The content is encrypted with the public key and stored in the database. When the user provides the private key after logging in, the content is decrypted using the
private key.

This repository does not contain two things due to security reasons.

1) The database url.

2) A python file 'secret.py' which contains the values of n, p, q which are used during encryption and decryption.
