# example of how to import module from subdirectory

import mymodule.resources as resources


def main():
    g1 = resources.greeting()
    g2 = resources.salutation()
    r1 = resources.response(g1)
    r2 = resources.response(g2)

    print(g1)
    print(r1)
    print(g2)
    print(r2)


if __name__ == '__main__':
    main()
