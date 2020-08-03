# Amazon Certificate Manager

## Import a certificate 

Paste the PEM-encoded certificate body

```
-----BEGIN CERTIFICATE-----
(your_domain_name.crt)
-----END CERTIFICATE-----

```


private key

```
-----BEGIN PRIVATE KEY-----
(your_private_key.key)
-----END PRIVATE KEY-----
```


and certificate chain (if your certificate is not self-signed)

```
-----BEGIN CERTIFICATE-----
(Your Primary SSL certificate: your_domain_name.crt)
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
(Your Intermediate certificate: DigiCertCA.crt)
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
(Your Root certificate: TrustedRoot.crt)
-----END CERTIFICATE-----
```

If the status is ``Issued``, then it is ready to use.

### Example Usage

Go to EC2 -> Load Balancing

Select a LB

Click ``Listeners``

Click Edit

Add HTTPS(Secure HTTP) and input the appropriate Instance Port

Select Certificate -> choose ``Choose a certificate from ACM (recommended)`` -> select Certificate

Remember to check if 443 port is allowed in Security Group