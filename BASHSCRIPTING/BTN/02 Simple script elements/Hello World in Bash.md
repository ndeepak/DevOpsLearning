#### **1. Creating a Shell Script**
1. Open the **nano editor** to create a new file called `hello_world.sh`:
    `nano hello_world.sh`
    
2. Add the following script content:
    `#!/bin/bash `
    `echo "hello world"`
    - `#!/bin/bash`: This is the **shebang** that specifies the script should be run using the Bash shell.
    - `echo "hello world"`: A command to print `hello world` to the terminal.
3. Save and exit the nano editor:
    - Press `CTRL+O` to write the file.
    - Press `Enter` to confirm the filename.
    - Press `CTRL+X` to exit.

---

#### **2. Making the Script Executable**
- By default, the script does not have execution permissions. Grant execution permissions using `chmod`:
    `chmod +x hello_world.sh`
    - `+x`: Adds executable permissions for the owner, group, and others.

---
#### **3. Running the Script**
- Run the script using the following command:
    `./hello_world.sh`
    
    **Output**:
    `hello world`
---
#### **4. Key Points**
- **Shebang (`#!/bin/bash`)**: Ensures the script runs in the specified shell (Bash in this case).
- **`chmod +x`**: Converts the script into an executable file.
- **`./hello_world.sh`**: Executes the script in the current directory.

This simple workflow demonstrates how to create, edit, and execute a basic shell script.