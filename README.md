# Hugo Encryptor

**Hugo-Encryptor** is a tool to protect your [Hugo](https://gohugo.io) posts. It uses AES-256 to encrypt the contents of your posts, and inserts a snippet of `<script>` code to verify whether the password is correct or not in readers' browser. Without a correct key, nobody can decrypt your private posts.

[中文文档](./README-zh_CN.md) [DEMO](https://0n0.fun/post/2019/03/this-is-hugo-encryptor/)


## Installation

Environmental dependence: Python3

### Step 1: Install all the requirements of Hugo-Encryptor

    $ git clone https://github.com/Li4n0/hugo_encryptor.git
    $ cd hugo_encryptor
    $ chmod +x hugo_encryptor.py
    $ pip install -r requirements.txt

### Step 2: Create a symlink (Optional)

    $ ln -s /absolute/path/to/hugo_encryptor/hugo_encryptor.py hugo_encryptor.py

### Step 3: Symlink `shortcodes/hugo-encryptor.html` into the shortcode directory of your blog:

    $ mkdir -p /path/to/your/blog/layouts/shortcodes
    $ ln -s /absolute/path/to/hugo_encryptor/shortcodes/hugo-encryptor.html /path/to/your/blog/layouts/shortcodes/hugo-encryptor.html


## Usage

### Step 1: Wrap the text you want to encrypt with the tag `hugo-encryptor`

**Notice: Some text are required before you actually start the encrypting part, with a tag `<!--more-->` placed in the middle of them. Example:**

```markdown
---
title: "An Encrypted Post"
---

Some text is required to be placed here.

<!--more-->

{{% hugo-encryptor "PASSWORD" %}}

# You cannot see me unless you've got the password!

This is the content you want to encrypt!

**Do remember to close the `hugo-encryptor` shortcodes tag:**

{{% /hugo-encryptor %}}
```


### Step 2: Generate your site as usual

It may be something like:

    $ hugo

> Notice: You may remove the `public/` directory before re-generate it, see [#15](https://github.com/Li4n0/hugo_encryptor/issues/15#issuecomment-826044272) for details.

### Step 3: Get the encryption done!

    $ python /absolute/path/to/hugo_encryptor/hugo_encryptor.py

Then all the private posts in your `public` directory would be encrypted thoroughly, congrats!


## Configuration

Though **Hugo-Encryptor** can run without any configurations, if you like, you can configure it (hmm.. slightly).

```toml
[params]
  hugoEncryptorLanguage = "zh-cn"     # within ["zh-cn", "zh-cn"]
```

### Style

**Hugo-Encryptor** has no any css but has left some class name for you to design your own style. Take a look at [shortcodes/hugo-encryptor.html](shortcodes/hugo-encryptor.html) ;-)


## Notice

* Do remember to keep the source code of your encrypted posts private. Never push your blog directory into a public repository.

* Every time when you generate your site, you should run `python hugo-encryptor` again to encrypt the posts which you want to be protected. If you are worried about you will forgot that, it's a good idea to use a shell script to take the place of  `hugo` ,such as below:

```bash
#!/bin/bash

hugo -D
python /absolute/path/to/hugo_encryptor/hugo_encryptor.py
rsync -a public remote@example.com:/
```
