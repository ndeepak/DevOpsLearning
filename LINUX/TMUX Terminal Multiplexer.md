# **Tmux: Terminal Multiplexer**

## **1. Introduction**

Tmux (Terminal Multiplexer) allows multiple terminal sessions to be managed from a single screen. It provides persistent sessions, window management, pane splitting, and customizable key bindings.
### **Use Cases**
- Managing multiple terminal sessions.
- Keeping sessions running after disconnecting.
- Efficient workflow for system administrators and developers.

---

## **2. Installation**
### **For Ubuntu/Debian**
```
sudo apt update
sudo apt install tmux
```

### **For RHEL/CentOS**
```
sudo yum install tmux
```

---

## **3. Starting and Using Tmux**
### **Basic Commands**

|Command|Description|
|---|---|
|`tmux`|Start a new tmux session.|
|`tmux new -s name`|Start a new session with a specific name.|
|`tmux attach -t name`|Reattach to an existing session.|
|`tmux ls`|List all active tmux sessions.|
|`tmux kill-session -t name`|Kill a specific session.|

---

## **4. Key Bindings**
Key bindings in tmux are prefixed by `Ctrl-b` (default). Use `Ctrl-b` followed by another key to execute commands.
### **Common Key Bindings**

|   |   |
|---|---|
|Key Combination|Description|
|`Ctrl-b d`|Detach from the session.|
|`Ctrl-b c`|Create a new window.|
|`Ctrl-b n`|Move to the next window.|
|`Ctrl-b p`|Move to the previous window.|
|`Ctrl-b w`|List all windows.|
|`Ctrl-b &`|Close the current window.|
|`Ctrl-b "`|Split the current pane horizontally.|
|`Ctrl-b %`|Split the current pane vertically.|
|`Ctrl-b o`|Move to the next pane.|
|`Ctrl-b x`|Kill the current pane.|

---
## **5. Session Management**
### **Creating and Naming Sessions**

```
tmux new -s mysession
```

### **Detaching and Attaching**
- Detach: `Ctrl-b d`
- Reattach: `tmux attach -t mysession`

### **Listing Sessions**
```
tmux ls
```

### **Killing a Session**
```
tmux kill-session -t mysession
```

---

## **6. Pane Management**
### **Splitting Panes**

|   |   |
|---|---|
|Command|Description|
|`Ctrl-b "`|Split pane horizontally.|
|`Ctrl-b %`|Split pane vertically.|

### **Navigating Panes**

|   |   |
|---|---|
|Key Combination|Description|
|`Ctrl-b o`|Move to the next pane.|
|`Ctrl-b q`|Show pane numbers for quick navigation.|
|`Ctrl-b {` and `Ctrl-b }`|Swap panes.|

### **Resizing Panes**

|   |   |
|---|---|
|Command|Description|
|`Ctrl-b :resize-pane -D`|Resize down.|
|`Ctrl-b :resize-pane -U`|Resize up.|
|`Ctrl-b :resize-pane -L`|Resize left.|
|`Ctrl-b :resize-pane -R`|Resize right.|

---

## **7. Windows and Tabs**
### **Managing Windows**

|   |   |
|---|---|
|Command|Description|
|`Ctrl-b c`|Create a new window.|
|`Ctrl-b ,`|Rename the current window.|
|`Ctrl-b n`|Switch to the next window.|
|`Ctrl-b p`|Switch to the previous window.|
|`Ctrl-b w`|Display a list of windows.|
|`Ctrl-b &`|Close the current window.|

---

## **8. Custom Layouts**
### **Creating a 2x2 Grid Layout**

```
bind g split-window -h \; split-window -v \; select-pane -t 0 \; split-window -v
```

- Add to `~/.tmux.conf`.
- Reload configuration with `tmux source-file ~/.tmux.conf`.
    

---

## **9. Customizing Tmux**
### **Changing the Prefix Key**

To change the prefix to `Ctrl-a`:

```
set-option -g prefix C-a
unbind C-b
bind C-a send-prefix
```

### **Reloading Configuration**
```
tmux source-file ~/.tmux.conf
```

### **Setting Custom Key Bindings**
Example to split panes with simpler keys:

```
bind v split-window -v
bind h split-window -h
```

---

## **10. Scripting with Tmux**
Automate tmux session creation:

```
tmux new-session -d -s mysession

tmux split-window -h

tmux split-window -v

tmux select-pane -t 0

tmux attach -t mysession
```

Save this in a script to start a predefined layout.

---

## **11. Working with Plugins**
To extend tmux functionality, use **tmux Plugin Manager (tpm)**.

### **Installing TPM**
```
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

Add this to `~/.tmux.conf`:
```
# TPM configuration
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
run '~/.tmux/plugins/tpm/tpm'
```

Reload configuration:

```
tmux source-file ~/.tmux.conf
```

Press `Ctrl-b I` to install plugins.

---

## **12. Copy Mode and Scrolling**
### **Entering Copy Mode**
- `Ctrl-b [` enters copy mode.
    

### **Navigating**

|   |   |
|---|---|
|Command|Description|
|`Arrow keys`|Move up, down, left, right.|
|`Ctrl-u`|Move half a page up.|
|`Ctrl-d`|Move half a page down.|

---

## **13. Conclusion**
Tmux is an essential tool for terminal-based workflows, offering powerful session management, pane layouts, and customization. Mastering tmux boosts efficiency, especially for system administrators and developers working on remote systems or handling multiple processes.