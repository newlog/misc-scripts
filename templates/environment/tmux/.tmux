set -g default-terminal "screen-256color"
set -g history-limit 10000

# Set status bar
set -g status-bg red
set -g status-fg black
set -g status-left '#[fg=black]#H'

# Highlight active window
#set-window-option -g window-status-current-bg colour27

# Set window notifications
setw -g monitor-activity on
set -g visual-activity on

# Automatically set window title
setw -g automatic-rename
#set -g terminal-overrides 'xterm*:smcup@:rmcup@'

# Info
#set -g status-right '#[fg=black]#(uptime | cut -d "," -f 2-)'

# use | and - to split the windows
bind-key | split-window -h
bind-key - split-window -v

# make the first window number start at 1
set -g base-index 1

# keybindings to make resizing esier
bind -r C-j resize-pane -L
bind -r C-k resize-pane -D
bind -r C-i resize-pane -U
bind -r C-l resize-pane -R
