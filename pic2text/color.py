"""使用 Linux 终端支持的颜色

-   http://www.tldp.org/HOWTO/Bash-Prompt-HOWTO/x329.html

颜色代码:

前景色: 30-37; 背景色 40-47.
颜色分别为 黑,红,绿,黄,蓝,紫,浅蓝,白

"""

# ASCII 27 -> \x1b -> \033

class Colorizer:
    """终端颜色序列

    一些颜色代码: F_ 前缀表示前景色, B_ 表示背景色

    BLACK, RED, GREEN, YELLOW, BLUE, PURPLE, LIGHTBLUE, WHITE

    X_ 表示效果:

    NULL 清空; BOLD 加粗; LIGHT 浅色; ITALIC 斜体;
    UNDERLINE 下划线; BLINK 闪烁; NEGA 负片; TRANSPARENT 透明;
    """

    # 一个被上色的块
    __TEMP = "\033[{code}m{content}\033[0m"

    # 前景色代码
    F_BLACK = 30
    F_RED = 31
    F_GREEN = 32
    F_YELLOW = 33
    F_BLUE = 34
    F_PURPLE = 35
    F_LIGHTBLUE = 36
    F_WHITE = 37

    # 背景色代码
    B_BLACK = 40
    B_RED = 41
    B_GREEN = 42
    B_YELLOW = 43
    B_BLUE = 44
    B_PURPLE = 45
    B_LIGHTBLUE = 46
    B_WHITE = 47

    # 效果代码

    X_NULL = 0                  # 清空
    X_BOLD = 1                  # 加粗
    X_LIGHT = 2                 # 浅色
    X_ITALIC = 3                # 斜体
    X_UNDERLINE = 4             # 下划线
    X_BLINK = 5                 # 闪烁
    X_NEGA = 7                  # 负片
    X_TRANSPARENT = 8           # 透明

    def colorize(self, string, *colors):
        """返回 content 的上色版本.

        colors 传入受支持的颜色代码.

        一个加粗效果, 黑色前景, 白色背景的文字:

        >>> x = Colorizer()
        >>> x.colorize("HelloWorld", x.X_BOLD, x.F_BLACK, x.B_WHITE)
        \033[1;30;47mHelloWorld\033[0m

        :param color: 色彩序列, 每一项用整数形式.
        :type color: list(int)
        """

        return self.__TEMP.format(
            code=";".join(map(lambda x: str(x), colors)), content=string
        )


def test_color_looking():
    """在终端打印所有的色彩序列组合, 观察效果
    """
    worker = Colorizer()

    for x in [0,1,2,3,4,5,6,7,8]:
        print("\n -- {}".format(x))
        print(r" B\F 30     31     32     33     34     35     36     37")
        for back in range(40, 48):
            print(" {} ".format(back), end="")
            for front in range(30, 38):
                print(worker.colorize(" Hello ", front, back, x), end="")
            print()

    print("\n 30     31     32     33     34     35     36     37")
    for i in range(0, 8):
        print(worker.colorize(" Hello ", 30 + i), end="")

    print("\n 40     41     42     43     44     45     46     47")
    for i in range(0, 8):
        print(worker.colorize(" Hello ", 40 + i, 8), end="")

    print("\n 0      1      2      3      4      5      6      7")
    for i in range(0, 8):
        print(worker.colorize(" Hello ", i), end="")

    print()
