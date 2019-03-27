# Hugo Encryptor

**Hugo-Encryptor** is a tool to protect your [Hugo](https://gohugo.io) posts. It uses AES-128 to encrypt the contents of your posts, and inserts a snippet of `<script>` code to verify whether the password is correct or not in readers' browser. Without a correct key, nobody can decrypt your private posts.

## Installation

Step 1: Install all the requirements of Hugo-Encryptor.

    $ cd Hugo-Encryptor
    $ pip install -r requirements.txt

Step 2: Place `hugo-encryptor.py` somewhere in the directory of your blog.

    $ cp hugo-encryptor.py /path/to/your/blog/hugo-encryptor.py

Step 3: Install our Hugo shortcodes file into your blog:

    $ mkdir -p /path/to/your/blog/layouts/shortcodes
    $ cp shortcodes/hugo-encryptor.html /path/to/your/blog/layouts/shortcodes/hugo-encryptor.html

## Usage

A typical way to use Hugo-Encryptor has been already uploaded in [example_site](example_site).

**Step 1: Call our `hugo-encryptor` shortcodes if you want to encrypt a very post**

```markdown
---
title: This Is An Encrypted Post
---

{{% hugo-encryptor "PASSWORD" %}}

# You cannot see me unless you've got the password!

This is the content of my private post!

**Do remember to close the `hugo-encryptor` shortcodes tag:**

{{% /hugo-encryptor %}}
```

**Step 2: Generate your site as usual**

It may be something like:

    $ hugo

**Step 3: Get the encryption done!**

    $ python hugo-encryptor.py --path /path/to/your/blog/public

Then all the private posts in your `public` directory would be encrypted thoroughly, congrats!

## Attentions

* Do remember to keep the source code of your encrypted posts private. A typical way to deal with them is to ignore them by adding `content/posts/` in your `.gitignore` file.

