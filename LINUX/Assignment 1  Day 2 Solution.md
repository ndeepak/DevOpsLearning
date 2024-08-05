## Fun Workaround Assignment: "The Great Command Quest!"

### Objective:

Embark on a journey through the Terminal as you complete a series of quests using basic Linux commands. Your mission is to explore, organize, and manipulate files and directories, ultimately discovering the "Golden File" hidden within a series of challenges.

---

### Instructions:

#### 1. **Setup the Environment:**

```
# Create the main directory
mkdir CommandQuest

# Navigate into the CommandQuest directory
cd CommandQuest

# Create subdirectories Forest, Mountain, and River
mkdir Forest Mountain River
```

#### 2. **Quests:**

**Quest 1: The Forest of Files**

Objective: Populate the Forest directory with various files.

```
# Navigate into Forest directory
cd Forest

# Create files named tree1.txt, tree2.txt, and tree3.txt
touch tree1.txt tree2.txt tree3.txt

# Fill these files with descriptions
echo "Oak: A large tree with lobed leaves." > tree1.txt
echo "Pine: A tree with needle-like leaves." > tree2.txt
echo "Maple: Known for its vibrant fall colors." > tree3.txt

# Create a subdirectory called Animals inside Forest
mkdir Animals

# Move one of the tree files into the Animals directory
mv tree1.txt Animals/

# Navigate back to the CommandQuest directory
cd ..
```

**Quest 2: The Mountain of Mystery**

Objective: Organize and document files in the Mountain directory.

```
# Navigate into Mountain directory
cd Mountain

# Create a Peak directory inside Mountain
mkdir Peak

# Copy the remaining tree files into the Peak directory
cp ../Forest/tree2.txt ../Forest/tree3.txt Peak/

# Create a file named MountainGuide.txt and write a guide
nano MountainGuide.txt
# (Write a brief guide on mountain climbing and save the file)

# Navigate back to the CommandQuest directory
cd ..
```

**Quest 3: The River of Records**

Objective: Manage data files in the River directory.

```
# Navigate into River directory
cd River

# Create a series of files (record1.txt, record2.txt, record3.txt)
touch record1.txt record2.txt record3.txt

# Insert the text "River Data Log" at the beginning of each record file
for file in record*.txt; do sed -i '1iRiver Data Log' "$file"; done

# Combine the contents of all record files into a single file
cat record*.txt > AllRecords.txt

# Navigate back to the CommandQuest directory
cd ..

```

**Quest 4: The Archives of the Ancients**

Objective: Create and extract archives.
```
# Navigate back to the CommandQuest directory
cd CommandQuest

# Archive all files in the Forest directory into a ZIP file
zip -r Forest.zip Forest/

# Create a new directory for the backup
mkdir ForestBackup

# Extract the contents of Forest.zip into the new directory
unzip Forest.zip -d ForestBackup

# Create a TAR archive of the Mountain directory
tar -cf Mountain.tar Mountain/

```

**Quest 5: The Guardians of the Scripts**

Objective: Use command-line tools to process and analyze data.

```
# Search for the word "Tree" in all files within the Forest directory
grep -r "Tree" Forest/

# Create a CSV-like data file for demonstration
echo -e "Name,Value\nA,10\nB,20\nC,30" > data.csv

# Use awk to display only the second column of data.csv
awk -F, '{print $2}' data.csv

# Sort the contents of AllRecords.txt alphabetically
sort AllRecords.txt -o AllRecords.txt
```

**Final Quest: The Discovery of the Golden File**

Objective: Locate and read the hidden file.
```
# Search for golden.txt within the CommandQuest directory
find CommandQuest -name "golden.txt"

# Once found, open and read the contents of golden.txt
# Assume golden.txt was found at /srv/shared/golden.txt
head -n 10 /srv/shared/golden.txt

```

**Bonus Challenges:
```
# Create a backup of the CommandQuest directory
cp -r CommandQuest CommandQuest_Backup

# Search for a hidden message in all text files within CommandQuest
grep -r "hidden message" CommandQuest/
```

### Submission:

Create a file named `CommandQuest_Completion.txt` with the following content:
```
1. Steps to complete each quest:
- Quest 1: Created files, moved one to a new directory.
- Quest 2: Organized files, created a guide.
- Quest 3: Managed data files, combined content.
- Quest 4: Created and extracted archives.
- Quest 5: Processed and analyzed data.

2. Challenges faced and solutions:
- Encountered permission issues: Adjusted file permissions with chmod.
- Resolved issues with file paths: Verified correct directories and paths.

3. Contents of the golden.txt file:
- (Include the contents you found)

```

---

This solution guides you through each quest with explanations and example commands. Adjust the paths and filenames as needed based on your specific setup.