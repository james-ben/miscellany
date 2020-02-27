import argparse


# global parameters
screen_width=80
tab_width=4


def getLine(text, style, indentVal):
    """Put text in the middle of a line.

    @param text - the text to center
    @param style - c or python
    @param indentVal - number of tabs to indent
    """

    text = " " + text + " "
    # are there indents?
    if indentVal:
        padding = tab_width*indentVal*2
        lineWidth = screen_width - padding
    else:
        lineWidth = screen_width
    # what filler char to use?
    if style == "python":
        formatStr = "{0:{c}^{n}}"
        fillChar = "#"
    elif style == "c":
        formatStr = "/{0:{c}^{n}}/"
        lineWidth -= 2
        if indentVal > 0:
            fillChar = "/"
        else:
            fillChar = "*"
    else:
        return "Invalid style!"
    # add the spaces
    temp_string = formatStr.format(text, c=fillChar, n=lineWidth)
    # then add the filler chars
    return "{0:{c}^{n}}".format(temp_string, c=' ', n=screen_width)


def parseArgs():
    parser = argparse.ArgumentParser(description="Make nice block comment header things")
    parser.add_argument('text', help='text to center')
    parser.add_argument('-i', '--indent', required=False, help='how many tabs indented less than the max screen width', nargs=1, type=int, metavar='n')
    # TODO: why use nargs?
    parser.add_argument('-p', '--python', help='create Python style comments instead of C', action='store_true')
    parser.add_argument('-w', '--width', type=int, help='set the screen width (default 80)')
    args = parser.parse_args()
    # TODO: explicit control over block style
    # TODO: other comment formats

    return args

def main():
    args = parseArgs()
    if args.width:
        global screen_width
        screen_width = args.width

    if args.indent:
        indentVal = args.indent[0]
    else:
        indentVal = 0
    text = args.text
    if args.python:
        style = "python"
    else:
        style = "c"

    line = getLine(text, style, indentVal)
    print(line.rstrip())
    print("")
    return

if __name__ == '__main__':
    main()
