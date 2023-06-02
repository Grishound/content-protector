# content-protector
A web app to store text. The content is stored in an encrypted format inside the database.
RSA encryption is used for encryption and decryption.

At the time of user registration, a public and a private key is generated. The public key is stored in the database whereas, the private key
is given to the user and the user is expected to store it somewhere safe.

The content is encrypted with the public key and stored in the database. When the user provides the private key after logging in, the content is decrypted using the
private key.

Live Link: https://content-protector.onrender.com
