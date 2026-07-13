


```conf

set -g @plugin 'tmux-plugins/tmux-cpu'
set -g status-right "#[fg=cyan]#H | CPU: #{cpu_percentage} | RAM: #{ram_percentage} | Load: #{loadavg} | %Y-%m-%d %H:%M"

# Pentest Workspace (Multi-window)
bind-key p run-shell "
tmux new-session -d -s pentest \; \
rename-window -t pentest:1 'recon' \; \

# Recon window (3 panes)
split-window -h -t pentest:1 -c '#{pane_current_path}' \; \
split-window -v -t pentest:1.0 -c '#{pane_current_path}' \; \

# Run tools
send-keys -t pentest:1.0 \"clear; echo '[NMAP]'; nmap -sC -sV TARGET\" C-m \; \
send-keys -t pentest:1.1 \"clear; echo '[GOBUSTER]'; gobuster dir -u http://TARGET -w /usr/share/wordlists/dirb/common.txt\" C-m \; \
send-keys -t pentest:1.2 \"clear; echo '[FFUF]'; ffuf -u http://TARGET/FUZZ -w /usr/share/wordlists/dirb/common.txt\" C-m \; \


# Exploit window
new-window -t pentest:2 -n exploit \; \
split-window -h -t pentest:2 -c '#{pane_current_path}' \; \

# Clean panes
send-keys -t pentest:2.0 \"clear; echo '[EXPLOIT]'\" C-m \; \
send-keys -t pentest:2.1 \"clear; echo '[SHELL]'\" C-m \; \

select-window -t pentest:1 \; \
attach-session -t pentest
"
```