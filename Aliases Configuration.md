To create an alias for the `code . --user-data-dir=./vscode --no-sandbox` command so that you can simply type `code` in the terminal, follow these steps:

1. **Open your shell configuration file:**
    
    - For `bash`, this file is typically `~/.bashrc`.
    - For `zsh`, this file is typically `~/.zshrc`.
2. **Edit the file to add your alias:** Open the file with a text editor, such as `nano` or `vim`:
    
    bash
    
    Copy code
    
    `nano ~/.bashrc`
    
3. **Add the alias to the file:** Append the following line to the end of the file:
    
    bash
    
    Copy code
    
    `alias code='code . --user-data-dir=./vscode --no-sandbox'`
    
4. **Save the file and exit the editor:**
    
    - In `nano`, press `CTRL+O` to save, then `CTRL+X` to exit.
    - In `vim`, press `ESC`, then type `:wq` and press `ENTER`.
5. **Apply the changes to your current shell session:**
    
    bash
    
    Copy code
    
    `source ~/.bashrc`
    

After following these steps, you should be able to simply type `code` in your terminal, and it will execute the `code . --user-data-dir=./vscode --no-sandbox` command.

## Example:

### For `bash`:

bash

Copy code

`nano ~/.bashrc`

Add the alias:

bash

Copy code

`alias code='code . --user-data-dir=./vscode --no-sandbox'`

Save and exit:

bash

Copy code

`source ~/.bashrc`

### For `zsh`:

bash

Copy code

`nano ~/.zshrc`

Add the alias:

bash

Copy code

`alias code='code . --user-data-dir=./vscode --no-sandbox'`

Save and exit:

bash

Copy code

`source ~/.zshrc`

Now, typing `code` in your terminal will execute the command with your specified options.