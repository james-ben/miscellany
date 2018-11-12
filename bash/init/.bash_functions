# makes a directory and changes into it
mkcd () {
    mkdir $1
    cd $1
}

# highlight lines that match a pattern
# https://superuser.com/a/199106
function highlight()
{
    sed "s/$1/`tput smso`&`tput rmso`/g" "${2:--}"
}

# get all of the symbols in a binary file
# https://metricpanda.com/rival-fortress-update-22-finding-duplicate-static-symbols-in-shared-libraries
function getSymbols()
{
    nm $1 | c++filt | cut -d ' ' -f 3-99 | sort | uniq
}

# replace 4 spaces with tabs
function fix_tabs()
{
    sed -i 's/    /\t/g' $1
}

# cat the lines of a file, inclusive
function getLines()
{
    if [ $# -ne 3 ]; then
        echo "illegal number of parameters"
        echo "usage:"
        echo " $0 first_line last_line file_name"
        return 1
    fi
    sed -n "$1,$2p" $3
}
