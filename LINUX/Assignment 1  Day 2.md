### Fun Workaround Assignment: "The Great Command Quest!"

#### Objective:

Embark on a journey through the Terminal as you complete a series of quests using basic Linux commands. Your mission is to explore, organize, and manipulate files and directories, ultimately discovering the "Golden File" hidden within a series of challenges.

#### Instructions:

1. **Setup the Environment**:
    
    - Create a main directory called `CommandQuest`.
    - Inside `CommandQuest`, create subdirectories named `Forest`, `Mountain`, and `River`.
2. **Quests**:
    
    **Quest 1: The Forest of Files**
    
    - **Objective**: Populate the `Forest` directory with various files.
    - Use `touch` to create files named `tree1.txt`, `tree2.txt`, and `tree3.txt`.
    - Use `echo` and `cat` to fill these files with a description of different tree types.
    - Create a subdirectory inside `Forest` called `Animals`.
    - Move one of the tree files into the `Animals` directory using `mv`.
    
    **Quest 2: The Mountain of Mystery**
    
    - **Objective**: Organize and document files in the `Mountain` directory.
    - Use `mkdir` to create a `Peak` directory inside `Mountain`.
    - Copy the remaining tree files from `Forest` into the `Peak` using `cp`.
    - Create a file named `MountainGuide.txt` in the `Mountain` directory and write a brief guide on mountain climbing using `nano`, `vi`, or `jed`.
    
    **Quest 3: The River of Records**
    
    - **Objective**: Manage data files in the `River` directory.
    - Create a series of files (`record1.txt`, `record2.txt`, `record3.txt`) using `touch`.
    - Use `sed` to insert the text "River Data Log" at the beginning of each record file.
    - Combine the contents of all record files into a single file named `AllRecords.txt` using `cat`.
    
    **Quest 4: The Archives of the Ancients**
    
    - **Objective**: Create and extract archives.
    - Archive all files in the `Forest` directory into a ZIP file named `Forest.zip` using `zip`.
    - Extract the contents of `Forest.zip` into a new directory named `ForestBackup` using `unzip`.
    - Create a TAR archive of the `Mountain` directory named `Mountain.tar` without compression.
    
    **Quest 5: The Guardians of the Scripts**
    
    - **Objective**: Use command-line tools to process and analyse data.
    - Search for the word "Tree" in all files within the `Forest` directory using `grep`.
    - Use `awk` to display only the second column of a CSV-like data file named `data.csv` (create this file with at least three rows and columns of data).
    - Sort the contents of `AllRecords.txt` alphabetically using `sort`.
    
    **Final Quest: The Discovery of the Golden File**
    
    - **Objective**: Locate and read the hidden file.
    - The file `golden.txt` is hidden somewhere within the `/` directory. Use `ls`, `cd`, `find`, and `file` commands to locate it. Same Machine [[192.168.10.34]]
    - Once found, open and read the contents using `head` or `tail`.

#### Bonus Challenges:

- **Create a backup**: Copy the `golden.txt` file to a new location named `CommandQuest_Backup`.
- **Search for a hidden message**: Use `grep` to search for a hidden message in all text files within `CommandQuest_Backup`.

#### Submission:

- Create a text file named `CommandQuest_Completion.txt` containing:
    - The steps you took to complete each quest.
    - Any challenges faced and how you overcame them.
    - The main hidden contents message of the `golden.txt` file.

#### Note:
This assignment encourages exploration and learning of Linux commands. Feel free to use `man` or online resources (except LLMs or ChatGPTs) to understand the commands better. Have fun, and may you find the Golden File!

Note: To make it look better, Just open it in VS code, preview mode with .md format or Note Taking app like Obsidian