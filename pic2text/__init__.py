from argparse import Action, ArgumentParser, SUPPRESS
from pathlib import Path
from sys import exit

from .maker import TextDrawer


class SetFilePathAction(Action):
    def __call__(self, parser, namespace, values, option_string):
        values = str(Path(values).absolute())
        setattr(namespace, self.dest, values)


def _get_parser():
    parser = ArgumentParser(
        "pic2text", argument_default=SUPPRESS
    )
    parser.add_argument(
        "path", action=SetFilePathAction,
        metavar="/path/to/picture.png",
    )
    parser.add_argument(
        "-o", dest="output", action=SetFilePathAction,
        required=False, default=None
    )
    parser.add_argument(
        '--width', metavar="120", help="每一行的字符数",
        required=False, default=120, type=int
    )
    parser.add_argument(
        "--wh", metavar="1.0", help="字体的宽高比",
        required=False, default=1.0, type=float
    )
    parser.add_argument(
        "--map", dest="map_", metavar="0123456789", help="从黑到白的灰度值到字符的映射",
    )
    parser.add_argument(
        "--gamma", metavar="1.0", help="Gamma 矫正", type=float
    )
    return parser


def _parse_args(argv):
    args = _get_parser().parse_args(argv)
    return args


def main():
    args = _get_parser().parse_args()
    path = args.path
    drawer = TextDrawer(**args.__dict__)
    drawer.draw(path, args.gamma)
    if args.output:
        drawer.save(args.output)
    else:
        drawer.show()
    exit(0)
