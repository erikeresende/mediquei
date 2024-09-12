from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import base64
from PIL import Image
from django.core.files.base import ContentFile
import logging
from io import BytesIO  # Correção da falta de importação

def sign_data(data, private_key_path):
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )

    signature = private_key.sign(
        data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature

def verify_signature(data, signature, public_key_path):
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )

    try:
        public_key.verify(
            signature,
            data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        return False
    
def processar_assinatura_digital(assinatura_digital, receita):
    try:
        header, encoded = assinatura_digital.split(',', 1)
        formato = header.split(';')[0].split('/')[1]
        file_data = base64.b64decode(encoded)

        if formato.lower() != 'png':
            return False, "A assinatura deve ser em formato PNG."

        image = Image.open(BytesIO(file_data))
        file_name = f"assinatura.{formato}"

        file_io = BytesIO()
        image.save(file_io, format='PNG')
        file_content = ContentFile(file_io.getvalue(), file_name)

        receita.assinatura_digital.save(file_name, file_content, save=False)
        return True, ""
    except Exception as e:
        return False, str(e)
