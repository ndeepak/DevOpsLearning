To create an alias for the `code . --user-data-dir=./vscode --no-sandbox` command so that you can simply type `code` in the terminal, follow these steps:
1. **Open your shell configuration file:**
    - For `bash`, this file is typically `~/.bashrc`.
    - For `zsh`, this file is typically `~/.zshrc`.
2. **Edit the file to add your alias:** Open the file with a text editor, such as `nano` or `vim`:
    `nano ~/.bashrc`
    
3. **Add the alias to the file:** Append the following line to the end of the file:    
    `alias code='code . --user-data-dir=./vscode --no-sandbox'`
    
4. **Save the file and exit the editor:**
    - In `nano`, press `CTRL+O` to save, then `CTRL+X` to exit.
    - In `vim`, press `ESC`, then type `:wq` and press `ENTER`.
5. **Apply the changes to your current shell session:**    
    `source ~/.bashrc`
After following these steps, you should be able to simply type `code` in your terminal, and it will execute the `code . --user-data-dir=./vscode --no-sandbox` command.

## Example:
### For `bash`:
`nano ~/.bashrc`
Add the alias:
`alias code='code . --user-data-dir=./vscode --no-sandbox'`

Save and exit:
`source ~/.bashrc`

### For `zsh`:
`nano ~/.zshrc`

Add the alias:
`alias code='code . --user-data-dir=./vscode --no-sandbox'`

Save and exit:
`source ~/.zshrc`

Now, typing `code` in your terminal will execute the command with your specified options.