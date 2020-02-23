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

            soup = BeautifulSoup(open(fullpath, 'rb'), 'lxml')
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

    for xmlpath in ['public/index.xml', 'public/rss.xml', 'public/feed.xml']:
        try:
            soup = BeautifulSoup(open(xmlpath, 'rb'), 'xml')
        except FileNotFoundError:
            continue

        print(xmlpath)

        descriptions = soup('description')

        for description in descriptions:

            if description.string is not None:
                post = BeautifulSoup(description.string,'html.parser')
                block = post.find('hugo-encryptor')

                if block is None:
                    pass

                else:      
                    language = block.find('p')

                    if language.string == 'The following content is password protected.':
                        prompt = BeautifulSoup('<p><i>The following content is password protected. Please view it on the original website.</i></p>','html.parser')
                    
                    else:
                        prompt = BeautifulSoup('<p><i>以下内容被密码保护。请前往原网站查看。</i></p>','html.parser')
                    
                    block.replace_with(prompt)
                    description.string.replace_with(str(post))

        with open(xmlpath, 'w') as f:
            f.write(str(soup))
