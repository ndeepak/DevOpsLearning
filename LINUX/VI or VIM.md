# Detailed Notes on Vim/Vi
## Introduction
Vim (Vi IMproved) and its predecessor Vi are powerful text editors available on most Unix-like operating systems. Vi is the standard editor, and Vim extends it with additional features like syntax highlighting and plugin support.

---

### Modes in Vim/Vi
Vim operates in different modes:
1. **Normal Mode**: The default mode for navigation and text manipulation.
2. **Insert Mode**: Used to insert text.
3. **Visual Mode**: For selecting and highlighting text.
4. **Command-Line Mode**: For executing commands.

#### Switching Modes
- **Insert Mode**: Press `i`, `I`, `a`, `A`, `o`, or `O`.
- **Normal Mode**: Press `Esc`.
- **Visual Mode**: Press `v` for character mode, `V` for line mode, or `Ctrl-v` for block mode.    
- **Command-Line Mode**: Press `:`.

---

### Basic Navigation
- `h` - Move left
- `j` - Move down
- `k` - Move up
- `l` - Move right
#### Word and Line Navigation
- `w` - Move to the next word
- `e` - Move to the end of the word
- `b` - Move to the beginning of the word
- `0` - Move to the beginning of the line
- `^` - Move to the first non-blank character
- `$` - Move to the end of the line
---

### Inserting Text
- `i` - Insert before the cursor
- `I` - Insert at the beginning of the line
- `a` - Append after the cursor
- `A` - Append at the end of the line
- `o` - Open a new line below    
- `O` - Open a new line above
---

### Deleting Text
- `x` - Delete the character under the cursor
- `dd` - Delete the entire line
- `dw` - Delete a word
- `d$` - Delete to the end of the line    
- `d0` - Delete to the beginning of the line
---

### Copy, Cut, and Paste
- `yy` or `Y` - Copy (yank) a line
- `yw` - Yank a word
- `p` - Paste after the cursor
- `P` - Paste before the cursor
- `dd` - Cut (delete) a line

---
### Undo and Redo
- `u` - Undo the last action
- `U` - Undo all changes on the current line
- `Ctrl-r` - Redo the undone change
---

### Searching and Replacing
- `/pattern` - Search forward for 'pattern'
- `?pattern` - Search backward for 'pattern'
- `n` - Repeat the search forward
- `N` - Repeat the search backward
#### Replace Command
- `:s/old/new/` - Replace the first occurrence of 'old' with 'new' on the current line
- `:s/old/new/g` - Replace all occurrences of 'old' with 'new' on the current line
- `:%s/old/new/g` - Replace all occurrences of 'old' with 'new' in the entire file
---

### Working with Files
- `:w` - Save the file
- `:w filename` - Save as 'filename'
- `:q` - Quit
- `:q!` - Quit without saving
- `:wq` or `ZZ` - Save and quit
- `:e filename` - Open 'filename'
- `:x` - Save and exit    
---
### Window Splitting
- `:split` or `:sp` - Split horizontally
- `:vsplit` or `:vs` - Split vertically
- `Ctrl-w` followed by arrow keys to navigate between panes
- `Ctrl-w q` - Close the current pane    
---
### Customization
Vim configuration is stored in a file named `.vimrc` in the user's home directory.
#### Sample .vimrc Configuration
```
syntax on
set number       " Show line numbers
set tabstop=4    " Set tab width to 4 spaces
set shiftwidth=4 " Set indentation width to 4 spaces
set expandtab    " Convert tabs to spaces
set autoindent   " Automatically indent new lines
set mouse=a      " Enable mouse support
```

---
### Plugins and Package Management
Vim supports plugins that extend its functionality. Popular plugin managers include:
- **Pathogen**
- **Vundle**
- **vim-plug**
#### Installing vim-plug
1. Install `curl` if not present.
2. Download and place the script:
    ```
    curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
    ```
3. Add the following to `.vimrc`:
    ```
    call plug#begin('~/.vim/plugged')
    Plug 'tpope/vim-sensible'
    call plug#end()
    ```    
4. Launch Vim and run `:PlugInstall`.
---
### Differences Between Vi and Vim

| Feature             | Vi  | Vim |
| ------------------- | --- | --- |
| Syntax highlighting | No  | Yes |
| Multi-level undo    | No  | Yes |
| Plugin support      | No  | Yes |
| Visual mode         | No  | Yes |

---
### Common Tips
1. Use `gg=G` to auto-indent the entire file.
2. Use `%` to jump between matching parentheses, brackets, or braces.
3. Use `.` to repeat the last command.    
4. Learn and use registers (`"` + a letter) to copy/paste between buffers.
---
### Conclusion
Mastering Vim/Vi takes practice and customization. Begin with essential commands and gradually explore its advanced capabilities to become more efficient