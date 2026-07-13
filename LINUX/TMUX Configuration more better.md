TMUX Configuration more better

```.tmux.conf
##### ========================================================
##### TMUX CONFIG — NDEEPAK NAGARKOTI
##### Clean • Productive • Dual Prefix • Commented
##### ========================================================


##### --------------------------------------------------------
##### 1. PREFIX KEYS (Ctrl-a AND Ctrl-b)
##### --------------------------------------------------------

# Default tmux prefix is Ctrl-b
# We keep it and ADD Ctrl-a (GNU Screen style)
set -g prefix C-b

# Bind Ctrl-a as an alternative prefix
bind C-a send-prefix

# Make Ctrl-a work as a proper prefix key
set -g prefix2 C-a


##### --------------------------------------------------------
##### 2. TPM — TMUX PLUGIN MANAGER
##### --------------------------------------------------------

# Core plugin manager
set -g @plugin 'tmux-plugins/tpm'

# Provides sensible defaults so we don't need to configure basics
set -g @plugin 'tmux-plugins/tmux-sensible'

# Smooth scrolling with mouse / trackpad
set -g @plugin 'azorng/tmux-smooth-scroll'

# Copy text from tmux directly to system clipboard
set -g @plugin 'tmux-plugins/tmux-yank'

# Restore tmux sessions after restart/reboot
set -g @plugin 'tmux-plugins/tmux-resurrect'

# Automatically save tmux sessions periodically
set -g @plugin 'tmux-plugins/tmux-continuum'


##### --------------------------------------------------------
##### 3. GENERAL OPTIONS (Quality of Life)
##### --------------------------------------------------------

# Enable mouse support (scrolling, resizing, selecting panes)
set -g mouse on

# Increase scrollback buffer size
set -g history-limit 100000

# Use true-color compatible terminal
set -g default-terminal "tmux-256color"

# Reduce delay after pressing ESC (important for Vim users)
set -sg escape-time 10


##### --------------------------------------------------------
##### 4. WINDOW & PANE INDEXING (Start from 1)
##### --------------------------------------------------------

# Windows start numbering from 1 instead of 0
set -g base-index 1

# Panes also start from 1
setw -g pane-base-index 1

# Automatically renumber windows when one closes
set -g renumber-windows on


##### --------------------------------------------------------
##### 5. WINDOW NAMING BEHAVIOR
##### --------------------------------------------------------

# Prevent tmux from renaming windows automatically
set -g allow-rename off
setw -g automatic-rename off


##### --------------------------------------------------------
##### 6. COPY MODE (Vim‑Style + System Clipboard)
##### --------------------------------------------------------

# Use Vim keybindings in copy mode
setw -g mode-keys vi

# Start selection with "v" (like Vim)
bind-key -T copy-mode-vi v send -X begin-selection

# Yank selection and exit copy mode with "y"
bind-key -T copy-mode-vi y send -X copy-selection-and-cancel


##### --------------------------------------------------------
##### 7. SPLIT PANES (Intuitive Keys)
##### --------------------------------------------------------

# Remove default awkward bindings
unbind '"'
unbind %

# Vertical split (|)
bind | split-window -h

# Horizontal split (-)
bind - split-window -v


##### --------------------------------------------------------
##### 8. PANE NAVIGATION (Vim Style)
##### --------------------------------------------------------

# Move between panes using h/j/k/l
bind -r h select-pane -L
bind -r j select-pane -D
bind -r k select-pane -U
bind -r l select-pane -R


##### --------------------------------------------------------
##### 9. RESIZE PANES (Shift + Vim Keys)
##### --------------------------------------------------------

# Resize panes in steps of 5 cells
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5


##### --------------------------------------------------------
##### 10. STATUS BAR & VISUAL POLISH
##### --------------------------------------------------------

# Update status bar every 5 seconds
set -g status-interval 5

# Length of left and right status sections
set -g status-left-length 30
set -g status-right-length 50

# Status bar colors
set -g status-style fg=white,bg=black

# Current window style
setw -g window-status-current-style fg=black,bg=green

# Inactive window style
setw -g window-status-style fg=white,bg=default

# Message (alerts/prompts) styling
set -g message-style fg=black,bg=yellow


##### --------------------------------------------------------
##### 11. SESSION PERSISTENCE (Continuum)
##### --------------------------------------------------------

# Automatically restore tmux sessions at startup
set -g @continuum-restore 'on'

# Auto-save sessions every 15 minutes
set -g @continuum-save-interval '15'


##### --------------------------------------------------------
##### 12. INITIALIZE TPM (KEEP THIS AT BOTTOM)
##### --------------------------------------------------------

# This must remain the last line in tmux.conf
run '~/.tmux/plugins/tpm/tpm'
```