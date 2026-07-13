# Combine Everything (Ultimate Flow)

### Step 1 — SSH into box
→ auto tmux starts
[AutoStart tmux on ssh login](LINUX/SystemAutoTMUX/AutoStart%20tmux%20on%20ssh%20login.md)
### Step 2 — Start pentest layout
```scss
+-----------------------+
| Recon (nmap, gobuster)|
+-----------+-----------+
| Exploit   | Shell     |
+-----------+-----------+
```
lets create different panes for window recon(which consists of nmap, gobuster and ffuf, other window for exploit and shell
`Prefix + p`
Also lets auto run tools like nmap, gobuster and ffuf using alike
`send-keys "nmap -sC -sV TARGET" C-m`
### Step 3 — Switch sessions anytime
`Prefix + s`
i am having problem with fzf
it return 123, i am in ubuntu wsl while switching other tmux session 

### Step 4 — Monitor system in status bar
→ CPU / RAM visible
```bash
set -g @plugin 'tmux-plugins/tmux-cpu'
set -g status-right "#[fg=cyan]#H | CPU: #{cpu_percentage} | RAM: #{ram_percentage} | %Y-%m-%d %H:%M"
```

---

# After completing above Then only we will move to Optional Advanced Upgrade (If You Want Next)

I can help you build:

### 1. Auto-named sessions per target

tmux new -s HTB-Lame

### 2. Pre-configured attack layouts

- web pentest
- AD pentest
- bug bounty

### 3. Logging all panes automatically

(for reports / OSCP exam)
c
### 4. tmux + nmap + ffuf automation scripts