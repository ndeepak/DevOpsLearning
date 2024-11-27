To make `--break-system-packages` the default for `pip install`, you can configure it in `pip.conf` or `pip.ini` depending on your operating system.

### Steps for Linux/MacOS:

1. Open or create the `pip.conf` file in the `~/.config/pip/` directory:
    
    bash
    
    Copy code
    
    `mkdir -p ~/.config/pip/ nano ~/.config/pip/pip.conf`
    
2. Add the following content to the file:
    
    ini
    
    Copy code
    
    `[global] break-system-packages = true`
    

### Steps for Windows:

1. Open or create the `pip.ini` file in `%APPDATA%\pip\` (usually `C:\Users\<username>\AppData\Roaming\pip\`):
    
    cmd
    
    Copy code
    
    `mkdir "%APPDATA%\pip" notepad "%APPDATA%\pip\pip.ini"`
    
2. Add the following content:
    
    ini
    
    Copy code
    
    `[global] break-system-packages = true`
    

### Verify the Configuration:

After setting it up, you can verify it with:

bash

Copy code

`pip config list`

You should see `break-system-packages = true` in the output.