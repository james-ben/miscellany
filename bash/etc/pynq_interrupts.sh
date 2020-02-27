# on the Pynq platform, highlights the number of interrupts counted on the user_intc line
cat /proc/interrupts | grep "user_intc" | awk ' {$2="\033[31m\033[7m"$2"\033[0m"; print $0 }'
# this is cool because it highlights only the 2nd column of the output
