# Pic2text

pic2text 是一个使用 Python 编写的将图片转化为字符画的工具.

# 安装

```
    $ git clone https://github.com/zombie110year/pic2text
    $ cd pic2text
    $ python setup.py install --user
```

# 使用

```
    $ pic2text pic.png -o text.txt
    # 将输出保存到文件
    $ pic2text pic.png
    # 输出至 stdout

    $ pic2text --help

    positional arguments:
    /path/to/picture.png

    optional arguments:
    -h, --help            show this help message and exit
    -o OUTPUT
    --width 120           每一行的字符数
    --wh 1.0              字体的宽高比
    --map 0123456789      从黑到白的灰度值到字符的映射
```

# License

MIT
