## Defining docker secrets.

- Create the following files inside this directory with the specified value in the table below.

|File | Data |
|-|-|
|**aes_key.txt** | The AES key to encrypt sensitive data |
|**ssl_crt.crt** | The public SSL/TLS certificate that will be used on services |
|**ssl_key.key** | The private SSL/TLS key that will be used on services |

> Create a self-signed certificate and key if you don't have a valid key-pair:

`openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ssl_key.key -out ssl_crt.crt`
