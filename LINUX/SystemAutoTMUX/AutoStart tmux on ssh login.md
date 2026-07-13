# AutoStart tmux on ssh login
## Edit your shell config

	nano ~/.bashrc 
OR your rc or profile files
https://medium.com/@nagarkotideepak9/understanding-bash-profile-and-bashrc-in-unix-like-systems-6aeb8c01101e

---
## Add this at bottom
```bash
# Auto start tmux  
if command -v tmux &> /dev/null && [ -z "$TMUX" ]; then  
    tmux attach-session -t main || tmux new-session -s main  
fi
```

---

## What it does
When you SSH:
`ssh user@target`

You automatically land inside:
`tmux session "main"`

---

## Why this matters
Prevents:
- losing shells
- broken sessions
- accidental disconnect loss

---

## Real-world pentest scenario
You get reverse shell → upgrade → tmux → stable shell