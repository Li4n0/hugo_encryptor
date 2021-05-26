const _do_decrypt = function (encrypted, password) {
    let md5 = forge.md5.create();
    let key = md5.update(password).digest();
    
    let parts = encrypted.split('||');
    let iv = forge.util.decode64(parts[0]);
    let mac = forge.util.decode64(parts[1]);
    let encoded_content = forge.util.decode64(parts[2]);

    let dec = forge.cipher.createDecipher('AES-GCM',key);
    dec.start({iv:iv, tag: mac});
    dec.update(forge.util.createBuffer(encoded_content));
    dec.finish();
    return forge.util.decodeUtf8(dec.output.data);
};

const _click_handler = function (element) {
    let parent = element.parentNode.parentNode;
    let encrypted = parent.querySelector(
        ".hugo-encryptor-cipher-text").innerText;
    let password = parent.querySelector(
        ".hugo-encryptor-input").value

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
};