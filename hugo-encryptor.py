# coding=utf-8
import os
import base64

from bs4 import BeautifulSoup
from Crypto.Cipher import AES


class DESCrypt(object):
    LEN = 16
    def __init__(self, key: str):
        if len(key) > DESCrypt.LEN:
            raise ValueError('password too long')

        self.key = key.encode().ljust(DESCrypt.LEN, b'\x00')
        self.mode = AES.MODE_CBC

    def encrypt(self, text: bytes):
        cryptor = AES.new(self.key, self.mode, self.key)
        padlen = DESCrypt.LEN - len(text) % DESCrypt.LEN

        padlen = padlen if padlen != 0 else DESCrypt.LEN

        for i in range(padlen):
            text += chr(i+1).encode()

        return cryptor.encrypt(text)


if __name__ == '__main__':
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if not filename.lower().endswith('.html'):
                continue

            fullpath = os.path.join(dirpath, filename)

            soup = BeautifulSoup(open(fullpath), features="html5lib")
            block = soup.find('div', {'id': 'hugo-encryptor'})

            if block is None:
                pass

            else:
                print(fullpath)

                cryptor = DESCrypt(block['data-password'])
                text = ''.join(map(str, block.contents)).encode()
                written = base64.b64encode(cryptor.encrypt(text))

                del block['data-password']
                block.string = written.decode()

                with open(fullpath, 'w') as f:
                    f.write(str(soup))
