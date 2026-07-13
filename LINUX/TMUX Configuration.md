# TMUX Configuration



```.tmux.conf
##### NDEEPAK #####
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'azorng/tmux-smooth-scroll'
set -g @plugin 'tmux-plugins/tmux-resurrect'   # sessions restoration
set -g @plugin 'tmux-plugins/tmux-continuum'   # sessions auto-save
set -g @plugin 'tmux-plugins/tmux-yank'        # copy to system clipboard

##### NDEEPAK #####
# Options to make tmux more pleasant
set -g mouse on
set -g default-terminal "tmux-256color"
set -g history-limit 100000

##### NDEEPAK #####
set -g base-index 1 # Indexing from 1
setw -g pane-base-index 1
set -g renumber-windows on

##### NDEEPAK #####
# Disable automatic window renaming
set -g allow-rename off
setw -g automatic-rename off

##### NDEEPAK #####
# Continuum config
# set -g @continuum-restore 'on'
# set -g @continuum-save-interval '10' # save every 10 seconds

##### NDEEPAK #####
run '~/.tmux/plugins/tpm/tpm'
```

- Run `tmux` then press `prefix/CTRL + B` + `I` (capital I)
If changed `.tmux.conf` file, open `tmux` then run:
```bash
$TMUX_PLUGIN_MANAGER_PATH/tpm/scripts/install_plugins.sh
```

