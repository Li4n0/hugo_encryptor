# coding=utf-8
import os
import base64
import hashlib

from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def KEY_SIZE(): return 16
def NONCE_SIZE(): return 12
def MAC_SIZE(): return 16

# cipher: aes-128-gcm
# what is needed to share between encrypt and decrypt:
#- 16 bytes key, use md5 on plaintext to gen
#- 12 bytes nonce, randomly generate
#- 16 bytes mac(tag), generate by encryptor


class AESCrypt(object):
    def __init__(self, key: bytes, nonce: bytes):
        """

        create an aes-128-gcm object for encryption

        :param key: the key used for encryption
        :type key: 16 bytes
        :param nonce: also known as **IV** in other ciphers
        :type nonce: 12 bytes
        :return: a AESCrypt object with key, nonce and mode set
        :rtype: AESCrypt
        """
        if len(key) != KEY_SIZE():
            raise RuntimeError('key length must be 16 bytes')
        if len(nonce) != NONCE_SIZE():
            raise RuntimeError('nonce length must be 12 bytes')
        self.key = key
        self.mode = AES.MODE_GCM
        self.nonce = nonce

    def encrypt(self, text: bytes):
        """

        perform the encryption, MAC is set to 16 bytes

        :param text: text needed to encrypt
        :type text: bytes
        :return: encrypted text and mac
        :rtype: tuple[bytes,bytes]
        """
        cryptor = AES.new(self.key, self.mode, nonce=self.nonce, mac_len=MAC_SIZE())
        return cryptor.encrypt_and_digest(text)


def nonce_gen():
    """

    generate a random nonce for gcm encryption

    :return: 12 bytes nonce
    :rtype: bytes
    """
    return get_random_bytes(NONCE_SIZE())


if __name__ == '__main__':
    for dirpath, dirnames, filenames in os.walk('public'):
        for filename in filenames:
            if not filename.lower().endswith('.html'):
                continue

            fullpath = os.path.join(dirpath, filename)

            soup = BeautifulSoup(open(fullpath, 'rb'), 'lxml')
            blocks = soup.findAll(
                'div', {'class': 'hugo-encryptor-cipher-text'})

            if len(blocks):
                print(fullpath)

            for block in blocks:
                md5 = hashlib.md5()
                md5.update(block['data-password'].encode('utf-8'))
                key = md5.digest()
                nonce = nonce_gen()
                cryptor = AESCrypt(key, nonce)
                text = ''.join(map(str, block.contents))
                enc_text, enc_tag = cryptor.encrypt(text.encode('utf8'))
                # using || to seperate different part, because base64 has padding
                written = base64.b64encode(nonce) + b'||' + base64.b64encode(enc_tag) + b'||' + base64.b64encode(enc_text)

                del block['data-password']
                # bytes.decode, make it a string
                # has nothing to do with base64 or utf8
                block.string = written.decode()

            if len(blocks):
                soup.body.append(soup.new_tag("script", src="https://cdn.jsdelivr.net/npm/node-forge@0.7.0/dist/forge.min.js"))
                script_tag = soup.new_tag("script", src="/decrypt.js")
                
                soup.body.append(script_tag)

            with open(fullpath, 'w', encoding='utf-8') as f:
                html = str(soup)
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

                    if language.string == 'Part of this article is encrypted with password:':
                        prompt = BeautifulSoup('<p><i>Part of this article is encrypted with password, please goto the original webpage to check it out.</i></p>', 'html.parser')
                    
                    else:
                        prompt = BeautifulSoup('<p><i>以下内容被密码保护。请前往原网站查看。</i></p>','html.parser')
                    
                    block.replace_with(prompt)
                    description.string.replace_with(str(post))

        with open(xmlpath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
