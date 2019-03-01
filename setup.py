from setuptools import setup, find_packages

PROJ_NAME = "pic2text"
AUTHOR = "Zombie110year"
EMAIL = "zombie110year@outlook.com"

# * 项目主页
URL = "https://github.com/zombie110year/"

# * 版本号
VERSION = "1.0.0"

# * 短描述
DESCRIPTION = "将图片转换为字符串"

# * 长描述
with open("README.md", "rt", encoding="utf-8") as file:
    LONG_DESCRIPTION = file.read()

# * 协议
with open("LICENSE", "rt", encoding="utf-8") as file:
    LICENSE = file.read()

# * 包的分类
CLASSIFIERS = []

# * 搜索包的关键字
KEYWORDS = []

# * 包所支持的平台
PLATFORMS = [
    "win32",
    "linux",
]

# * entry_points 包的程序入口.

ENTRY = {
    'console_scripts': [
        "pic2text = pic2text:main"
    ],
}

# * 该程序的依赖项

REQUIRE = []

setup(
    name=PROJ_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    packages=['pic2text'],
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    platforms=PLATFORMS,
    entry_points=ENTRY,
    include_package_data=True,          # 添加包内资源文件
)
