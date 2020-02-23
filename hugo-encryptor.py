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
                key = md5.hexdigest()
                cryptor = AESCrypt(key)
                text = ''.join(map(str, block.contents))
                written = base64.b64encode(cryptor.encrypt(text.encode('utf8')))

                del block['data-password']
                block.string = written.decode()

            if len(blocks):
                soup.body.append(soup.new_tag("script", src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.9-1/crypto-js.js"))
                script_tag = soup.new_tag("script");
                script_tag.string = """
const _do_decrypt = function(encrypted, password) {
  let key = CryptoJS.enc.Utf8.parse(password);
  let iv = CryptoJS.enc.Utf8.parse(password.substr(16));

  let decrypted_data = CryptoJS.AES.decrypt(encrypted, key, {
    iv: iv,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
  });
  return decrypted_data.toString(CryptoJS.enc.Utf8);
};

const _click_handler = function(element) {
  let parent = element.parentNode.parentNode;
  let encrypted = parent.querySelector(
    ".hugo-encryptor-cipher-text").innerText;
  let password = parent.querySelector(
    ".hugo-encryptor-input").value;
  password = CryptoJS.MD5(password).toString();

  let index = -1;
  let elements = document.querySelectorAll(
    ".hugo-encryptor-container");
  for (index = 0; index < elements.length; ++index) {
    if (elements[index].isSameNode(parent)) {
      break;
    }
  }

  let decrypted = "";
  try {
    decrypted = _do_decrypt(encrypted, password);
  } catch (err) {
    console.error(err);
    alert("Failed to decrypt.");
    return;
  }

  if (!decrypted.includes("--- DON'T MODIFY THIS LINE ---")) {
    alert("Incorrect password.");
    return;
  }

  let storage = localStorage;

  let key = location.pathname + ".password." + index;
  storage.setItem(key, password);
  parent.innerHTML = decrypted;
}

window.onload = () => {
  let index = -1;
  let elements = document.querySelectorAll(
    ".hugo-encryptor-container");

  while (1) {
    ++index;

    let key = location.pathname + ".password." + index;
    let password = localStorage.getItem(key);

    if (!password) {
      break;

    } else {
      console.log("Found password for part " + index);

      let parent = elements[index];
      let encrypted = parent.querySelector(".hugo-encryptor-cipher-text").innerText;
      let decrypted = _do_decrypt(encrypted, password);
      elements[index].innerHTML = decrypted;
    }
  }
};"""
                soup.body.append(script_tag)

            with open(fullpath, 'w') as f:
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

        with open(xmlpath, 'w') as f:
            f.write(str(soup))
