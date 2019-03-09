from copy import deepcopy

from PIL import Image

from .color import Colorizer


class CharMap(tuple):
    """根据传入的索引值与 256 的相对大小查找元素的列表
    """

    def __getitem__(self, index):
        return super().__getitem__(
            (len(self) * index) >> 8
        )


class TextDrawer:
    """字符画画师!

    一般使用方法::

        from pic2text import TextDrawer

        drawer = TextDrawer(width=160, wh=0.6)
        # 设置 160 个字符宽, 字体矫正因子(宽高比) 为 0.6

        # 也可以使用 config 方法进行设置
        drawer.config(width=120, wh=1.0)

        drawer.draw("test.png")

        drawer.show()
        # 在 stdout 中打印

        drawer.save("test.txt")
        # 保存到文件当中


    .. data:: __MAP

        这是一个从灰度到字符的映射表, 见 :class:`CharMap`.

    .. data:: __WH

        使用字体的宽高比, __WH = width / height,
        用于修复因字体原因导致的图像变形.

    .. data:: __WIDTH

        字符画的宽度, 单位为字符.
        程序会保持原图的宽高比,
        如果要调整因字体导致的变形, 请设置 __WH
    """
    # 灰度-字符 正相关 0~1
    __MAP = CharMap(
        '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
    )
    # 宽高比的倒数, 修复因字体原因引起的变形
    __WH = 1.0

    # 缩略图宽度
    __WIDTH = 120

    # 缓存字符
    __cache = None

    @property
    def wh(self):
        """宽高比
        """
        return self.__WH

    @property
    def width(self):
        "查看当前所用的宽度"
        return self.__WIDTH

    def __init__(self, **kwargs):
        "见 :meth:`self.config`"
        self.config(**kwargs)
        self.__height = None

    def config(self, **kwargs):
        """设置

        可配置项:

        :attr:`self.__MAP`
            通过命名参数 ``map_`` 设置, 值必须是一个字符串
        :attr:`self.__WH`
            通过命名参数 ``wh`` 设置, 值应当为浮点数,
            输入当前所用字体的宽高比,
            将会自动转化为倒数形式在程序中使用.
        :attr:`self.__WIDTH`
            通过命名参数 ``width`` 设置, 值应当为整数,
            控制图像的宽度.
            程序会保持原图的缩放,
            如果要调整因字体导致的变形,
            请设置 ``self.__WH``
        """
        if 'map_' in kwargs:
            self.__MAP = CharMap(kwargs.get("map_", ""))
        if 'wh' in kwargs:
            self.__WH = kwargs.get("wh", 1.0)
        if 'width' in kwargs:
            self.__WIDTH = kwargs.get("width", 120)

    def rgb_to_grey(self, r: int, g: int, b: int, alpha=255) -> int:
        """将像素 RGB 转化为灰度值

        传入值的范围在 [0, 255] 之间

        :param int alpha: alpha 通道值, 默认为 255
        :return: 灰度值, 范围在 [0, 255] 之间
        :rtype: :class:`int`
        """
        if alpha == 0:
            return 0
        else:
            return (r*38 + g*75 + b*15) >> 7

    def get_char(self, grey: int) -> str:
        """根据灰度值获取对应的字符

        字符映射表为 :data:`self.__MAP`

        :param int grey: [0, 255]
        """
        return self.__MAP[grey]

    def image_to_text_array(self, im: Image.Image) -> list:
        """将彩色图片 ``im`` 转化为被字符填充的二维数组::

            [
                ['x', 'x', 'x', ...],
                ['x', 'x', 'x', ...],
                ...
                ['x', 'x', 'x', ...],
            ]

        :param im: 彩色图片
        :type im: PIL.Image.Image
        :return: list(list(str()))
        """
        text_buffer = [
            [
                ' ' for i in range(im.width)
            ] for j in range(im.height)
        ]
        for height in range(im.height):
            for width in range(im.width):
                grey = self.rgb_to_grey(*im.getpixel((width, height)))
                text_buffer[height][width] = self.get_char(grey)

        return text_buffer

    def image_to_color_array(self, im: Image.Image):
        color_buffer = [
            [
                '' for i in range(im.width)
            ] for j in range(im.height)
        ]

    def _get_text(self, buffer: list):
        """将字符二维数组转化为字符串
        """
        text = "\n".join([
            ''.join(buffer[i]) for i in range(self.__height)
        ])

        return text

    def draw(self, path, colorful=False):
        """将路径下的图片转为字符串返回

        :param str path: 指向图片文件的路径
        :return: 由图像转化而来的字符串
        """
        image = Image.open(path)
        # 缩放比例
        percentage = self.width / image.width

        height = int(self.wh * percentage * image.height)
        self.__height = height
        thumbnail = image.resize((self.width, height), Image.NEAREST)

        text_buffer = self.image_to_text_array(thumbnail)

        if colorful:
            pass
        else:
            buffer = text_buffer

        self.__cache = deepcopy(buffer)

        text = self._get_text(buffer)
        return text

    def show(self):
        """获取上次处理图片的字符画,
            打印在 stdout 上并返回
        """
        text = self._get_text(self.__cache)
        print(text)
        return text

    def save(self, path):
        """保存上次处理图片得到的字符画到文件 path
        """

        with open(path, "wt", encoding="utf-8") as file:
            file.write(
                self._get_text(self.__cache)
            )
