from pic2text import _parse_args, main
# import the entry of your program

a = ["tests/pic.png", "-o", "tests/text.txt",]
b = ["tests/pic.png", "-o", "tests/text.txt", "--width", "125"]
c = ["tests/pic.png", "-o", "tests/text.txt", "--wh", "0.8"]
d = ["tests/pic.png", "-o", "tests/text.txt", "--map", "!@#$%^&*()_+"]


if __name__ == "__main__":
    # args = _parse_args(d)
    # print(args)

    main()
