import base64
import hashlib
import secrets
import string
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken


class FernetHasher:
    # define os caracteres possíveis para a string gerada
    RANDOM_STRING_CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits

    # define o diretório base do projeto
    BASE_DIR = Path("../../../gerenciador-de-senhas")

    # define o diretório onde as chaves serão salvas
    KEY_DIR = BASE_DIR / "keys"

    def __init__(self, key):
        if not isinstance(key, bytes):  # chave deve estar em bytes
            key = key.encode()
        self.fernet = Fernet(key)

    @classmethod
    def get_random_string(cls, length=18):
        random_string = ""
        for i in range(length):
            random_string += secrets.choice(cls.RANDOM_STRING_CHARS)
        return random_string

    @classmethod
    def create_key(cls, archive=False):
        value = cls.get_random_string()
        hasher = hashlib.sha256(value.encode('utf-8')).digest()  # gera um hash SHA-256 da string.
        key = base64.b64encode(hasher)  # codifica o hash em Base64
        if archive:
            return key, cls.archive_key(key)
        return key, None

    @classmethod
    def archive_key(cls, key):  # salva a chave na pasta keys
        file = f'key_{cls.get_random_string(length=5)}.key'
        file_path = cls.KEY_DIR / file

        while Path(file_path).exists():  # se ja houver uma chave de mesmo nome:
            file = f'key_{cls.get_random_string(length=5)}.key'
            file_path = cls.KEY_DIR / file

        with open(file_path, "wb") as arq:
            arq.write(key)

        return cls.KEY_DIR / file  # retorna o diretorio onde a chave foi salva

    def encrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        return self.fernet.encrypt(value)

    def decrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        try:
            return self.fernet.decrypt(value).decode()
        except InvalidToken:
            return 'Token Inválido'
