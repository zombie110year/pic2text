from copy import deepcopy

import numpy as np
from PIL import Image

from .color import Colorizer


class CharMap(tuple):
    """根据传入的 gamma 值查找元素.
    gamma: 0~1
    """

    def __getitem__(self, gamma):
        length = len(self)
        index = int(length * gamma)
        if index == length:
            index -= 1
        return super(CharMap, self).__getitem__(
            index
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
        '@#$%WMHGOBKwmghokb:|"^\'+~-__,.. '
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

    def rgb_to_grey(self, im: Image.Image) -> int:
        """将像素 RGB 转化为灰度值

        传入值的范围在 [0, 255] 之间

        :param im: PIL 读取的图像
        :return: 灰度值, 范围在 [0, 255] 之间
        :rtype: np.ndarray(shape=(im.height, im.width)) grey_array
        """
        # shape=(height, width, rgba)
        buffer = np.array(im, dtype=np.uint64)
        result = np.ndarray(shape=(im.height, im.width), dtype=np.uint64)
        result = (buffer[:, :, 0] * 38 + buffer[:, :, 1] * 75 + buffer[:, :, 2] * 15) >> 7
        return result

    def get_char(self, grey: np.ndarray, gamma: float, max_: int) -> str:
        """根据灰度值获取对应的字符

        字符映射表为 :data:`self.__MAP`

        :param int grey: [0, 255]
        :param float gamma: gamma 矫正的幂数
        :param float max_: 最大的灰度值
        """
        buffer = np.ndarray(shape=grey.shape, dtype=np.float64)
        buffer = (grey / max_)**gamma
        result = np.ndarray(shape=grey.shape, dtype=np.uint8)
        for y in range(grey.shape[0]):
            for x in range(grey.shape[1]):
                result[y, x] = ord(self.__MAP[buffer[y, x]])

        return result

    def image_to_text_array(self, im: Image.Image, gamma) -> list:
        """将彩色图片 ``im`` 转化为被字符填充的二维数组::

            [
                ['x', 'x', 'x', ...],
                ['x', 'x', 'x', ...],
                ...
                ['x', 'x', 'x', ...],
            ]

        :param im: 彩色图片
        :type im: PIL.Image.Image
        :param float gamma: 伽马矫正值
        :return: list(list(str()))
        """
        text_buffer = np.ndarray(shape=(im.height, im.width), dtype=np.uint8)
        buffer = self.rgb_to_grey(im)

        text_buffer = self.get_char(buffer, gamma, np.max(buffer))

        return text_buffer

    def image_to_color_array(self, im: Image.Image):
        color_buffer = [
            [
                '' for i in range(im.width)
            ] for j in range(im.height)
        ]

    def _get_text(self, buffer: np.ndarray):
        """将 uint8 二维数组转化为字符串
        """
        text = '\n'.join([
            ''.join([chr(item) for item in buffer[i]]) for i in range(buffer.shape[0])
        ])

        return text

    def draw(self, path, gamma):
        """将路径下的图片转为字符串返回

        :param str path: 指向图片文件的路径
        :param float gamma: 伽马矫正值 0~1: 亮, 1~infty 暗
        :return: 由图像转化而来的字符串
        """
        image = Image.open(path)
        # 缩放比例
        percentage = self.width / image.width

        height = int(self.wh * percentage * image.height)
        self.__height = height
        thumbnail = image.resize((self.width, height), Image.NEAREST)

        buffer = self.image_to_text_array(thumbnail, gamma)

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
