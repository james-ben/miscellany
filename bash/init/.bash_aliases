#################################
# pulled out of the .bashrc file
#################################

# some more ls aliases
# alias ll='ls -alF'
alias ll='ls -Alh'
alias la='ls -A'
alias l='ls -CF'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'


##############################
# added by me
##############################

# list all binaries in the PATH
alias path_bins='IFS=':';for i in $PATH; do test -d "$i" && find "$i" -maxdepth 1 -executable -type f -exec basename {} \;; done'

