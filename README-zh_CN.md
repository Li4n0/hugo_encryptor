# Hugo Encryptor

**Hugo-Encryptor** 是一款能够帮助作者保护文章内容的工具。它使用 AES-256 来对文章的内容进行加密，并且通过在文章中嵌入内联 `JavaScript` 代码来验证读者输入的密码是否正确。没有正确的文章密码，读者将无法看到文章的加密内容。

[English Document](./README.md) [效果演示](https://0n0.fun/post/2019/03/this-is-hugo-encryptor/)

## 安装

环境依赖：Python3

### 步骤一：下载 Hugo-Encryptor 并安装其所需要的依赖库

    $ git clone https://github.com/Li4n0/hugo_encryptor.git
    $ cd hugo_encryptor
    $ chmod +x hugo_encryptor.py
    $ pip install -r requirements.txt

### 步骤二：在博客根目录创建软链接(可选)

    $ mkdir -p /path/to/your/blog/layouts/shortcodes
    $ ln -s /absolute/path/to/hugo_encryptor/shortcodes/hugo-encryptor.html /path/to/your/blog/layouts/shortcodes/hugo-encryptor.html

### 步骤三：为 `shortcodes/hugo-encryptor.html` 创建软链接

    $ mkdir -p /path/to/your/blog/layouts/shortcodes
    $ ln -s /absolute/path/to/hugo_encryptor/shortcodes/hugo-encryptor.html /path/to/your/blog/layouts/shortcodes/hugo-encryptor.html


## 使用方法

### 步骤一：使用 `hugo-encryptor` 标签包裹你需要加密的内容

**注意：在 `hugo-encryptor` 标签之前必须存在一段明文文字以及 `<!--more-->`**

```markdown
---
title: "这是一篇加密文章"
---

**这里必须存在一些明文文字以及概要标签:**

<!--more-->

{{% hugo-encryptor "PASSWORD" %}}

# 这里是你要加密的内容!

这里是你要加密的内容!

**别忘了闭合 `hugo-encryptor` shortcode 标签:**

{{% /hugo-encryptor %}}
```

### 步骤二：像往常一样生成你的网站

    $ hugo

> 注意：在重新生成之前请先将你的 `public/` 删除，详见 [#15](https://github.com/Li4n0/hugo_encryptor/issues/15#issuecomment-826044272)。

### 步骤三：进行加密

    $ python /absolute/path/to/hugo_encryptor/hugo_encryptor.py


## 配置

虽然 **Hugo-Encryptor** 可以在没有经过任何配置的情况下正常运行，但是我们提供了一些设置，来帮助用户将 **Hugo-Encryptor**按照自己的喜好进行配置

### 语言

在默认情况下，**Hugo-Encryptor** 用中文作为提示信息的输出语言，通过在博客的配置文件添加`hugoEncryptorLanguage` 参数，你可以将它改变为英文输出，就像下面这样：

```toml
[params]
 		 ......
  hugoEncryptorLanguage = "en-us" # or "zh-cn"
```

### 样式

在默认情况下，**Hugo-Encryptor** 没有任何样式，但是我们为每一个可见元素都提供了类名，方便用户自己在 css 文件中为他们添加样式

## 注意：

- 切记一定要保证你所加密的文章的源代码是私密的。永远不要把你的博客目录发布到一个公开的仓库

- 每当你生成你的站点，你都应该再一次执行`$ python hugo-encryptor` 命令来加密你想保护的文章。如果你担心你会忘记这一点，选择使用一个 shell 脚本来代替 `$ hugo` 命令是一个不错的选择，就像下面这样：

  ```bash
  #!/bin/bash
  hugo
  python hugo-encryptor
  ```

  

