import argparse

# these are pretty standard
screen_width=80
tab_width=4

# puts text in the center of a C block comment
def blockLine(text):
    text = " " + text + " "
    return "/{0:{c}^{n}}/".format(text, c='*', n=screen_width-2)

# puts text in the center of a C line comment ('/'), but indented
def midLine(text, indent_num):
    text = " " + text + " "
    # figure out how much white space to add
    padding = tab_width*indent_num*2
    block_width = screen_width - padding
    temp_string = "{0:{c}^{n}}".format(text, c='/', n=block_width)
    return "{0:{c}^{n}}".format(temp_string, c=' ', n=screen_width)

def main():
    parser = argparse.ArgumentParser(description="Make nice block comment header things")
    parser.add_argument('text', help='text to center')
    parser.add_argument('-i', '--indent', required=False, help='how many tabs indented less than the max screen width', nargs=1, type=int, metavar='n')
    args = parser.parse_args()
    if args.indent:
        print(midLine(args.text, args.indent[0]))
    else:
        print(blockLine(args.text))

    print("")
    return

if __name__ == '__main__':
    main()
