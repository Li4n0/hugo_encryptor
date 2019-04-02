# coding=utf-8
import os
import base64
import hashlib

from bs4 import BeautifulSoup
from Crypto.Cipher import AES


class AESCrypt(object):
    LEN = 32
    def __init__(self, key: str):
        self.key = key.encode()
        self.mode = AES.MODE_CBC

    def encrypt(self, text: bytes):
        cryptor = AES.new(self.key, self.mode, self.key[16:])
        padlen = AESCrypt.LEN - len(text) % AESCrypt.LEN
        padlen = padlen if padlen != 0 else AESCrypt.LEN
        text += (chr(padlen)*padlen).encode('utf8')

        return cryptor.encrypt(text)


if __name__ == '__main__':
    for dirpath, dirnames, filenames in os.walk('./public'):
        for filename in filenames:
            if not filename.lower().endswith('.html'):
                continue

            fullpath = os.path.join(dirpath, filename)

            soup = BeautifulSoup(open(fullpath),'lxml')
            block = soup.find('cipher-text')

            if block is None:
                pass

            else:
                print(fullpath)
                md5 = hashlib.md5()
                md5.update(block['data-password'].encode('utf-8'))
                key = md5.hexdigest()
                cryptor = AESCrypt(key)
                text = ''.join(map(str, block.contents))
                written = base64.b64encode(cryptor.encrypt(text.encode('utf8')))

                del block['data-password']
                block.string = written.decode()

                with open(fullpath, 'w') as f:
                    f.write(str(soup))
