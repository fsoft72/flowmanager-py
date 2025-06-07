#!/usr/bin/env python3
"""Generate self-signed SSL certificates using Python cryptography library"""

import os
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_ssl_certificates():
    print("Generating self-signed SSL certificates for localhost...")
    
    cert_dir = "certs/CA/localhost"
    os.makedirs(cert_dir, exist_ok=True)
    
    # Generate private key
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    
    # Generate certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "FlowManager"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(
        private_key.public_key()
    ).serial_number(x509.random_serial_number()).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(datetime.utcnow() + timedelta(days=365)).add_extension(
        x509.SubjectAlternativeName([x509.DNSName("localhost")]), critical=False
    ).sign(private_key, hashes.SHA256())
    
    # Write files
    key_path = os.path.join(cert_dir, "localhost.decrypted.key")
    with open(key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    cert_path = os.path.join(cert_dir, "localhost.crt")
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    os.chmod(key_path, 0o600)
    os.chmod(cert_path, 0o644)
    
    print("✅ SSL certificates generated successfully!")
    print(f"   Certificate: {cert_path}")
    print(f"   Private key: {key_path}")
    print("Now you can run: python run_production.py")

if __name__ == "__main__":
    try:
        generate_ssl_certificates()
    except Exception as e:
        print(f"❌ Error: {e}")
